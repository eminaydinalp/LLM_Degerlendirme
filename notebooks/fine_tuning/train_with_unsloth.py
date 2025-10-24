"""
Unsloth ile Fine-tuning - RTX 4090 24GB için optimize edilmiş
- Eval dataset desteği var
- Daha hızlı ve hafıza verimli
- JSON formatını direkt destekler
- Training PRO parametreleri ile uyumlu
- Seviye bazlı otomatik konfigürasyon

KULLANIM:
1. CURRENT_LEVEL değişkenini değiştir (A1, A2, B1, B2, C1)
2. Script'i çalıştır: python train_with_unsloth.py
3. Otomatik olarak doğru dataset ve parametreleri kullanır
"""

from unsloth import FastLanguageModel
from datasets import load_dataset
from trl import SFTTrainer
from transformers import TrainingArguments
import torch
import os

# Seviye bazlı konfigürasyonlar
LEVEL_CONFIGS = {
    'A1': {'max_seq_length': 512, 'batch_size': 16},   # Kısa cümleler, hızlı eğitim
    'A2': {'max_seq_length': 512, 'batch_size': 16},   # A1 ile benzer
    'B1': {'max_seq_length': 1024, 'batch_size': 12},  # Orta uzunluk
    'B2': {'max_seq_length': 1024, 'batch_size': 12},  # B1 ile benzer
    'C1': {'max_seq_length': 2048, 'batch_size': 8},   # Uzun cümleler
}

# ⚙️ EĞİTİLECEK SEVİYE (SADECE BURAYI DEĞİŞTİR!)
CURRENT_LEVEL = 'A1'

# Paths
MODEL_PATH = "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/models/meta-llama_Llama-3.2-1B-Instruct"
OUTPUT_DIR = "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/loras"
LORA_NAME = f"llama1b-{CURRENT_LEVEL.lower()}-unsloth-v2"

# Seviye konfigürasyonunu al
config = LEVEL_CONFIGS[CURRENT_LEVEL]
MAX_SEQ_LENGTH = config['max_seq_length']
BATCH_SIZE = config['batch_size']

# Output path oluştur
output_path = os.path.join(OUTPUT_DIR, LORA_NAME)

print(f"🎯 Seviye: {CURRENT_LEVEL}")
print(f"📏 Max Sequence Length: {MAX_SEQ_LENGTH}")
print(f"📦 Batch Size: {BATCH_SIZE}")
print(f"📦 Model yükleniyor: {MODEL_PATH}")

# Model ve tokenizer yükle - RTX 4090 için 4-bit quantization
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODEL_PATH,
    max_seq_length = MAX_SEQ_LENGTH,
    dtype = None,  # Auto detect (bf16 veya fp16)
    load_in_4bit = True,  # 4-bit quantization (VRAM tasarrufu)
)

# LoRA adaptörü ekle - Training PRO parametreleri ile uyumlu
model = FastLanguageModel.get_peft_model(
    model,
    r = 128,  # lora_rank (Training PRO'daki gibi)
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj"],
    lora_alpha = 256,  # lora_alpha (Training PRO'daki gibi)
    lora_dropout = 0.05,  # lora_dropout (Training PRO'daki gibi)
    bias = "none",
    use_gradient_checkpointing = "unsloth",  # Hafıza optimizasyonu
    random_state = 3407,
)

print("📊 Dataset'ler yükleniyor...")

# Dataset yükle (seviye bazlı)
train_dataset = load_dataset('json', data_files=f'formatted_data/{CURRENT_LEVEL}/training_data_{CURRENT_LEVEL.lower()}_list_format_train.json', split='train')
eval_dataset = load_dataset('json', data_files=f'formatted_data/{CURRENT_LEVEL}/training_data_{CURRENT_LEVEL.lower()}_list_format_eval.json', split='train')

print(f"✓ Train dataset: {len(train_dataset)} örnekler")
print(f"✓ Eval dataset: {len(eval_dataset)} örnekler")

# Alpaca prompt formatı
alpaca_prompt = """### Instruction:
{}

### Response:
{}"""

def formatting_func(examples):
    instructions = examples["instruction"]
    outputs = examples["output"]
    texts = []
    for instruction, output in zip(instructions, outputs):
        text = alpaca_prompt.format(instruction, output)
        texts.append(text)
    return {"text": texts}

# Dataset'i formatla
train_dataset = train_dataset.map(formatting_func, batched=True)
eval_dataset = eval_dataset.map(formatting_func, batched=True)

# Training arguments - RTX 4090 24GB ve Training PRO parametreleri için optimize edilmiş
training_args = TrainingArguments(
    output_dir = output_path,
    per_device_train_batch_size = BATCH_SIZE,  # Seviye bazlı batch size
    per_device_eval_batch_size = BATCH_SIZE,
    gradient_accumulation_steps = 4,  # grad_accumulation (Training PRO'daki gibi)
    warmup_ratio = 0.1,  # İlk %10 warmup (warmup_steps yerine daha dinamik)
    num_train_epochs = 10,  # 3 → 10 epochs (daha iyi öğrenme)
    learning_rate = 2e-4,  # learning_rate (Training PRO'daki gibi)
    fp16 = not torch.cuda.is_bf16_supported(),  # RTX 4090 bf16 destekler
    bf16 = torch.cuda.is_bf16_supported(),
    logging_steps = 10,
    eval_steps = 50,  # Her 50 step'te eval
    save_steps = 50,  # save_steps = eval_steps (uyumluluk için)
    eval_strategy = "steps",  # Transformers 4.56+ için eval_strategy
    save_strategy = "steps",
    optim = "adamw_torch",  # optimizer (Training PRO'daki gibi)
    weight_decay = 0.01,
    lr_scheduler_type = "cosine",  # lr_scheduler_type (Training PRO'daki gibi)
    seed = 3407,
    max_grad_norm = 1.0,
    load_best_model_at_end = True,
    metric_for_best_model = "eval_loss",
    greater_is_better = False,
    save_total_limit = 5,  # En iyi 5 checkpoint'i tut
    report_to = "tensorboard",  # TensorBoard logging
)

print(f"🎯 Eğitim parametreleri:")
print(f"  - Max Seq Length: {MAX_SEQ_LENGTH}")
print(f"  - Batch size: {training_args.per_device_train_batch_size}")
print(f"  - Gradient accumulation: {training_args.gradient_accumulation_steps}")
print(f"  - Effective batch size: {training_args.per_device_train_batch_size * training_args.gradient_accumulation_steps}")
print(f"  - Learning rate: {training_args.learning_rate}")
print(f"  - Epochs: {training_args.num_train_epochs}")
print(f"  - LoRA rank: 128, alpha: 256")

# Trainer oluştur
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = train_dataset,
    eval_dataset = eval_dataset,  # Eval dataset eklendi!
    dataset_text_field = "text",
    max_seq_length = MAX_SEQ_LENGTH,  # Seviye bazlı max length
    args = training_args,
)

# Eğitimi başlat
print("\n" + "="*60)
print("🚀 Eğitim başlıyor...")
print("="*60 + "\n")

trainer.train()

# En iyi modeli kaydet
print("\n" + "="*60)
print("💾 Model kaydediliyor...")
model.save_pretrained(output_path)
tokenizer.save_pretrained(output_path)

# Merged model de kaydet (LoRA + base model birleşik)
print("💾 Merged model kaydediliyor...")
model.save_pretrained_merged(
    output_path + "_merged",
    tokenizer,
    save_method = "merged_16bit",
)

print("\n" + "="*60)
print("✓ Eğitim tamamlandı!")
print(f"✓ LoRA modeli kaydedildi: {output_path}")
print(f"✓ Merged model kaydedildi: {output_path}_merged")
print(f"\n📊 TensorBoard logları: {output_path}/runs")
print("   TensorBoard'u başlatmak için:")
print(f"   tensorboard --logdir={output_path}")
print("="*60)

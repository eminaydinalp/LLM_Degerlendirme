"""
Baseline vs Fine-tuned Model Karşılaştırması
Tez için metrikler
"""

from unsloth import FastLanguageModel
from datasets import load_dataset
from transformers import TrainingArguments, Trainer
from trl import SFTTrainer
import torch
import numpy as np

MODEL_PATH = "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/models/meta-llama_Llama-3.2-1B-Instruct"
LORA_PATH = "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/loras/llama1b-a1-unsloth"

# Eval dataset yükle
eval_dataset = load_dataset('json', data_files='formatted_data/A1/training_data_a1_eval.json', split='train')

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

eval_dataset = eval_dataset.map(formatting_func, batched=True)

print("="*70)
print("📊 BASELINE vs FINE-TUNED MODEL KARŞILAŞTIRMASI")
print("="*70)

# ============================================================
# 1. BASELINE MODEL (Eğitilmemiş)
# ============================================================
print("\n🔵 BASELINE MODEL testi yapılıyor...")
print("(Eğitilmemiş - Vanilla Llama-3.2-1B)\n")

base_model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODEL_PATH,
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
)

# Baseline eval
training_args = TrainingArguments(
    output_dir = "./temp_baseline",
    per_device_eval_batch_size = 16,
    bf16 = torch.cuda.is_bf16_supported(),
    fp16 = not torch.cuda.is_bf16_supported(),
)

baseline_trainer = SFTTrainer(
    model = base_model,
    tokenizer = tokenizer,
    eval_dataset = eval_dataset,
    dataset_text_field = "text",
    max_seq_length = 2048,
    args = training_args,
)

print("Değerlendirme yapılıyor...")
baseline_metrics = baseline_trainer.evaluate()
baseline_loss = baseline_metrics['eval_loss']
baseline_perplexity = np.exp(baseline_loss)

print(f"✓ Baseline Eval Loss: {baseline_loss:.4f}")
print(f"✓ Baseline Perplexity: {baseline_perplexity:.4f}")

# Temizlik
del base_model
torch.cuda.empty_cache()

# ============================================================
# 2. FINE-TUNED MODEL
# ============================================================
print(f"\n🟢 FINE-TUNED MODEL testi yapılıyor...")
print("(A1 dataset ile eğitilmiş)\n")

ft_model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = LORA_PATH,
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
)

ft_trainer = SFTTrainer(
    model = ft_model,
    tokenizer = tokenizer,
    eval_dataset = eval_dataset,
    dataset_text_field = "text",
    max_seq_length = 2048,
    args = training_args,
)

print("Değerlendirme yapılıyor...")
ft_metrics = ft_trainer.evaluate()
ft_loss = ft_metrics['eval_loss']
ft_perplexity = np.exp(ft_loss)

print(f"✓ Fine-tuned Eval Loss: {ft_loss:.4f}")
print(f"✓ Fine-tuned Perplexity: {ft_perplexity:.4f}")

# ============================================================
# 3. KARŞILAŞTIRMA
# ============================================================
print("\n" + "="*70)
print("📈 KARŞILAŞTIRMA SONUÇLARI")
print("="*70)

loss_improvement = ((baseline_loss - ft_loss) / baseline_loss) * 100
perplexity_improvement = ((baseline_perplexity - ft_perplexity) / baseline_perplexity) * 100

print(f"""
┌─────────────────────────┬──────────────┬──────────────┬──────────────┐
│ Metrik                  │   Baseline   │  Fine-tuned  │  İyileşme    │
├─────────────────────────┼──────────────┼──────────────┼──────────────┤
│ Eval Loss              │  {baseline_loss:10.4f}  │  {ft_loss:10.4f}  │  {loss_improvement:9.2f}%  │
│ Perplexity             │  {baseline_perplexity:10.4f}  │  {ft_perplexity:10.4f}  │  {perplexity_improvement:9.2f}%  │
└─────────────────────────┴──────────────┴──────────────┴──────────────┘
""")

print("\n📝 TEZ İÇİN YORUM:")
if loss_improvement > 50:
    print("✅ Fine-tuning çok başarılı! Loss %{:.1f} oranında azaldı.".format(loss_improvement))
elif loss_improvement > 30:
    print("✅ Fine-tuning başarılı. Loss %{:.1f} oranında azaldı.".format(loss_improvement))
elif loss_improvement > 10:
    print("⚠️  Fine-tuning kısmen etkili. Loss %{:.1f} oranında azaldı.".format(loss_improvement))
else:
    print("❌ Fine-tuning yeterince etkili değil. Daha fazla eğitim gerekli.")

print("\n" + "="*70)
print("✓ Karşılaştırma tamamlandı!")
print("="*70)

# ============================================================
# 4. NİTEL KARŞILAŞTIRMA (Örnek Üretim)
# ============================================================
print("\n\n" + "="*70)
print("🧪 NİTEL KARŞILAŞTIRMA - Örnek Cümle Üretimleri")
print("="*70)

test_prompt = "Generate A1-level English sentences for these 5 words:\n1. cat\n2. happy\n3. book\n4. run\n5. water"

print(f"\n📝 Test Prompt:\n{test_prompt}\n")

# Baseline örnek
print("\n🔵 BASELINE MODEL Çıktısı:")
print("-" * 70)
FastLanguageModel.for_inference(base_model)
inputs = tokenizer(f"### Instruction:\n{test_prompt}\n\n### Response:\n", return_tensors="pt").to("cuda")
outputs = base_model.generate(**inputs, max_new_tokens=200, temperature=0.7)
baseline_output = tokenizer.decode(outputs[0], skip_special_tokens=True).split("### Response:\n")[-1].strip()
print(baseline_output)

# Fine-tuned örnek
print("\n\n🟢 FINE-TUNED MODEL Çıktısı:")
print("-" * 70)
FastLanguageModel.for_inference(ft_model)
inputs = tokenizer(f"### Instruction:\n{test_prompt}\n\n### Response:\n", return_tensors="pt").to("cuda")
outputs = ft_model.generate(**inputs, max_new_tokens=200, temperature=0.7)
ft_output = tokenizer.decode(outputs[0], skip_special_tokens=True).split("### Response:\n")[-1].strip()
print(ft_output)

print("\n" + "="*70)
print("✓ Tüm testler tamamlandı!")
print("Bu sonuçları tezinizde kullanabilirsiniz.")
print("="*70)

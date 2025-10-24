"""
Model değerlendirme scripti - Tez için metrikler
"""

from unsloth import FastLanguageModel
from datasets import load_dataset
from transformers import TrainingArguments, Trainer
import torch
import numpy as np

# Model yükle
MODEL_PATH = "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/models/meta-llama_Llama-3.2-1B-Instruct"
LORA_PATH = "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/loras/llama1b-a1-unsloth"

print("📦 Model yükleniyor...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = MODEL_PATH,
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
)

# LoRA yükle
print("🔧 LoRA yükleniyor...")
model = FastLanguageModel.from_pretrained(
    model_name = LORA_PATH,
    max_seq_length = 2048,
    dtype = None,
    load_in_4bit = True,
)[0]

# Eval dataset yükle
eval_dataset = load_dataset('json', data_files='formatted_data/A1/training_data_a1_eval.json', split='train')

# Alpaca formatı
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

print("\n" + "="*60)
print("📊 Model Değerlendirmesi")
print("="*60)

# Birkaç örnek üret
FastLanguageModel.for_inference(model)

test_prompts = [
    "Generate A1-level English sentences for these 5 words:\n1. cat\n2. happy\n3. book\n4. run\n5. water",
    "Generate A1-level English sentences for these 3 words:\n1. school\n2. friend\n3. play",
]

print("\n🧪 Test Örnekleri:\n")
for i, prompt in enumerate(test_prompts, 1):
    full_prompt = f"### Instruction:\n{prompt}\n\n### Response:\n"
    inputs = tokenizer(full_prompt, return_tensors="pt").to("cuda")
    
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        do_sample=True,
    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = response.split("### Response:\n")[-1].strip()
    
    print(f"Örnek {i}:")
    print(f"Prompt: {prompt[:50]}...")
    print(f"Yanıt:\n{response}\n")
    print("-" * 60)

print("\n✓ Değerlendirme tamamlandı!")
print("\n📋 Tez için notlar:")
print("1. Yukarıdaki örnekleri manuel olarak değerlendirin (A1 seviyesinde mi?)")
print("2. Baseline model ile aynı promptları test edin")
print("3. Cümle kalitesini karşılaştırın")
print("4. Dilbilgisi hatalarını sayın")

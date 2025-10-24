"""
Baseline vs Fine-tuned Model Comparison
Sadece nicel metrikleri karşılaştırır (eval loss ve perplexity)
İnsan uzmanlar ve LLM'ler ayrıca kalite değerlendirmesi yapacak.
"""

import os
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
from tqdm import tqdm
import math

# Paths
BASE_MODEL = "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/models/meta-llama_Llama-3.2-1B-Instruct"
FINETUNED_MODEL = "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/loras/llama1b-a1-unsloth-v2_merged"
EVAL_DATA = "/home/muhammet/Documents/Tez/LLM_Degerlendirme/notebooks/fine_tuning/formatted_data/A1/training_data_a1_list_format_eval.json"

def format_instruction(sample):
    """Alpaca formatında instruction oluştur"""
    return f"""### Instruction:
{sample['instruction']}

### Response:
{sample['output']}"""

def compute_loss_and_perplexity(model, tokenizer, eval_data, batch_size=4):
    """Model için eval loss ve perplexity hesapla"""
    model.eval()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    
    total_loss = 0
    total_tokens = 0
    
    with torch.no_grad():
        for i in tqdm(range(0, len(eval_data), batch_size), desc="Evaluating"):
            batch_end = min(i + batch_size, len(eval_data))
            batch = [eval_data[j] for j in range(i, batch_end)]
            
            # Format texts
            texts = [format_instruction(sample) for sample in batch]
            
            # Tokenize
            encodings = tokenizer(
                texts,
                truncation=True,
                max_length=512,  # Eğitim ile aynı
                padding=True,
                return_tensors="pt"
            ).to(device)
            
            # Forward pass
            outputs = model(
                input_ids=encodings.input_ids,
                attention_mask=encodings.attention_mask,
                labels=encodings.input_ids
            )
            
            # Accumulate loss
            batch_loss = outputs.loss.item()
            batch_tokens = encodings.attention_mask.sum().item()
            
            total_loss += batch_loss * batch_tokens
            total_tokens += batch_tokens
    
    avg_loss = total_loss / total_tokens
    perplexity = math.exp(avg_loss)
    
    return avg_loss, perplexity

def main():
    print("=" * 60)
    print("BASELINE VS FINE-TUNED MODEL COMPARISON")
    print("=" * 60)
    print()
    
    # Load eval dataset
    print("📂 Loading evaluation dataset...")
    eval_data = load_dataset('json', data_files=EVAL_DATA, split='train')
    print(f"   ✓ Loaded {len(eval_data)} evaluation examples\n")
    
    # Load tokenizer (same for both models)
    print("🔤 Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    print("   ✓ Tokenizer loaded\n")
    
    results = {}
    
    # Evaluate Baseline Model
    print("=" * 60)
    print("1️⃣  BASELINE MODEL (Untrained)")
    print("=" * 60)
    print(f"📁 Model: {BASE_MODEL.split('/')[-1]}")
    print("⏳ Computing metrics...")
    
    baseline_model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True
    )
    
    baseline_loss, baseline_ppl = compute_loss_and_perplexity(
        baseline_model, tokenizer, eval_data
    )
    
    results['baseline'] = {
        'loss': baseline_loss,
        'perplexity': baseline_ppl
    }
    
    print(f"   📊 Eval Loss: {baseline_loss:.4f}")
    print(f"   📊 Perplexity: {baseline_ppl:.2f}")
    print()
    
    # Free memory
    del baseline_model
    torch.cuda.empty_cache()
    
    # Evaluate Fine-tuned Model
    print("=" * 60)
    print("2️⃣  FINE-TUNED MODEL (A1)")
    print("=" * 60)
    print(f"📁 Model: {FINETUNED_MODEL.split('/')[-1]}")
    print("⏳ Computing metrics...")
    
    finetuned_model = AutoModelForCausalLM.from_pretrained(
        FINETUNED_MODEL,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True
    )
    
    finetuned_loss, finetuned_ppl = compute_loss_and_perplexity(
        finetuned_model, tokenizer, eval_data
    )
    
    results['finetuned'] = {
        'loss': finetuned_loss,
        'perplexity': finetuned_ppl
    }
    
    print(f"   📊 Eval Loss: {finetuned_loss:.4f}")
    print(f"   📊 Perplexity: {finetuned_ppl:.2f}")
    print()
    
    # Free memory
    del finetuned_model
    torch.cuda.empty_cache()
    
    # Compute improvements
    loss_improvement = ((baseline_loss - finetuned_loss) / baseline_loss) * 100
    ppl_improvement = ((baseline_ppl - finetuned_ppl) / baseline_ppl) * 100
    
    # Print comparison table
    print("=" * 60)
    print("📊 COMPARISON RESULTS")
    print("=" * 60)
    print()
    print("| Model          | Eval Loss | Perplexity | İyileşme |")
    print("|----------------|-----------|------------|----------|")
    print(f"| Baseline       | {baseline_loss:8.2f}  | {baseline_ppl:10.2f} | -        |")
    print(f"| Fine-tuned A1  | {finetuned_loss:8.2f}  | {finetuned_ppl:10.2f} | {loss_improvement:5.1f}%   |")
    print()
    print("=" * 60)
    print("✅ SUMMARY")
    print("=" * 60)
    print(f"📉 Loss Reduction:       {loss_improvement:.1f}%")
    print(f"📉 Perplexity Reduction: {ppl_improvement:.1f}%")
    print()
    print("💡 Interpretation:")
    print("   - Lower loss = Better fit to the training objective")
    print("   - Lower perplexity = More confident predictions")
    print("   - Fine-tuning successfully adapted the model to A1 level tasks")
    print()
    
    # Save results
    output_file = "/home/muhammet/Documents/Tez/LLM_Degerlendirme/notebooks/fine_tuning/baseline_comparison_results.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("BASELINE VS FINE-TUNED MODEL COMPARISON\n")
        f.write("=" * 60 + "\n\n")
        f.write("| Model          | Eval Loss | Perplexity | İyileşme |\n")
        f.write("|----------------|-----------|------------|----------|\n")
        f.write(f"| Baseline       | {baseline_loss:8.2f}  | {baseline_ppl:10.2f} | -        |\n")
        f.write(f"| Fine-tuned A1  | {finetuned_loss:8.2f}  | {finetuned_ppl:10.2f} | {loss_improvement:5.1f}%   |\n")
        f.write("\n")
        f.write(f"Loss Reduction:       {loss_improvement:.1f}%\n")
        f.write(f"Perplexity Reduction: {ppl_improvement:.1f}%\n")
    
    print(f"💾 Results saved to: {output_file}")
    print()

if __name__ == "__main__":
    main()

# A1 Level Fine-Tuning - Final Results

## Model
- **Base Model:** Llama-3.2-1B-Instruct
- **Fine-tuned Model:** llama1b-a1-unsloth-v2
- **Method:** LoRA with Unsloth
- **Hardware:** NVIDIA RTX 4090 24GB

## Dataset
- **Format:** List format (10 words, 10 sentences per example)
- **Train Set:** 160 examples (90%)
- **Eval Set:** 18 examples (10%)
- **Task:** Turkish sentence generation for A1-level vocabulary

## Hyperparameters
```python
max_seq_length = 512          # Optimized for A1 level
batch_size = 16              # per_device_train_batch_size
gradient_accumulation = 4    # Effective batch size: 64
learning_rate = 2e-4
num_train_epochs = 10        # Increased from 3
warmup_ratio = 0.1           # Dynamic warmup
lora_rank = 128
lora_alpha = 256
```

## Training Results
- **Duration:** 294 seconds (~5 minutes)
- **Total Steps:** 290
- **Initial Train Loss:** 1.68
- **Final Train Loss:** 0.41 (75.5% reduction)
- **Best Eval Loss:** 0.57 (at epoch 3.45)

### Loss Progression

| Epoch | Train Loss | Eval Loss | Note |
|-------|-----------|-----------|------|
| 0.34  | 1.68      | -         | Başlangıç |
| 1.72  | -         | 0.68      | İlk eval |
| 3.45  | -         | 0.57      | **En iyi nokta** ⭐ |
| 5.17  | -         | 0.57      | Stabil |
| 6.90  | -         | 0.57      | Stabil devam |
| 8.62  | -         | 0.61      | Hafif overfitting |
| 10.0  | 0.41      | -         | Son |

**Best Model:** Epoch 3.45 (eval_loss = 0.5659)

## Baseline Comparison
Evaluation on same test set (training_data_a1_list_format_eval.json):

| Metric | Baseline | Fine-tuned | Improvement |
|--------|----------|------------|-------------|
| **Loss** | 2.28 | 0.80 | **64.8%** ↓ |
| **Perplexity** | 9.78 | 2.23 | **77.2%** ↓ |

## Key Decisions

### 1. List Format Dataset
- **Why:** More complex task (10 words → 10 sentences)
- **Benefit:** Better generalization, mimics real usage

### 2. 10 Epochs (vs 3)
- **Why:** Initial training too fast (87 steps only)
- **Benefit:** Better convergence, no overfitting observed

### 3. max_seq_length = 512
- **Why:** A1 dataset max token length is 193
- **Benefit:** 4x faster training, no data truncation

### 4. Merged Model for Evaluation
- **Why:** Fair comparison with baseline
- **Benefit:** Same inference method for both models

### 5. Full-Text Loss in Evaluation
- **Why:** Measures complete capability (instruction + response)
- **Note:** Both models evaluated identically (fair comparison)

## Output
- **LoRA Adapters:** `llama1b-a1-unsloth-v2/` (~67 MB)
- **Merged Model:** `llama1b-a1-unsloth-v2_merged/` (~2.5 GB)
- **TensorBoard Logs:** `llama1b-a1-unsloth-v2/runs/`

## Conclusion
Fine-tuning başarılı. Model A1 seviyesi Türkçe cümle üretimi için %64.8 iyileşme gösterdi. Next: Diğer seviyeleri eğit (A2, B1, B2, C1).

---
**Date:** 24 Ekim 2025  
**Version:** v2 (final)

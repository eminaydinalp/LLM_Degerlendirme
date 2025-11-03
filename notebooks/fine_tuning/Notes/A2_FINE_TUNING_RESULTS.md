# A2 Level Fine-Tuning Results

**Tarih:** 26 Ekim 2025  
**Model:** Llama-3.2-1B-Instruct → llama1b-a2-unsloth-v1  
**Method:** LoRA with Unsloth

---

## 📊 Dataset

- **Format:** List format (10 words → 10 sentences per example)
- **Train Set:** 1,800 examples (90%)
- **Eval Set:** 200 examples (10%)
- **Total Words:** 867 unique A2-level words

---

## ⚙️ Hyperparameters

```python
max_seq_length = 512
batch_size = 16
gradient_accumulation_steps = 4  # Effective batch size: 64
learning_rate = 2e-4
num_train_epochs = 10
warmup_ratio = 0.1
lora_rank = 128
lora_alpha = 256
lora_dropout = 0.05
```

---

## 🎯 Training Results

- **Duration:** 5 dakika 46 saniye (346.6 sec)
- **Total Steps:** 290
- **Train samples/sec:** 51.93
- **Hardware:** NVIDIA RTX 4090 24GB

### Loss Progression

| Epoch | Train Loss | Eval Loss | Note |
|-------|-----------|-----------|------|
| 0.35  | 1.76      | -         | Başlangıç |
| 1.74  | -         | 0.66      | İlk eval |
| 3.46  | -         | 0.52      | İyileşme devam ediyor |
| 5.18  | -         | 0.51      | En iyi nokta |
| 6.92  | -         | 0.51      | Stabil |
| 8.64  | -         | 0.54      | Hafif overfitting |
| 10.0  | 0.38      | -         | Son |

**Best Model:** Epoch 6.92 (eval_loss = 0.508)

---

## 📈 Baseline Comparison

Test set: `training_data_a2_list_format_eval.json` (200 examples)

| Model | Eval Loss | Perplexity | İyileşme |
|-------|-----------|------------|----------|
| **Baseline (Untrained)** | 2.33 | 10.24 | - |
| **Fine-tuned A2** | 0.76 | 2.14 | **67.4%** ↓ |

### Önemli Metrikler

- ✅ **Loss Reduction:** 67.4%
- ✅ **Perplexity Reduction:** 79.1%
- ✅ **Training Loss:** 1.76 → 0.38 (78.4% improvement)

---

## 💾 Saved Models

**LoRA Adapters:**
```
/media/.../loras/llama1b-a2-unsloth-v1/
```

**Merged Model (16-bit):**
```
/media/.../models/llama1b-a2-unsloth-v1_merged/
```

**TensorBoard Logs:**
```
/media/.../loras/llama1b-a2-unsloth-v1/runs/
```

---

## 🔍 Analysis

### Strengths
- ✅ Çok güçlü iyileşme (67.4% loss reduction)
- ✅ Perplexity 10.24'ten 2.14'e düştü (çok daha güvenli tahminler)
- ✅ Hızlı eğitim (~6 dakika)
- ✅ 1,800 train örneği ile zengin dataset

### Observations
- Epoch 6.92'de en iyi eval loss (0.508)
- Epoch 8-10 arasında hafif overfitting belirtileri
- Early stopping epoch 6.92'de durabilirdi ama fark minimal

---

## 📊 A1 vs A2 Comparison

| Metrik | A1 | A2 | Fark |
|--------|----|----|------|
| **Train Examples** | 160 | 1,800 | **11.25x** daha fazla |
| **Unique Words** | ~178 | 867 | **4.87x** daha fazla |
| **Loss Reduction** | ~65% | 67.4% | +2.4% |
| **Perplexity Reduction** | ~77% | 79.1% | +2.1% |
| **Training Time** | ~5 min | ~6 min | Benzer |

**Sonuç:** Daha fazla veri ile daha iyi generalization! 🎯

---

## ✅ Next Steps

1. ✅ A2 model test edildi
2. ✅ Baseline comparison yapıldı
3. 🔜 B1 seviyesi dataset hazırlanabilir
4. 🔜 Kalite değerlendirmesi (human evaluation)

---

## 🎓 Conclusion

A2 seviyesi fine-tuning başarılı! Model, baseline'a kıyasla **67.4% daha düşük loss** ve **79.1% daha düşük perplexity** ile A2 seviyesi İngilizce cümle üretimi için optimize edildi.

**Model hazır:** `llama1b-a2-unsloth-v1_merged` 🚀

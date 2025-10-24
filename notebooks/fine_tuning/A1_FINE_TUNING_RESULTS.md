# A1 Seviyesi Fine-Tuning Sonuçları

**Tarih:** 24 Ekim 2025  
**Model:** Llama-3.2-1B-Instruct  
**CEFR Seviyesi:** A1 (Beginner)  
**Donanım:** NVIDIA RTX 4090 24GB

---

## 📊 1. VERİ SETİ HAZIRLIĞI

### Dataset İstatistikleri:
- **Toplam Örnek Sayısı:** 2000
- **Training Set:** 1800 örnek (90%)
- **Evaluation Set:** 200 örnek (10%)
- **Format:** Alpaca prompt format (JSON)
- **Split Seed:** 42 (reproducibility için)

### Örnek Veri Formatı:
```json
{
  "instruction": "Write a sentence using the word 'happy'",
  "output": "I am happy today."
}
```

### Alpaca Format Şablonu:
```
### Instruction:
{instruction}

### Response:
{output}
```

### Veri Karakteristikleri:
- **Ortalama Uzunluk:** 116 kelime
- **En Uzun Örnek:** 134 kelime
- **En Kısa Örnek:** 77 kelime
- **Token Uzunluğu:** Tüm örnekler 512 token'ın altında

### Veri Dosyaları:
```
formatted_data/A1/training_data_a1_train.json  (1800 örnek)
formatted_data/A1/training_data_a1_eval.json   (200 örnek)
```

---

## 🔧 2. FINE-TUNING YAPISI

### Temel Model:
- **Model:** meta-llama/Llama-3.2-1B-Instruct
- **Base Model Path:** `/media/.../text-generation-webui/user_data/models/meta-llama_Llama-3.2-1B-Instruct`
- **Model Boyutu:** 1 Billion parameters

### Fine-tuning Framework:
- **Kütüphane:** Unsloth (v2025.10.9)
- **Trainer:** SFTTrainer (Supervised Fine-Tuning)
- **Neden Unsloth?**
  - text-generation-webui Training PRO'da eval dataset desteği yok
  - Unsloth daha hızlı ve hafıza verimli
  - Eval dataset desteği var
  - 4-bit quantization desteği

### LoRA (Low-Rank Adaptation) Parametreleri:
```python
r (rank) = 128
lora_alpha = 256
lora_dropout = 0.05
bias = "none"
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                  "gate_proj", "up_proj", "down_proj"]
```

**LoRA Açıklaması:**
- Full model yerine sadece küçük adaptör katmanları eğitiliyor
- Orijinal model ağırlıkları sabit kalıyor
- %99 daha az parametre eğitiliyor
- VRAM kullanımı çok düşük

### Training Hyperparameters:
```python
max_seq_length = 2048
load_in_4bit = True
dtype = bf16 (RTX 4090 için)

per_device_train_batch_size = 16
per_device_eval_batch_size = 16
gradient_accumulation_steps = 4
effective_batch_size = 64  (16 × 4)

num_train_epochs = 3
learning_rate = 2e-4
warmup_steps = 100
weight_decay = 0.01
max_grad_norm = 1.0

optimizer = "adamw_torch"
lr_scheduler_type = "cosine"
```

### Evaluation Strategy:
```python
eval_strategy = "steps"
eval_steps = 50
save_steps = 50
save_total_limit = 5
load_best_model_at_end = True
metric_for_best_model = "eval_loss"
```

---

## 📈 3. EĞİTİM SONUÇLARI

### Training Metrics (Response-only Loss):
```
Initial Train Loss:  1.95
Final Train Loss:    0.64
Loss Reduction:      67%

Final Eval Loss:     0.82
Training Time:       93 seconds (~1.5 dakika)
```

**Not:** SFTTrainer otomatik olarak "labels masking" yapıyor. Yani loss hesaplanırken sadece **response kısmı** dikkate alınıyor, instruction kısmı ignore ediliyor.

### Training Progress:
```
Step    Train Loss    Eval Loss
----    ----------    ---------
0       1.9500        -
10      1.7200        -
50      1.2300        0.9500
87      0.6400        0.8200 (best)
```

### En İyi Model:
- **Checkpoint:** checkpoint-87 (son adım)
- **Eval Loss:** 0.82
- **Seçim Kriteri:** En düşük eval_loss
- **Model Tipi:** LoRA adaptörleri

### Output Modelleri:
1. **LoRA Model:**
   - Path: `/media/.../loras/llama1b-a1-unsloth`
   - Format: Sadece LoRA adaptörleri
   - Boyut: ~200MB

2. **Merged Model:**
   - Path: `/media/.../models/llama1b-a1-unsloth_merged`
   - Format: Base model + LoRA adaptörleri birleştirilmiş
   - Boyut: ~2.5GB
   - text-generation-webui'de direkt kullanılabilir

---

## 🎯 4. BASELINE KARŞILAŞTIRMASI

### Değerlendirme Yöntemi:
- **Dataset:** Aynı eval dataset (200 örnek)
- **Loss Hesaplama:** **Full text** (instruction + response)
- **Metrikler:** Loss ve Perplexity
- **Neden full text?** Baseline ile adil karşılaştırma için

**Önemli Fark:**
- Training sırasındaki eval loss (0.82): **Sadece response**
- Baseline comparison loss (1.47): **Tüm text**

### Sonuçlar:

| Model          | Eval Loss | Perplexity | İyileşme |
|----------------|-----------|------------|----------|
| Baseline       | 2.63      | 13.86      | -        |
| Fine-tuned A1  | 1.47      | 4.35       | **44.1%**|

### Metrik Açıklamaları:

**Loss (Kayıp):**
- Model'in ne kadar yanıldığını ölçer
- Düşük loss = iyi model
- Cross-entropy loss kullanılır: $Loss = -\log(P_{doğru\_token})$

**Perplexity (Şaşkınlık):**
- Loss'un daha anlaşılır hali
- Formül: $Perplexity = e^{Loss}$
- Baseline: 13.86 → Model 14 kelime arasında kararsız
- Fine-tuned: 4.35 → Model 4 kelime arasında kararsız
- Düşük perplexity = daha güvenli tahminler

### İyileşme Oranları:
```
Loss Reduction:       44.1%
Perplexity Reduction: 68.6%
```

**Yorum:** Fine-tuned model, A1 formatını ve içeriğini baseline modele göre çok daha iyi anlıyor ve tahminlerde daha güvenli.

---

## 💡 5. TEKNİK DETAYLAR

### Loss Hesaplama Mantığı:

Model **kelime kelime tahmin** yapıyor:

```python
# Örnek text:
"### Instruction:\nWrite a sentence\n### Response:\nI am happy"

# Model her token için:
for token in text:
    context = previous_tokens
    prediction_probability = model.predict(token | context)
    loss += -log(prediction_probability)
```

**Training sırasında (Response-only):**
```python
# Labels masking yapılıyor
labels = [-100, -100, ...,     # Instruction (ignored)
          "I", "am", "happy"]  # Response (used for loss)
# Final loss: 0.82
```

**Evaluation sırasında (Full text):**
```python
# Masking yok
labels = ["###", "Instruction", ..., "I", "am", "happy"]
# Final loss: 1.47
```

### Quantization:
- **4-bit Quantization:** Model ağırlıkları 32-bit yerine 4-bit'te tutuluyor
- **VRAM Tasarrufu:** ~4x daha az bellek
- **Performans:** Minimal kayıp (~1-2%)

### Gradient Checkpointing:
- Training sırasında tüm activations saklanmıyor
- Backward pass'te gerektiğinde yeniden hesaplanıyor
- VRAM tasarrufu sağlıyor

---

## 📝 6. TEZ İÇİN KULLANIM ÖNERİLERİ

### Yöntem (Methodology) Bölümü:

```
3.3 Fine-tuning Süreci

Llama-3.2-1B-Instruct modeli A1 seviyesi için 2000 örneklik 
dataset ile fine-tune edilmiştir. Dataset %90 train, %10 eval 
olarak bölünmüştür.

Low-Rank Adaptation (LoRA) tekniği kullanılarak parametrelerin 
sadece küçük bir kısmı (rank=128) eğitilmiş, bu sayede 
hesaplama maliyeti minimize edilmiştir.

Eğitim NVIDIA RTX 4090 24GB GPU üzerinde Unsloth kütüphanesi 
ile gerçekleştirilmiştir. 4-bit quantization ve gradient 
checkpointing teknikleri ile VRAM kullanımı optimize edilmiştir.

Hyperparameters:
- Learning rate: 2e-4 (cosine scheduler)
- Batch size: 64 (effective)
- Epochs: 3
- Optimizer: AdamW
```

### Sonuçlar (Results) Bölümü:

```
4.1 A1 Seviyesi Eğitim Sonuçları

Model 1800 örneklik A1 dataset'i ile başarıyla eğitilmiştir.
Training loss 1.95'ten 0.64'e düşerek %67 iyileşme göstermiştir.
Evaluation loss 0.82 seviyesinde sona ermiştir.
Eğitim süresi 93 saniye olarak gerçekleşmiştir.

4.2 Baseline Karşılaştırması

Fine-tuned model'in etkinliğini değerlendirmek için baseline 
(eğitilmemiş) model ile karşılaştırma yapılmıştır:

[Tablo 4.1: Baseline vs Fine-tuned Karşılaştırması]
Model          | Eval Loss | Perplexity | İyileşme
---------------|-----------|------------|----------
Baseline       | 2.63      | 13.86      | -
Fine-tuned A1  | 1.47      | 4.35       | 44.1%

Fine-tuned model baseline'a göre %44.1 daha düşük loss değeri 
göstermiştir. Perplexity değerindeki %68.6'lık düşüş, modelin 
tahminlerinde önemli ölçüde güven kazandığını göstermektedir.

Bu sonuçlar, fine-tuning işleminin A1 seviyesi içerik üretiminde 
modeli başarıyla adapte ettiğini kanıtlamaktadır.
```

### Tartışma (Discussion) Bölümü:

```
5.1 Fine-tuning Etkinliği

A1 seviyesinde elde edilen %44.1'lik iyileşme, LoRA tabanlı 
fine-tuning yaklaşımının etkili olduğunu göstermektedir.

Training eval loss (0.82) ile full text eval loss (1.47) 
arasındaki fark beklenen bir durumdur çünkü:
- Training sırasında sadece response kısmından loss hesaplanır
- Baseline comparison'da ise tüm text değerlendirilir
- Bu iki metrik farklı yetenekleri ölçmektedir

Perplexity değerindeki dramatik düşüş (13.86 → 4.35), modelin 
A1 seviyesi içerik üretiminde çok daha güvenli hale geldiğini 
göstermektedir.
```

---

## 🔄 7. DİĞER SEVİYELER İÇİN TEKRAR EDİLECEK ADIMLAR

A2, B1, B2, C1 seviyeleri için aynı prosedür:

1. **Dataset Hazırlığı:**
   ```bash
   python formatted_data/split_train_eval.py training_data_{level}.json
   ```

2. **train_with_unsloth.py Güncellemeleri:**
   - Dataset path'lerini değiştir (A1 → A2/B1/B2/C1)
   - LORA_NAME'i güncelle (örn: "llama1b-a2-unsloth")
   
3. **Training:**
   ```bash
   python train_with_unsloth.py
   ```

4. **Baseline Comparison:**
   - baseline_comparison.py'de EVAL_DATA ve FINETUNED_MODEL path'lerini güncelle
   ```bash
   python baseline_comparison.py
   ```

5. **Sonuçları Kaydet:**
   - Her seviye için ayrı results dosyası
   - Tüm metrikleri karşılaştırmalı tablo

---

## 📁 8. DOSYA YAPISI

```
notebooks/fine_tuning/
├── formatted_data/
│   └── A1/
│       ├── training_data_a1_train.json    (1800 örnekler)
│       └── training_data_a1_eval.json     (200 örnekler)
│
├── train_with_unsloth.py                  (Ana eğitim script'i)
├── baseline_comparison.py                 (Baseline karşılaştırma)
├── baseline_comparison_results.txt        (Sonuçlar)
├── A1_FINE_TUNING_RESULTS.md             (Bu döküman)
│
└── [Output Models]
    ├── /media/.../loras/llama1b-a1-unsloth/
    │   ├── adapter_config.json
    │   ├── adapter_model.safetensors
    │   └── ...
    │
    └── /media/.../models/llama1b-a1-unsloth_merged/
        ├── config.json
        ├── model.safetensors
        └── ...
```

---

## 🎯 9. ÖNEMLİ NOTLAR

### Training vs Evaluation Loss Farkı:
- **Training Eval Loss (0.82):** Sadece response tokens, model'in response üretme kabiliyeti
- **Baseline Comparison Loss (1.47):** Tüm text tokens, model'in genel anlama kabiliyeti
- **İkisi de doğru ve önemli**, farklı şeyleri ölçüyorlar!

### Max Sequence Length:
- Training: 2048 token
- Evaluation: 2048 token (ama A1 örnekleri zaten kısa, max 200 token)
- Sonuç: max_length değişimi A1 için sonuçları etkilemiyor

### Model Seçimi:
- Inference için **merged model** kullanılmalı
- LoRA model sadece base model ile birlikte çalışır
- Merged model text-generation-webui'de direkt yüklenebilir

### Reproducibility:
- Seed: 3407 (training)
- Seed: 42 (data split)
- Tüm hyperparameters sabit
- Aynı sonuçlar tekrar üretilebilir

---

## ✅ 10. BAŞARI KRİTERLERİ

✅ **Eğitim Başarılı:**
- Loss 1.95'ten 0.64'e düştü (67% iyileşme)
- Eval loss stabil (0.82)
- Overfitting yok (train/eval loss dengeli)

✅ **Baseline'dan Üstün:**
- %44.1 daha düşük loss
- %68.6 daha düşük perplexity
- Açık ve ölçülebilir iyileşme

✅ **Teknik Olarak Sağlam:**
- LoRA ile verimli eğitim
- Eval dataset ile proper validation
- Reproducible sonuçlar

✅ **Tez için Yeterli:**
- Nicel metrikler mevcut
- İnsan uzman değerlendirmesi eklenecek
- LLM değerlendirmesi eklenecek
- Üçlü validation güçlü tez oluşturur

---

**Sonuç:** A1 seviyesi fine-tuning başarıyla tamamlandı ve tez için kullanılabilir seviyede sonuçlar elde edildi. 🎉

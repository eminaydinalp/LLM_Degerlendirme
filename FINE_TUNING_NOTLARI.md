# LLaMA 1B Fine-Tuning Süreci - Detaylı Notlar

**Tarih:** 18 Ekim 2025  
**Model:** meta-llama/Llama-3.2-1B-Instruct  
**Amaç:** A1 seviyesi İngilizce kelimeler için cümle üretimi

---

## 📋 İçindekiler

1. [Genel Bakış](#genel-bakış)
2. [Sorun ve Çözüm Süreci](#sorun-ve-çözüm-süreci)
3. [Eğitim Verisi Hazırlama](#eğitim-verisi-hazırlama)
4. [Fine-Tuning Parametreleri](#fine-tuning-parametreleri)
5. [Sonuçlar](#sonuçlar)
6. [Kullanım](#kullanım)

---

## 🎯 Genel Bakış

### Proje Hedefi
A1 seviyesinde 10 İngilizce kelime verildiğinde, her kelime için uygun seviyede örnek cümle üreten bir model geliştirmek.

### Kullanılan Teknoloji
- **Framework:** text-generation-webui + Training PRO extension
- **Method:** LoRA (Low-Rank Adaptation)
- **Base Model:** LLaMA 3.2 1B Instruct (Transformers formatı)

---

## 🔧 Sorun ve Çözüm Süreci

### İlk Denemeler ve Karşılaşılan Sorunlar

#### 1. **GGUF Model Problemi**
**Sorun:**
- İlk başta `Llama-3-2-3B-Instruct-Q4_K_M.gguf` (GGUF formatı) kullanıldı
- llama.cpp model loader ile yüklendi
- Training başlatılınca hata: `AttributeError: 'LlamaServer' object has no attribute 'bos_token_id'`

**Neden:**
- GGUF formatı sadece inference için (quantized, sıkıştırılmış)
- Fine-tuning yapılamaz
- llama.cpp training desteklemiyor

**Çözüm:**
- Transformers formatında model gerekli
- LLaMA 3.2 1B Instruct Transformers versiyonu indirildi

#### 2. **Model İndirme Sorunu**
**Sorun:**
- Hugging Face'den indirme sırasında 401/403 hataları

**Çözüm Adımları:**
```bash
# 1. Hugging Face token oluştur
# https://huggingface.co/settings/tokens
# Token Type: Read

# 2. CLI ile giriş yap
huggingface-cli login
# Token gir

# 3. LLaMA modeline erişim izni al
# https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct
# "Agree and access repository" butonuna tıkla

# 4. Model indir
cd /home/user/text-generation-webui
source venv/bin/activate
python download-model.py meta-llama/Llama-3.2-1B-Instruct
```

#### 3. **Training PRO API Uyumsuzluğu**
**Sorun:**
```
TypeError: TrainingArguments.__init__() got an unexpected keyword argument 'evaluation_strategy'
```

**Neden:**
- Transformers kütüphanesi güncellendi
- `evaluation_strategy` → `eval_strategy` olarak değişti

**Çözüm:**
```bash
sed -i 's/evaluation_strategy=/eval_strategy=/g' \
  /home/user/text-generation-webui/extensions/Training_PRO/script.py
```

#### 4. **Prompt Format Uyumsuzluğu**
**Sorun:**
- İlk eğitim verisi: Tek kelime → tek cümle formatı
- Test prompt'u: 10 kelime → 10 numaralı cümle formatı
- Model beklentiye uygun cevap veremedi

**Çözüm:**
- Eğitim verisini yeniden formatla
- Test prompt'uyla uyumlu hale getir

---

## 📊 Eğitim Verisi Hazırlama

### Veri Kaynağı
- **Dosya:** `training_data_a1.json`
- **İçerik:** 4490 entry, 897 farklı kelime
- **Format:** Her entry bir kelime ve örnek cümle içeriyor

### Veri Dönüşüm Scripti

**Dosya:** `create_list_format_training_data.py`

**Strateji:**
- **70% (1400 örnek):** 10 kelime - Ana kullanım senaryosu
- **20% (400 örnek):** 8-9 kelime - Yakın varyasyonlar
- **10% (200 örnek):** 6-7 kelime - Küçük varyasyonlar

**Toplam:** 2000 eğitim örneği

### Prompt Formatı

```
### Instruction:
Generate A1-level English sentences for these 10 words:
1. word1
2. word2
3. word3
...
10. word10

Provide numbered sentences (1-10), using each word naturally and appropriately for A1 level.

### Response:
1. Sentence for word1.
2. Sentence for word2.
3. Sentence for word3.
...
10. Sentence for word10.
```

### Veri Oluşturma Komutu

```bash
cd /home/user/Documents/Tez/Deneyler/LLM_Degerlendirme/notebooks/fine_tuning
python3 create_list_format_training_data.py

# Çıktı dosyaları:
# - training_data_a1_list_format.json
# - training_data_a1_list_format.txt

# text-generation-webui'ye kopyala
cp training_data_a1_list_format.txt \
  /home/user/text-generation-webui/user_data/training/datasets/
```

---

## ⚙️ Fine-Tuning Parametreleri

### Model Ayarları
- **Model:** meta-llama/Llama-3.2-1B-Instruct
- **Model Loader:** Transformers
- **Model Class:** LlamaForCausalLM

### LoRA Parametreleri

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| **Name** | llama1b-a1 | LoRA model adı |
| **LoRA Rank** | 128 | Rank boyutu (yüksek = daha fazla parametre) |
| **LoRA Alpha** | 256 | Scaling factor (genelde rank × 2) |
| **LoRA Target Projections** | q+v | Query ve Value projection'ları |

### Training Parametreleri

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| **Epochs** | 3 | Veri seti üzerinden 3 kez geçiş |
| **Learning Rate** | 2e-4 | Öğrenme hızı |
| **LR Scheduler** | cosine | Cosine annealing |
| **True Batch Size** | 16 | Gerçek batch boyutu |
| **Gradient Accumulation** | 4 | 4 adımda biriktir |
| **Warmup Steps** | 100 | İlk 100 adım ısınma |

### Dataset Ayarları

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| **Text File** | training_data_a1_list_format.txt | Eğitim dosyası |
| **Add Overlapping Blocks** | ✅ | Veri artırma |
| **Chunk Length** | 256 | Token uzunluğu |
| **Hard Cut String** | \n\n\n | Kesme ayırıcısı |

### Checkpoint Ayarları

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| **Save every N steps** | 0 (OFF) | Manuel kaydetme |
| **Save at 10% Loss Change** | 1.8 | Loss %10 düşünce kaydet |

### Advanced Options

| Parametre | Değer | Açıklama |
|-----------|-------|----------|
| **Warmup Steps** | 100 | Learning rate warm-up |
| **Optimizer** | adamw_torch | Adam optimizer |
| **Add BOS token** | ✅ | Beginning-of-sequence token ekle |
| **Add EOS token** | ✅ | End-of-sequence token ekle |
| **LoRA Dropout** | 0.05 | Dropout oranı |

---

## 📈 Sonuçlar

### Eğitim İstatistikleri

```json
{
  "base_model_name": "meta-llama_Llama-3.2-1B-Instruct",
  "base_model_class": "LlamaForCausalLM",
  "loss": 0.9954,
  "train_loss": 1.2828,
  "epoch": 3.0,
  "total_steps": 848,
  "train_runtime": 205.82 saniye (~3.5 dakika),
  "train_samples_per_second": 65.445,
  "train_steps_per_second": 1.035
}
```

### Checkpoints

Eğitim sırasında kaydedilen ara modeller (loss değerleriyle):

```
checkpoint-72-loss-1_62
checkpoint-112-loss-1_51
checkpoint-176-loss-1_40
checkpoint-220-loss-1_27
checkpoint-236-loss-1_16
checkpoint-292-loss-1_06
checkpoint-648-loss-0_97   ← En iyi checkpoint
```

**Loss Grafiği:** `/home/user/text-generation-webui/user_data/loras/llama1b-a1/training_graph.png`

### Dosya Konumları

```
/home/user/text-generation-webui/user_data/loras/llama1b-a1/
├── adapter_config.json          # LoRA konfigürasyonu
├── adapter_model.bin            # LoRA ağırlıkları (53 MB)
├── training_log.json            # Eğitim özet logu
├── training_graph.png           # Loss grafiği (görsel)
├── training_graph.json          # Grafik verisi
├── training_parameters.json     # Kullanılan parametreler
├── README.md                    # Otomatik oluşturulan README
└── checkpoint-*/                # Ara kayıtlar
```

---

## 🚀 Kullanım

### 1. Model Yükleme

#### Web Arayüzünde:

1. **Model** sekmesine git
2. **Unload** butonu ile mevcut modeli kaldır (eğer yüklüyse)
3. Model dropdown'dan **meta-llama_Llama-3.2-1B-Instruct** seç
4. **Load** butonuna tıkla
5. **LoRA(s)** bölümüne in
6. Dropdown'dan **llama1b-a1** seç
7. **Apply LoRAs** butonuna tıkla
8. "Successfully loaded" mesajını bekle

### 2. Test Etme

#### Chat Sekmesinde:

**Doğru Prompt Formatı:**
```
Generate A1-level English sentences for these 10 words:
1. age
2. animal
3. ask
4. computer
5. eat
6. car
7. but
8. drive
9. amazing
10. funny

Provide numbered sentences (1-10), using each word naturally and appropriately for A1 level.
```

**Beklenen Çıktı:**
```
1. My grandmother is 80 years old.
2. I like animals.
3. Can I ask a question?
4. I use my computer for homework.
5. I eat breakfast every morning.
6. My father has a red car.
7. I like pizza, but I don't like vegetables.
8. I can drive a car.
9. The sunset is amazing.
10. That movie was very funny.
```

### 3. Farklı Kelime Sayıları İçin

Model 6-10 kelime arası esnek çalışır:

**6 kelime örneği:**
```
Generate A1-level English sentences for these 6 words:
1. happy
2. book
3. friend
4. water
5. school
6. play

Provide numbered sentences (1-6), using each word naturally and appropriately for A1 level.
```

---

## 📝 Önemli Notlar

### ✅ Başarılı Olan Şeyler

1. **Hibrit veri stratejisi** - %70 10-kelime, %30 varyasyon
2. **Numaralı liste formatı** - Model yapıyı öğrendi
3. **LoRA rank 128** - Yeterince kapasiteli ama hafif
4. **3 epoch** - Overfitting olmadan öğrendi

### ⚠️ Dikkat Edilmesi Gerekenler

1. **Model formatı önemli**: GGUF değil, Transformers formatı gerekli
2. **Prompt tutarlılığı**: Eğitim ve test prompt'ları aynı formatta olmalı
3. **LoRA yükleme**: Eğitim sonrası mutlaka model reload et
4. **API güncellemeleri**: Training PRO script'i bazen güncelleme gerektirebilir

### 🔄 Gelecekte Tekrar Eğitim İçin

**Hızlı Başlangıç:**

```bash
# 1. Veriyi hazırla
cd /home/user/Documents/Tez/Deneyler/LLM_Degerlendirme/notebooks/fine_tuning
python3 create_list_format_training_data.py

# 2. Kopyala
cp training_data_a1_list_format.txt \
  /home/user/text-generation-webui/user_data/training/datasets/

# 3. Web arayüzünde:
# - Model yükle (base model)
# - Training PRO sekmesi
# - Dataset seç
# - Parametreleri ayarla (yukarıdaki tabloya bak)
# - Start LoRA Training
```

---

## 🐛 Sorun Giderme

### Hata: "evaluation_strategy" deprecated
```bash
sed -i 's/evaluation_strategy=/eval_strategy=/g' \
  /home/user/text-generation-webui/extensions/Training_PRO/script.py
```

### Hata: Dataset görünmüyor
```bash
# Doğru klasöre kopyala
cp *.txt /home/user/text-generation-webui/user_data/training/datasets/

# Web arayüzünü yenile (F5)
```

### Hata: Model dirty after training
```
# Model sekmesinde:
1. Unload butonu
2. Load butonu
3. LoRA'yı tekrar yükle
```

---

## 📚 Referanslar

- **Base Model:** https://huggingface.co/meta-llama/Llama-3.2-1B-Instruct
- **text-generation-webui:** https://github.com/oobabooga/text-generation-webui
- **LoRA Paper:** https://arxiv.org/abs/2106.09685

---

## 📊 Veri Setleri

### Kaynak Veri
- `training_data_a1.json` - 4490 entry, 897 kelime

### Oluşturulan Veriler
- `training_data_a1_list_format.json` - 2000 örnek (JSON)
- `training_data_a1_list_format.txt` - 2000 örnek (Text format)

### Scripter
- `create_list_format_training_data.py` - Veri oluşturma scripti
- `convert_to_txt.py` - JSON → TXT dönüştürme
- `convert_to_webui_format.py` - WebUI format dönüştürme

---

**Son Güncelleme:** 18 Ekim 2025  
**Durum:** ✅ Başarılı - Model eğitildi ve test edildi  
**Sonraki Adımlar:** Farklı seviyelerde (A2, B1, B2, C1) aynı süreci tekrarla

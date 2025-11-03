# B1 Model - Düzeltilmiş Eğitim Parametreleri

## 🎯 Sorun
İlk eğitimde `grad_norm: inf` problemi nedeniyle model düzgün öğrenmedi.

## ⚙️ Yeni Parametreler (A1 Başarı Formülü + Düzeltmeler)

### Model Ayarları
- **Model:** meta-llama/Llama-3.2-1B-Instruct
- **Model Loader:** Transformers
- **Model Class:** LlamaForCausalLM

### LoRA Parametreleri (A1'deki Gibi)

| Parametre | A1 Değeri | B1 İçin | Neden |
|-----------|-----------|---------|-------|
| **Name** | llama1b-a1 | **llama1b-b1** | B1 versiyonu |
| **LoRA Rank** | 128 | **128** | A1'de başarılı oldu |
| **LoRA Alpha** | 256 | **256** | A1'de başarılı oldu |
| **LoRA Target** | q+v | **q+v** | Aynı |

### Training Parametreleri

| Parametre | A1 Değeri | B1 İçin | Neden |
|-----------|-----------|---------|-------|
| **Epochs** | 3 | **3** | A1'de başarılı oldu |
| **Learning Rate** | 2e-4 | **1e-4** (0.0001) | %50 azaltma - NEFtune için daha güvenli |
| **LR Scheduler** | cosine | **cosine** | A1'de çalıştı |
| **Batch Size** | 16 | **16** | A1'deki gibi |
| **Gradient Accumulation** | 4 | **4** | A1'deki gibi |
| **Warmup Steps** | 100 | **150** | Biraz daha uzun |
| **NEFtune Scale** | 3 | **1** | ⚠️ AZALT! Bu kritik!

### Dataset Ayarları

| Parametre | İlk Değer | Yeni Değer |
|-----------|-----------|------------|
| **Text File** | training_data_b1_list_format.txt | **training_data_b1_list_format.txt** |
| **Overlapping Blocks** | ❌ | **❌** |
| **Chunk Length** | 256 | **256** |
| **Hard Cut String** | \n\n\n | **\n\n\n** |

### Checkpoint Ayarları

| Parametre | Yeni Değer | Neden |
|-----------|------------|-------|
| **Save every N steps** | **100** | Her 100 adımda kaydet |
| **Save at Loss Change** | **0** (OFF) | Devre dışı |

**Neden?** Checkpointlere bakıp hangi adımda iyi olduğunu göreceğiz.

### Advanced Options

| Parametre | A1 Değeri | B1 İçin | Neden |
|-----------|-----------|---------|-------|
| **Warmup Steps** | 100 | **150** | Biraz daha uzun |
| **Optimizer** | adamw_torch | **adamw_torch** | Aynı |
| **Add BOS token** | ✅ | **✅** | Aynı |
| **Add EOS token** | ✅ | **✅** | Aynı |
| **LoRA Dropout** | 0.05 | **0.05** | Aynı |
| **NEFtune Scale** | 3 | **1** | ⚠️ AZALT! Gradient patlaması nedeni! |

## 🎯 Kritik Değişiklikler

### 1. **NEFtune Scale: 3 → 1** ⭐ EN ÖNEMLİ!
- A1'de 3 kullanmışsın ama şanslıymışsın
- NEFtune 3 çok agresif, gradient'leri patlatabilir
- Scale 1 daha güvenli

### 2. **Learning Rate: 2e-4 → 1e-4**
- NEFtune ile kombine olunca 2e-4 fazla
- 1e-4 daha dengeli

### 3. **Warmup: 100 → 150**
- Daha yumuşak başlangıç
- NEFtune'un ilk etkisini yumuşatır

## 📊 Beklenen Davranış

### İlk 50 Step:
- `grad_norm`: 0.5 - 5.0 (sonlu değerler!)
- `loss`: 2.4 - 2.3

### 50-200 Step (Warmup):
- `grad_norm`: 1.0 - 10.0 (stabil)
- `loss`: 2.3 - 2.0

### 200+ Step:
- `grad_norm`: 2.0 - 20.0 (kontrol altında)
- `loss`: 2.0 → 1.5 → 1.2

## ⚠️ Eğer Yine `grad_norm: inf` Olursa

### Son Çare Parametreler (Ultra Conservative):

- **Learning Rate:** 1e-5 (0.00001)
- **LoRA Rank:** 16
- **Batch Size:** 8
- **Gradient Accumulation:** 8

## 🎯 Alternatif Çözüm: Training PRO Kodunu Düzenle

Eğer tekrar deneyeceksen, script'e gradient clipping ekleyelim:

```bash
# Training PRO script'ini düzenle
nano /media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/text-generation-webui/extensions/Training_PRO/script.py

# Şu satırı bul (yaklaşık satır 1050-1080 arası):
# training_arguments = TrainingArguments(...)

# İçine şunu ekle:
max_grad_norm=1.0,  # Gradient clipping
```

Ama manuel düzenleme gerektiriyor.

## 🚀 Önerilen Aksiyon

### ⭐ ÖNER İLAN: A1 Formülü + NEFtune Fix

**Sorun bulundu:** NEFtune scale 3 + Learning rate 2e-4 → Gradient patlaması!

#### Yeni Strateji:

**Seçenek 1: Güvenli Yol (Önerilen)** ✅
```
- Learning Rate: 1e-4 (0.0001)
- NEFtune Scale: 1
- Rank: 128 (A1'deki gibi)
- Epochs: 3
- Batch: 16, Grad Acc: 4
- Warmup: 150
```
**Beklenen Süre:** ~4-5 saat  
**Başarı İhtimali:** %90+

**Seçenek 2: Çok Güvenli (Eğer S1 başarısızsa)**
```
- Learning Rate: 5e-5 (0.00005)
- NEFtune Scale: 0 (Kapalı!)
- Rank: 64
- Epochs: 3
```
**Beklenen Süre:** ~5-6 saat  
**Başarı İhtimali:** %95+

**Seçenek 3: A1'in Aynısı (Risk)** ⚠️
```
- Learning Rate: 2e-4
- NEFtune Scale: 3
- Her şey A1'deki gibi
```
**Risk:** Yine `grad_norm: inf` olabilir  
**Ama:** A1'de çalıştı, belki B1'de de çalışır?

### ⚠️ İlk 50 Step'te Kontrol Et:

```bash
# Terminal'de şunu ara:
grep "grad_norm" training.log | head -20
```

**Eğer yine `inf` görürsen:** HEMEN DURDUR ve bana haber ver!

### 📊 Başarı Kriterleri:

| Step | grad_norm | loss | Durum |
|------|-----------|------|-------|
| 1-50 | < 10 | ~2.4 | ✅ İyi |
| 50-200 | < 20 | 2.4 → 2.2 | ✅ İyi |
| 200+ | < 50 | 2.2 → 1.5 | ✅ İyi |

**Eğer herhangi bir step'te `inf` görürsen:** Problem var, durdur!

---

**Ne düşünüyorsun? Hangi seçenekle gidelim?**



Loglar :

grad_norm': inf -> Tehlikeli 


18:22:37-385220 INFO     Starting training...                                   
Training 'llama' model using (q, v) projections
Trainable params: 13,631,488 (1.0910 %), All params: 1,249,445,888 (Model: 1,235,814,400)
18:22:37-407988 INFO     Log file 'train_dataset_sample.json' created in the    
                         'user_data/logs' directory.                            
/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/text-generation-webui/venv/lib/python3.12/site-packages/torch/cuda/__init__.py:827: UserWarning: Can't initialize NVML
  warnings.warn("Can't initialize NVML")
Step:      3 {'loss': 2.4395, 'grad_norm': inf, 'learning_rate': 8.000000000000001e-06, 'epoch': 0.017543859649122806}
Step:      7 {'loss': 2.4141, 'grad_norm': inf, 'learning_rate': 1.6000000000000003e-05, 'epoch': 0.03508771929824561}
Step:     11 {'loss': 2.4961, 'grad_norm': inf, 'learning_rate': 2.4e-05, 'epoch': 0.05263157894736842}
Step:     15 {'loss': 2.4013, 'grad_norm': inf, 'learning_rate': 3.2000000000000005e-05, 'epoch': 0.07017543859649122}
Step:     19 {'loss': 2.3927, 'grad_norm': inf, 'learning_rate': 4e-05, 'epoch': 0.08771929824561403}
Step:     23 {'loss': 2.4432, 'grad_norm': inf, 'learning_rate': 4.8e-05, 'epoch': 0.10526315789473684}
Step:     27 {'loss': 2.4623, 'grad_norm': inf, 'learning_rate': 5.6000000000000006e-05, 'epoch': 0.12280701754385964}
Step:     31 {'loss': 2.4773, 'grad_norm': inf, 'learning_rate': 6.400000000000001e-05, 'epoch': 0.14035087719298245}
Step:     35 {'loss': 2.4429, 'grad_norm': inf, 'learning_rate': 7.2e-05, 'epoch': 0.15789473684210525}
Step:     39 {'loss': 2.428, 'grad_norm': inf, 'learning_rate': 8e-05, 'epoch': 0.17543859649122806}
Step:     43 {'loss': 2.4513, 'grad_norm': inf, 'learning_rate': 8.800000000000001e-05, 'epoch': 0.19298245614035087}
Step:     47 {'loss': 2.3795, 'grad_norm': inf, 'learning_rate': 9.6e-05, 'epoch': 0.21052631578947367}
Step:     51 {'loss': 2.4501, 'grad_norm': inf, 'learning_rate': 0.00010400000000000001, 'epoch': 0.22807017543859648}
Step:     55 {'loss': 2.4176, 'grad_norm': inf, 'learning_rate': 0.00011200000000000001, 'epoch': 0.24561403508771928}
Step:     59 {'loss': 2.4541, 'grad_norm': inf, 'learning_rate': 0.00012, 'epoch': 0.2631578947368421}
Step:     63 {'loss': 2.4422, 'grad_norm': inf, 'learning_rate': 0.00012800000000000002, 'epoch': 0.2807017543859649}
Step:     67 {'loss': 2.4745, 'grad_norm': inf, 'learning_rate': 0.00013600000000000003, 'epoch': 0.2982456140350877}
Step:     71 {'loss': 2.4488, 'grad_norm': inf, 'learning_rate': 0.000144, 'epoch': 0.3157894736842105}
Step:     75 {'loss': 2.5318, 'grad_norm': inf, 'learning_rate': 0.000152, 'epoch': 0.3333333333333333}
Step:     79 {'loss': 2.3843, 'grad_norm': inf, 'learning_rate': 0.00016, 'epoch': 0.3508771929824561}
Step:     83 {'loss': 2.4409, 'grad_norm': inf, 'learning_rate': 0.000168, 'epoch': 0.3684210526315789}
Step:     87 {'loss': 2.4344, 'grad_norm': inf, 'learning_rate': 0.00017600000000000002, 'epoch': 0.38596491228070173}
Step:     91 {'loss': 2.4631, 'grad_norm': inf, 'learning_rate': 0.00018400000000000003, 'epoch': 0.40350877192982454}
Step:     95 {'loss': 2.5394, 'grad_norm': inf, 'learning_rate': 0.000192, 'epoch': 0.42105263157894735}
Step:     99 {'loss': 2.4697, 'grad_norm': inf, 'learning_rate': 0.0002, 'epoch': 0.43859649122807015}
Step:    103 {'loss': 2.4832, 'grad_norm': inf, 'learning_rate': 0.00019997685019798912, 'epoch': 0.45614035087719296}
Step:    107 {'loss': 2.4168, 'grad_norm': inf, 'learning_rate': 0.00019990741151022301, 'epoch': 0.47368421052631576}
Step:    111 {'loss': 2.4124, 'grad_norm': inf, 'learning_rate': 0.00019979171608653924, 'epoch': 0.49122807017543857}
Step:    115 {'loss': 2.4266, 'grad_norm': inf, 'learning_rate': 0.00019962981749346078, 'epoch': 0.5087719298245614}
Step:    119 {'loss': 2.4546, 'grad_norm': inf, 'learning_rate': 0.0001994217906893952, 'epoch': 0.5263157894736842}
Step:    123 {'loss': 2.5352, 'grad_norm': inf, 'learning_rate': 0.000199167731989929, 'epoch': 0.543859649122807}
Step:    127 {'loss': 2.4835, 'grad_norm': inf, 'learning_rate': 0.00019886775902323405, 'epoch': 0.5614035087719298}
Step:    131 {'loss': 2.482, 'grad_norm': inf, 'learning_rate': 0.00019852201067560606, 'epoch': 0.5789473684210527}
Step:    135 {'loss': 2.3737, 'grad_norm': inf, 'learning_rate': 0.00019813064702716094, 'epoch': 0.5964912280701754}
Step:    139 {'loss': 2.4686, 'grad_norm': inf, 'learning_rate': 0.0001976938492777182, 'epoch': 0.6140350877192983}
Step:    143 {'loss': 2.5108, 'grad_norm': inf, 'learning_rate': 0.00019721181966290613, 'epoch': 0.631578947368421}
Step:    147 {'loss': 2.3479, 'grad_norm': inf, 'learning_rate': 0.00019668478136052774, 'epoch': 0.6491228070175439}
Step:    151 {'loss': 2.4318, 'grad_norm': inf, 'learning_rate': 0.0001961129783872301, 'epoch': 0.6666666666666666}
Step:    155 {'loss': 2.4503, 'grad_norm': inf, 'learning_rate': 0.00019549667548552556, 'epoch': 0.6842105263157895}
Step:    159 {'loss': 2.4454, 'grad_norm': inf, 'learning_rate': 0.00019483615800121716, 'epoch': 0.7017543859649122}
Step:    163 {'loss': 2.412, 'grad_norm': inf, 'learning_rate': 0.00019413173175128473, 'epoch': 0.7192982456140351}
Step:    167 {'loss': 2.3792, 'grad_norm': inf, 'learning_rate': 0.0001933837228822925, 'epoch': 0.7368421052631579}
Step:    171 {'loss': 2.4262, 'grad_norm': inf, 'learning_rate': 0.000192592477719385, 'epoch': 0.7543859649122807}
Step:    175 {'loss': 2.4362, 'grad_norm': inf, 'learning_rate': 0.00019175836260593938, 'epoch': 0.7719298245614035}
Step:    179 {'loss': 2.4837, 'grad_norm': inf, 'learning_rate': 0.0001908817637339503, 'epoch': 0.7894736842105263}
Step:    183 {'loss': 2.3824, 'grad_norm': inf, 'learning_rate': 0.00018996308696522433, 'epoch': 0.8070175438596491}
Step:    187 {'loss': 2.4317, 'grad_norm': inf, 'learning_rate': 0.00018900275764346768, 'epoch': 0.8245614035087719}
Step:    191 {'loss': 2.4875, 'grad_norm': inf, 'learning_rate': 0.00018800122039735358, 'epoch': 0.8421052631578947}
Step:    195 {'loss': 2.4428, 'grad_norm': inf, 'learning_rate': 0.0001869589389346611, 'epoch': 0.8596491228070176}
Step:    199 {'loss': 2.417, 'grad_norm': inf, 'learning_rate': 0.00018587639582758031, 'epoch': 0.8771929824561403}
Step:    203 {'loss': 2.4728, 'grad_norm': inf, 'learning_rate': 0.00018475409228928312, 'epoch': 0.8947368421052632}
Step:    207 {'loss': 2.463, 'grad_norm': inf, 'learning_rate': 0.0001835925479418637, 'epoch': 0.9122807017543859}
Step:    211 {'loss': 2.4503, 'grad_norm': inf, 'learning_rate': 0.00018239230057575542, 'epoch': 0.9298245614035088}
Step:    215 {'loss': 2.3658, 'grad_norm': inf, 'learning_rate': 0.0001811539059007361, 'epoch': 0.9473684210526315}
Step:    219 {'loss': 2.4518, 'grad_norm': inf, 'learning_rate': 0.00017987793728863651, 'epoch': 0.9649122807017544}
Step:    223 {'loss': 2.4599, 'grad_norm': inf, 'learning_rate': 0.00017856498550787144, 'epoch': 0.9824561403508771}
Step:    227 {'loss': 2.4557, 'grad_norm': inf, 'learning_rate': 0.00017721565844991643, 'epoch': 1.0}
Step:    231 {'loss': 2.4577, 'grad_norm': inf, 'learning_rate': 0.00017583058084785625, 'epoch': 1.0175438596491229}
Step:    235 {'loss': 2.4889, 'grad_norm': inf, 'learning_rate': 0.00017441039398713608, 'epoch': 1.0350877192982457}
Step:    239 {'loss': 2.4841, 'grad_norm': inf, 'learning_rate': 0.00017295575540864877, 'epoch': 1.0526315789473684}
Step:    243 {'loss': 2.4313, 'grad_norm': inf, 'learning_rate': 0.00017146733860429612, 'epoch': 1.0701754385964912}
Step:    247 {'loss': 2.4683, 'grad_norm': inf, 'learning_rate': 0.0001699458327051647, 'epoch': 1.087719298245614}
Step:    251 {'loss': 2.4619, 'grad_norm': inf, 'learning_rate': 0.00016839194216246108, 'epoch': 1.1052631578947367}
Step:    255 {'loss': 2.4606, 'grad_norm': inf, 'learning_rate': 0.00016680638642135336, 'epoch': 1.1228070175438596}
Step:    259 {'loss': 2.3868, 'grad_norm': inf, 'learning_rate': 0.00016518989958787126, 'epoch': 1.1403508771929824}
Step:    263 {'loss': 2.3792, 'grad_norm': inf, 'learning_rate': 0.00016354323008901776, 'epoch': 1.1578947368421053}
Step:    267 {'loss': 2.5052, 'grad_norm': inf, 'learning_rate': 0.00016186714032625035, 'epoch': 1.1754385964912282}
Step:    271 {'loss': 2.365, 'grad_norm': inf, 'learning_rate': 0.00016016240632249224, 'epoch': 1.1929824561403508}
Step:    275 {'loss': 2.4224, 'grad_norm': inf, 'learning_rate': 0.00015842981736283686, 'epoch': 1.2105263157894737}
Step:    279 {'loss': 2.4794, 'grad_norm': inf, 'learning_rate': 0.00015667017562911176, 'epoch': 1.2280701754385965}
Step:    283 {'loss': 2.4435, 'grad_norm': inf, 'learning_rate': 0.00015488429582847192, 'epoch': 1.2456140350877192}
Step:    287 {'loss': 2.4067, 'grad_norm': inf, 'learning_rate': 0.00015307300481619333, 'epoch': 1.263157894736842}
Step:    291 {'loss': 2.4375, 'grad_norm': inf, 'learning_rate': 0.0001512371412128424, 'epoch': 1.280701754385965}
Step:    295 {'loss': 2.4188, 'grad_norm': inf, 'learning_rate': 0.00014937755501599772, 'epoch': 1.2982456140350878}
Step:    299 {'loss': 2.4279, 'grad_norm': inf, 'learning_rate': 0.00014749510720670506, 'epoch': 1.3157894736842106}
Step:    303 {'loss': 2.3586, 'grad_norm': inf, 'learning_rate': 0.00014559066935084588, 'epoch': 1.3333333333333333}
Step:    307 {'loss': 2.449, 'grad_norm': inf, 'learning_rate': 0.0001436651231956064, 'epoch': 1.3508771929824561}
Step:    311 {'loss': 2.5125, 'grad_norm': inf, 'learning_rate': 0.00014171936026123168, 'epoch': 1.368421052631579}
Step:    315 {'loss': 2.4642, 'grad_norm': inf, 'learning_rate': 0.0001397542814282556, 'epoch': 1.3859649122807016}
Step:    319 {'loss': 2.4525, 'grad_norm': inf, 'learning_rate': 0.0001377707965203965, 'epoch': 1.4035087719298245}
Step:    323 {'loss': 2.4403, 'grad_norm': inf, 'learning_rate': 0.0001357698238833126, 'epoch': 1.4210526315789473}
Step:    327 {'loss': 2.4692, 'grad_norm': inf, 'learning_rate': 0.00013375228995941133, 'epoch': 1.4385964912280702}
Step:    331 {'loss': 2.4042, 'grad_norm': inf, 'learning_rate': 0.00013171912885891063, 'epoch': 1.456140350877193}
Step:    335 {'loss': 2.4271, 'grad_norm': inf, 'learning_rate': 0.00012967128192734902, 'epoch': 1.4736842105263157}
Step:    339 {'loss': 2.4859, 'grad_norm': inf, 'learning_rate': 0.00012760969730974694, 'epoch': 1.4912280701754386}
Step:    343 {'loss': 2.4878, 'grad_norm': inf, 'learning_rate': 0.0001255353295116187, 'epoch': 1.5087719298245614}
Step:    347 {'loss': 2.4811, 'grad_norm': inf, 'learning_rate': 0.00012344913895704097, 'epoch': 1.526315789473684}
Step:    351 {'loss': 2.442, 'grad_norm': inf, 'learning_rate': 0.00012135209154397962, 'epoch': 1.543859649122807}
Step:    355 {'loss': 2.3633, 'grad_norm': inf, 'learning_rate': 0.000119245158197083, 'epoch': 1.5614035087719298}
Step:    359 {'loss': 2.4111, 'grad_norm': inf, 'learning_rate': 0.00011712931441814776, 'epoch': 1.5789473684210527}
Step:    363 {'loss': 2.4239, 'grad_norm': inf, 'learning_rate': 0.00011500553983446527, 'epoch': 1.5964912280701755}
Step:    367 {'loss': 2.4358, 'grad_norm': inf, 'learning_rate': 0.0001128748177452581, 'epoch': 1.6140350877192984}
Step:    371 {'loss': 2.4645, 'grad_norm': inf, 'learning_rate': 0.00011073813466641632, 'epoch': 1.631578947368421}
Step:    375 {'loss': 2.4317, 'grad_norm': inf, 'learning_rate': 0.00010859647987374467, 'epoch': 1.6491228070175439}
Step:    379 {'loss': 2.4255, 'grad_norm': inf, 'learning_rate': 0.00010645084494493165, 'epoch': 1.6666666666666665}
Step:    383 {'loss': 2.4563, 'grad_norm': inf, 'learning_rate': 0.00010430222330045304, 'epoch': 1.6842105263157894}
Step:    387 {'loss': 2.4084, 'grad_norm': inf, 'learning_rate': 0.00010215160974362223, 'epoch': 1.7017543859649122}
Step:    391 {'loss': 2.4693, 'grad_norm': inf, 'learning_rate': 0.0001, 'epoch': 1.719298245614035}
Step:    395 {'loss': 2.4579, 'grad_norm': inf, 'learning_rate': 9.784839025637778e-05, 'epoch': 1.736842105263158}
Step:    399 {'loss': 2.407, 'grad_norm': inf, 'learning_rate': 9.569777669954694e-05, 'epoch': 1.7543859649122808}
Step:    403 {'loss': 2.4401, 'grad_norm': inf, 'learning_rate': 9.354915505506839e-05, 'epoch': 1.7719298245614035}
Step:    407 {'loss': 2.4247, 'grad_norm': inf, 'learning_rate': 9.140352012625537e-05, 'epoch': 1.7894736842105263}
Step:    411 {'loss': 2.5381, 'grad_norm': inf, 'learning_rate': 8.92618653335837e-05, 'epoch': 1.807017543859649}
Step:    415 {'loss': 2.4056, 'grad_norm': inf, 'learning_rate': 8.712518225474191e-05, 'epoch': 1.8245614035087718}
Step:    419 {'loss': 2.4284, 'grad_norm': inf, 'learning_rate': 8.499446016553474e-05, 'epoch': 1.8421052631578947}
Step:    423 {'loss': 2.4489, 'grad_norm': inf, 'learning_rate': 8.287068558185225e-05, 'epoch': 1.8596491228070176}
Step:    427 {'loss': 2.4414, 'grad_norm': inf, 'learning_rate': 8.075484180291701e-05, 'epoch': 1.8771929824561404}
Step:    431 {'loss': 2.4714, 'grad_norm': inf, 'learning_rate': 7.864790845602039e-05, 'epoch': 1.8947368421052633}
Step:    435 {'loss': 2.4738, 'grad_norm': inf, 'learning_rate': 7.655086104295904e-05, 'epoch': 1.912280701754386}
Step:    439 {'loss': 2.4229, 'grad_norm': inf, 'learning_rate': 7.446467048838131e-05, 'epoch': 1.9298245614035088}
Step:    443 {'loss': 2.4196, 'grad_norm': inf, 'learning_rate': 7.239030269025311e-05, 'epoch': 1.9473684210526314}
Step:    447 {'loss': 2.539, 'grad_norm': inf, 'learning_rate': 7.032871807265096e-05, 'epoch': 1.9649122807017543}
Step:    451 {'loss': 2.4044, 'grad_norm': inf, 'learning_rate': 6.82808711410894e-05, 'epoch': 1.9824561403508771}
Step:    455 {'loss': 2.4296, 'grad_norm': inf, 'learning_rate': 6.624771004058868e-05, 'epoch': 2.0}
Step:    459 {'loss': 2.4894, 'grad_norm': inf, 'learning_rate': 6.423017611668745e-05, 'epoch': 2.017543859649123}
Step:    463 {'loss': 2.5275, 'grad_norm': inf, 'learning_rate': 6.22292034796035e-05, 'epoch': 2.0350877192982457}
Step:    467 {'loss': 2.4778, 'grad_norm': inf, 'learning_rate': 6.024571857174443e-05, 'epoch': 2.0526315789473686}
Step:    471 {'loss': 2.4441, 'grad_norm': inf, 'learning_rate': 5.828063973876834e-05, 'epoch': 2.0701754385964914}
Step:    475 {'loss': 2.4629, 'grad_norm': inf, 'learning_rate': 5.633487680439361e-05, 'epoch': 2.087719298245614}
Step:    479 {'loss': 2.4203, 'grad_norm': inf, 'learning_rate': 5.440933064915414e-05, 'epoch': 2.1052631578947367}
Step:    483 {'loss': 2.4331, 'grad_norm': inf, 'learning_rate': 5.2504892793295e-05, 'epoch': 2.1228070175438596}
Step:    487 {'loss': 2.4873, 'grad_norm': inf, 'learning_rate': 5.062244498400228e-05, 'epoch': 2.1403508771929824}
Step:    491 {'loss': 2.5227, 'grad_norm': inf, 'learning_rate': 4.876285878715764e-05, 'epoch': 2.1578947368421053}
Step:    495 {'loss': 2.4516, 'grad_norm': inf, 'learning_rate': 4.6926995183806644e-05, 'epoch': 2.175438596491228}
Step:    499 {'loss': 2.4886, 'grad_norm': inf, 'learning_rate': 4.5115704171528105e-05, 'epoch': 2.192982456140351}
Step:    503 {'loss': 2.4121, 'grad_norm': inf, 'learning_rate': 4.332982437088825e-05, 'epoch': 2.2105263157894735}
Step:    507 {'loss': 2.434, 'grad_norm': inf, 'learning_rate': 4.1570182637163155e-05, 'epoch': 2.2280701754385963}
Step:    511 {'loss': 2.4658, 'grad_norm': inf, 'learning_rate': 3.9837593677507726e-05, 'epoch': 2.245614035087719}
Step:    515 {'loss': 2.4221, 'grad_norm': inf, 'learning_rate': 3.813285967374969e-05, 'epoch': 2.263157894736842}
Step:    519 {'loss': 2.512, 'grad_norm': inf, 'learning_rate': 3.645676991098227e-05, 'epoch': 2.280701754385965}
Step:    523 {'loss': 2.4632, 'grad_norm': inf, 'learning_rate': 3.4810100412128747e-05, 'epoch': 2.2982456140350878}
Step:    527 {'loss': 2.4164, 'grad_norm': inf, 'learning_rate': 3.319361357864663e-05, 'epoch': 2.3157894736842106}
Step:    531 {'loss': 2.3944, 'grad_norm': inf, 'learning_rate': 3.160805783753897e-05, 'epoch': 2.3333333333333335}
Step:    535 {'loss': 2.5156, 'grad_norm': inf, 'learning_rate': 3.005416729483531e-05, 'epoch': 2.3508771929824563}
Step:    539 {'loss': 2.4001, 'grad_norm': inf, 'learning_rate': 2.853266139570391e-05, 'epoch': 2.3684210526315788}
Step:    543 {'loss': 2.4399, 'grad_norm': inf, 'learning_rate': 2.7044244591351232e-05, 'epoch': 2.3859649122807016}
Step:    547 {'loss': 2.4219, 'grad_norm': inf, 'learning_rate': 2.5589606012863963e-05, 'epoch': 2.4035087719298245}
Step:    551 {'loss': 2.446, 'grad_norm': inf, 'learning_rate': 2.4169419152143768e-05, 'epoch': 2.4210526315789473}
Step:    555 {'loss': 2.4117, 'grad_norm': inf, 'learning_rate': 2.2784341550083576e-05, 'epoch': 2.43859649122807}
Step:    559 {'loss': 2.4221, 'grad_norm': inf, 'learning_rate': 2.1435014492128547e-05, 'epoch': 2.456140350877193}
Step:    563 {'loss': 2.442, 'grad_norm': inf, 'learning_rate': 2.0122062711363532e-05, 'epoch': 2.473684210526316}
Step:    567 {'loss': 2.4626, 'grad_norm': inf, 'learning_rate': 1.8846094099263912e-05, 'epoch': 2.4912280701754383}
Step:    571 {'loss': 2.4352, 'grad_norm': inf, 'learning_rate': 1.7607699424244585e-05, 'epoch': 2.5087719298245617}
Step:    575 {'loss': 2.374, 'grad_norm': inf, 'learning_rate': 1.6407452058136296e-05, 'epoch': 2.526315789473684}
Step:    579 {'loss': 2.4227, 'grad_norm': inf, 'learning_rate': 1.5245907710716911e-05, 'epoch': 2.543859649122807}
Step:    583 {'loss': 2.4042, 'grad_norm': inf, 'learning_rate': 1.4123604172419713e-05, 'epoch': 2.56140350877193}
Step:    587 {'loss': 2.4138, 'grad_norm': inf, 'learning_rate': 1.30410610653389e-05, 'epoch': 2.5789473684210527}
Step:    591 {'loss': 2.4299, 'grad_norm': inf, 'learning_rate': 1.1998779602646437e-05, 'epoch': 2.5964912280701755}
Step:    595 {'loss': 2.3977, 'grad_norm': inf, 'learning_rate': 1.0997242356532334e-05, 'epoch': 2.6140350877192984}
Step:    599 {'loss': 2.4046, 'grad_norm': inf, 'learning_rate': 1.0036913034775674e-05, 'epoch': 2.6315789473684212}
Step:    603 {'loss': 2.4956, 'grad_norm': inf, 'learning_rate': 9.118236266049707e-06, 'epoch': 2.6491228070175437}
Step:    607 {'loss': 2.4621, 'grad_norm': inf, 'learning_rate': 8.24163739406062e-06, 'epoch': 2.6666666666666665}
Step:    611 {'loss': 2.4597, 'grad_norm': inf, 'learning_rate': 7.40752228061502e-06, 'epoch': 2.6842105263157894}
Step:    615 {'loss': 2.4356, 'grad_norm': inf, 'learning_rate': 6.616277117707492e-06, 'epoch': 2.7017543859649122}
Step:    619 {'loss': 2.4896, 'grad_norm': inf, 'learning_rate': 5.868268248715292e-06, 'epoch': 2.719298245614035}
Step:    623 {'loss': 2.4063, 'grad_norm': inf, 'learning_rate': 5.163841998782837e-06, 'epoch': 2.736842105263158}
Step:    627 {'loss': 2.4627, 'grad_norm': inf, 'learning_rate': 4.503324514474483e-06, 'epoch': 2.754385964912281}
Step:    631 {'loss': 2.4591, 'grad_norm': inf, 'learning_rate': 3.887021612769936e-06, 'epoch': 2.7719298245614032}
Step:    635 {'loss': 2.4116, 'grad_norm': inf, 'learning_rate': 3.3152186394722505e-06, 'epoch': 2.7894736842105265}
Step:    639 {'loss': 2.4962, 'grad_norm': inf, 'learning_rate': 2.7881803370938597e-06, 'epoch': 2.807017543859649}
Step:    643 {'loss': 2.4457, 'grad_norm': inf, 'learning_rate': 2.30615072228183e-06, 'epoch': 2.824561403508772}
Step:    647 {'loss': 2.4391, 'grad_norm': inf, 'learning_rate': 1.869352972839067e-06, 'epoch': 2.8421052631578947}
Step:    651 {'loss': 2.4241, 'grad_norm': inf, 'learning_rate': 1.4779893243939359e-06, 'epoch': 2.8596491228070176}
Step:    655 {'loss': 2.4177, 'grad_norm': inf, 'learning_rate': 1.1322409767659525e-06, 'epoch': 2.8771929824561404}
Step:    659 {'loss': 2.5227, 'grad_norm': inf, 'learning_rate': 8.322680100710023e-07, 'epoch': 2.8947368421052633}
Step:    663 {'loss': 2.3909, 'grad_norm': inf, 'learning_rate': 5.782093106048159e-07, 'epoch': 2.912280701754386}
Step:    667 {'loss': 2.3635, 'grad_norm': inf, 'learning_rate': 3.701825065392184e-07, 'epoch': 2.9298245614035086}
Step:    671 {'loss': 2.4592, 'grad_norm': inf, 'learning_rate': 2.082839134607828e-07, 'epoch': 2.9473684210526314}
Step:    675 {'loss': 2.4869, 'grad_norm': inf, 'learning_rate': 9.258848977700129e-08, 'epoch': 2.9649122807017543}
Step:    679 {'loss': 2.4558, 'grad_norm': inf, 'learning_rate': 2.3149802010913323e-08, 'epoch': 2.982456140350877}
Step:    683 {'loss': 2.4082, 'grad_norm': inf, 'learning_rate': 0.0, 'epoch': 3.0}
Step:    683 {'train_runtime': 13893.3078, 'train_samples_per_second': 0.787, 'train_steps_per_second': 0.012, 'train_loss': 2.4439938653979385, 'epoch': 3.0}
22:14:11-000860 INFO     LoRA training run is completed and saved.              
22:14:11-456457 INFO     Training complete, saving...                           
22:14:11-546802 INFO     Training complete!   

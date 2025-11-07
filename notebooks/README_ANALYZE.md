# Analiz Scripti Kullanım Kılavuzu

## 🎯 Genel Bakış

`analyze_results.py` scripti, grup bazlı LLM değerlendirme sonuçlarını analiz eder, CSV tabloları ve performans grafikleri oluşturur.

**Yeni Özellik:** Artık her seviye için sonuçlar ayrı klasörlerde organize edilir! 📁

## 🚀 Hızlı Başlangıç

### Temel Kullanım (Her seviye ayrı)

```bash
# ChatGPT sonuçlarını analiz et - Her seviye kendi klasöründe
python analyze_results.py --evaluator chatgpt_ratings --group 1

# DeepSeek sonuçlarını analiz et - Her seviye kendi klasöründe
python analyze_results.py --evaluator deepseek_ratings --group 1
```

### Birleşik Mod (Tüm seviyeler birlikte)

```bash
# Eski davranış: Tüm seviyeler tek klasörde
python analyze_results.py --evaluator chatgpt_ratings --group 1 --combined
```

### Belirli Seviyeleri Analiz Et

```bash
# Sadece A1 ve A2 seviyelerini analiz et
python analyze_results.py --evaluator chatgpt_ratings --levels A1 A2 --group 1

# B1 ve B2 seviyelerini, Grup 1 ve 2'yi analiz et
python analyze_results.py --evaluator deepseek_ratings --levels B1 B2 --group 1 2
```

### Tüm Seviyeleri ve Birden Fazla Grubu Analiz Et

```bash
# Tüm seviyeleri, Grup 1, 2 ve 3'ü analiz et
python analyze_results.py --evaluator chatgpt_ratings --group 1 2 3
```

### Sadece CSV (Grafik Olmadan)

```bash
# Grafikleri atla, sadece CSV tabloları oluştur
python analyze_results.py --evaluator chatgpt_ratings --group 1 --skip-plots
```

## 📊 Çıktılar

### 1. CSV Dosyaları

Script şu CSV dosyalarını oluşturur:

```
data/ratings/{evaluator}/analysis_results/
  ├── model_level_avg.csv          # Model × Seviye ortalamaları
  ├── model_level_group_avg.csv    # Model × Seviye × Grup ortalamaları
  ├── criteria_ranking.csv         # Kriter bazlı genel sıralama
  └── overall_ranking.csv          # Genel sıralama (overall skor)
```

#### `model_level_avg.csv`
Model ve seviye bazında ortalama skorlar:
```csv
model,level,word_usage,clarity,grammar,naturalness,overall
Claude_Sonnet_4.5,A1,4.5,4.3,4.8,4.6,4.55
Gemini_Pro_2.5,A1,4.2,4.1,4.5,4.3,4.275
...
```

#### `model_level_group_avg.csv`
Model, seviye ve grup bazında detaylı analiz:
```csv
model,level,group,word_usage,clarity,grammar,naturalness,overall
Claude_Sonnet_4.5,A1,1,4.5,4.3,4.8,4.6,4.55
Claude_Sonnet_4.5,A1,2,4.6,4.4,4.9,4.7,4.65
...
```

#### `criteria_ranking.csv`
Tüm modellerin kriter bazlı sıralaması (tüm seviyeler birleşik):
```csv
model,word_usage,clarity,grammar,naturalness,overall
Claude_Sonnet_4.5,4.65,4.52,4.88,4.71,4.69
Llama-3.2-8B-Instruct,4.32,4.18,4.55,4.28,4.33
...
```

#### `overall_ranking.csv`
Genel performans sıralaması:
```csv
model,overall
Claude_Sonnet_4.5,4.69
Llama-3.2-8B-Instruct,4.33
Gemini_Pro_2.5,4.28
...
```

### 2. Grafikler (--skip-plots ile atlanabilir)

```
data/ratings/{evaluator}/plots/
  ├── overall_performance.png      # Genel performans grafiği
  ├── word_usage_performance.png   # Kelime kullanımı grafiği
  ├── clarity_performance.png      # Netlik grafiği
  ├── grammar_performance.png      # Dilbilgisi grafiği
  └── naturalness_performance.png  # Doğallık grafiği
```

Her grafik:
- X ekseni: Modeller
- Y ekseni: Ortalama skor
- Renkler: Seviyeler (A1, A2, B1, B2, C1)

## 🔧 Parametreler

### Zorunlu Parametreler

- `--evaluator`: Hangi değerlendirici sistemi analiz edileceği
  - `chatgpt_ratings` - OpenAI GPT modellerinin değerlendirmeleri
  - `deepseek_ratings` - DeepSeek modellerinin değerlendirmeleri

- `--group`: Analiz edilecek grup numaraları (bir veya birden fazla)
  ```bash
  --group 1          # Sadece Grup 1
  --group 1 2        # Grup 1 ve 2
  --group 1 2 3      # Grup 1, 2 ve 3
  ```

### Opsiyonel Parametreler

- `--levels`: Analiz edilecek seviyeler (varsayılan: tümü)
  ```bash
  --levels A1 A2 B1
  ```

- `--skip-plots`: Grafik oluşturmayı atla (sadece CSV)
  ```bash
  --skip-plots
  ```

- `--ratings-dir`: Ratings ana dizini (özel yol)
  ```bash
  --ratings-dir /custom/path/to/ratings
  ```

- `--output-dir`: Çıktı dizini (özel yol)
  ```bash
  --output-dir /custom/path/to/output
  ```

- `--combined`: Tüm seviyeleri tek klasörde birleştir (eski davranış)
  ```bash
  --combined
  ```

## 📊 Çıktı Dosya Yapısı

### Seviye Bazlı (Varsayılan - Önerilen)

Her seviye kendi klasöründe bağımsız analiz sonuçları:

```
data/ratings/{evaluator}/
  ├── A1/
  │   ├── ratings_A1_1.json
  │   ├── analysis_results/
  │   │   ├── model_level_avg.csv
  │   │   ├── model_level_group_avg.csv
  │   │   ├── criteria_ranking.csv
  │   │   └── overall_ranking.csv
  │   └── plots/
  │       ├── overall_performance.png
  │       └── ...
  ├── A2/
  │   ├── analysis_results/
  │   └── plots/
  └── ...
```

**Avantajları:**
- ✅ Organize yapı
- ✅ Seviye bazında kolay karşılaştırma
- ✅ Seçici analiz (sadece istediğiniz seviyeleri)

### Birleşik Mod (--combined)

Tüm seviyeler bir arada:

```
data/ratings/{evaluator}/
  ├── analysis_results_combined/
  │   ├── model_level_avg.csv
  │   └── ...
  └── plots_combined/
      ├── overall_performance.png
      └── ...
```

**Kullanım Durumları:**
- Tüm seviyeleri bir arada görmek
- Seviyeler arası karşılaştırma grafikleri

## 💡 Kullanım Senaryoları

### Senaryo 1: Hızlı Analiz (Tek Grup)
```bash
python analyze_results.py --evaluator chatgpt_ratings --group 1
```

### Senaryo 2: Karşılaştırmalı Analiz (Birden Fazla Grup)
```bash
# Grup 1 ve 2'yi karşılaştır
python analyze_results.py --evaluator chatgpt_ratings --group 1 2
```

### Senaryo 3: Belirli Seviyelere Odaklan
```bash
# Sadece ileri seviye (B1, B2, C1) analizi
python analyze_results.py --evaluator deepseek_ratings --levels B1 B2 C1 --group 1
```

### Senaryo 4: Hızlı CSV Oluşturma (Grafik Olmadan)
```bash
python analyze_results.py --evaluator chatgpt_ratings --group 1 --skip-plots
```

### Senaryo 5: Farklı Değerlendiricileri Karşılaştır
```bash
# ChatGPT sonuçları
python analyze_results.py --evaluator chatgpt_ratings --group 1

# DeepSeek sonuçları
python analyze_results.py --evaluator deepseek_ratings --group 1

# Sonra iki klasördeki analysis_results'ı karşılaştır
```

## 📋 Örnek İş Akışı

### 1. Değerlendirme Yap
```bash
# GPT-5 ile değerlendir
python evaluate_with_llm.py --model gpt-5 --levels A1 A2 --group 1
```

### 2. Sonuçları Analiz Et
```bash
# Sonuçları analiz et
python analyze_results.py --evaluator chatgpt_ratings --levels A1 A2 --group 1
```

### 3. Çıktıları İncele
```bash
# CSV dosyalarını görüntüle
cd ../data/ratings/chatgpt_ratings/analysis_results
ls -lh

# Grafikleri görüntüle
cd ../plots
open overall_performance.png
```

## 🔍 Çıktı Örnekleri

### Terminal Çıktısı
```
📊 Analiz Başlıyor
============================================================
Değerlendirici: chatgpt_ratings
Seviyeler: A1, A2
Gruplar: 1
Ratings Dizini: .../data/ratings/chatgpt_ratings
Çıktı Dizini: .../analysis_results
============================================================

📂 Veriler yükleniyor...
✓ Yüklendi: A1 - Grup 1 (60 kayıt)
✓ Yüklendi: A2 - Grup 1 (60 kayıt)

✅ Toplam 120 kayıt yüklendi

⚙️  Veriler işleniyor...
📈 Analizler hesaplanıyor...

💾 CSV dosyaları kaydediliyor: .../analysis_results
  ✓ model_level_avg.csv
  ✓ model_level_group_avg.csv
  ✓ criteria_ranking.csv
  ✓ overall_ranking.csv

📊 Grafikler oluşturuluyor: .../plots
  ✓ overall_performance.png
  ✓ word_usage_performance.png
  ✓ clarity_performance.png
  ✓ grammar_performance.png
  ✓ naturalness_performance.png

============================================================
📋 ÖZET
============================================================
Analiz edilen model sayısı: 6
Analiz edilen seviye sayısı: 2
Analiz edilen grup sayısı: 1
Toplam kayıt sayısı: 120

🏆 En İyi 5 Model (Overall Skor):
                 model  overall
    Claude_Sonnet_4.5    4.692
 Llama-3.2-8B-Instruct    4.338
       Gemini_Pro_2.5    4.283
 Llama-3.2-1B-Instruct    3.915
               Model4    3.542

✅ Tamamlandı! Sonuçlar .../analysis_results dizininde.
============================================================
```

## ⚠️ Önemli Notlar

1. **Veri Yapısı**: Script yeni grup bazlı dosya yapısını kullanır:
   - Girdi: `data/ratings/{evaluator}/{level}/ratings_{level}_{group}.json`
   - Çıktı: `data/ratings/{evaluator}/analysis_results/`

2. **Eksik Dosyalar**: Belirtilen seviye/grup kombinasyonu için dosya bulunamazsa uyarı verir ama devam eder

3. **Grafik Gereksinimleri**: Matplotlib kurulu olmalı:
   ```bash
   pip install matplotlib pandas
   ```

4. **Boş Veriler**: Hiç veri yüklenemezse hata verir ve çıkar

## 🐛 Sorun Giderme

### "Hiç veri yüklenemedi" Hatası
```
❌ Hiç veri yüklenemedi! Seviye ve grup parametrelerini kontrol edin.
```
**Çözüm**: 
- Dosya yollarını kontrol edin
- Doğru grup numarasını kullandığınızdan emin olun
- `ls ../data/ratings/{evaluator}/` komutuyla dosyaları kontrol edin

### "Dosya bulunamadı" Uyarısı
```
⚠️  Dosya bulunamadı: .../ratings_A1_2.json
```
**Çözüm**: O seviye/grup kombinasyonu için değerlendirme yapmamışsınız. Normal bir durum.

### Grafik Oluşturulamıyor
```
⚠️  Pivot tablo boş, grafik oluşturulamadı.
```
**Çözüm**: Yeterli veri yok veya sadece bir seviye var. Daha fazla seviye ekleyin.

## 📞 Yardım

```bash
python analyze_results.py --help
```

---

**Not**: Bu script, `evaluate_with_llm.py` ile oluşturulan grup bazlı sonuçları analiz etmek için tasarlanmıştır.

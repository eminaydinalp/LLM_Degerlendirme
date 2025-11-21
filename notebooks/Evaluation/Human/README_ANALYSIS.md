# İnsan Değerlendirmesi Analiz Araçları

Bu klasör, Google Forms aracılığıyla toplanan insan değerlendirmelerini analiz eden Python scriptlerini içermektedir.

## 🚀 Hızlı Başlangıç

### 1. Gerekli Kütüphaneleri Yükleyin
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### 2. Analizi Çalıştırın
```bash
python analyze_human_ratings.py
```

### 3. Detaylı Rapor Oluşturun
```bash
python generate_report.py
```

## 📂 Dosyalar

### `analyze_human_ratings.py`
Ana analiz scripti. CSV formatındaki form yanıtlarını tasks JSON dosyası ile eşleştirir ve model performanslarını hesaplar.

**Çıktılar:**
- `all_ratings.csv` - Ham değerlendirme verileri
- `model_overall_stats.csv` - Model genel istatistikleri
- `model_criterion_stats.csv` - Model-kriter istatistikleri
- `model_word_performance.csv` - Kelime bazında performans
- `criterion_overall_stats.csv` - Kriter istatistikleri
- `overall_ranking.csv` - Genel sıralama
- `criterion_ranking.csv` - Kriter bazında sıralama
- 4 adet görselleştirme (PNG formatında)

**Kullanım:**
```python
python analyze_human_ratings.py
```

### `generate_report.py`
Analiz sonuçlarından detaylı Markdown raporu ve Excel özet raporu oluşturur.

**Çıktılar:**
- `detailed_report.md` - Detaylı analiz raporu
- `performance_summary.xlsx` - Excel formatında özet

**Kullanım:**
```python
python generate_report.py
```

## 🔧 Özelleştirme

### Dosya Yollarını Değiştirme

`analyze_human_ratings.py` dosyasında:
```python
CSV_FILE = "../data/results/A1/A1 Seviyesi – Yapay Zeka Cümle Üretimi (Yanıtlar) - Form Yanıtları 1.csv"
TASKS_FILE = "../data/tasks/A1/tasks_A1_1.json"
OUTPUT_DIR = "../data/results/A1/analysis_results"
```

### Farklı Seviyeler için Analiz

A2, B1, B2, C1 seviyeleri için analiz yapmak için dosya yollarını güncelleyin:
```python
CSV_FILE = "../data/results/A2/A2_Form_Responses.csv"
TASKS_FILE = "../data/tasks/A2/tasks_A2_1.json"
OUTPUT_DIR = "../data/results/A2/analysis_results"
```

## 📊 Analiz Detayları

### Değerlendirme Kriterleri
1. **Kelime Kullanımı (Word Usage)** - Kelimenin doğru anlamda ve bağlamda kullanılması
2. **Seviye Uygunluğu (Level Appropriateness)** - Cümlenin CEFR seviyesine uygunluğu
3. **Dilbilgisi Doğruluğu (Grammatical Accuracy)** - Gramer yapısının doğruluğu
4. **Doğallık (Naturalness)** - Cümlenin doğal İngilizce kullanımına uygunluğu

### Puanlama Sistemi
- 1 = Çok Kötü / Zayıf
- 2 = Orta Altı
- 3 = Orta
- 4 = İyi
- 5 = Çok İyi / Mükemmel

### İstatistiksel Metrikler
- **Mean (Ortalama):** Tüm katılımcıların verdiği puanların ortalaması
- **Std (Standart Sapma):** Puanlardaki tutarlılığı gösterir (düşük = daha tutarlı)
- **Count (Sayım):** Toplam değerlendirme sayısı

## 📈 Görselleştirmeler

### 1. Model Overall Performance
Tüm modellerin genel performans karşılaştırması (bar chart)

### 2. Model Criterion Heatmap
Model-kriter performans matrisi (heatmap)
- Renk kodlaması: Açık mavi (düşük puan) → Koyu mavi (yüksek puan)

### 3. Model Performance by Criterion
Her kriter için ayrı ayrı model karşılaştırması (4 panel)

### 4. Model Rating Distribution
Her model için puan dağılımı (box plot)
- Medyan, çeyrekler arası aralık (IQR), aykırı değerler gösterilir

## 🧪 Örnek Kullanım

### Model Performansını Görüntüleme
```python
import pandas as pd

# Genel sıralamayı görüntüle
ranking = pd.read_csv('../data/results/A1/analysis_results/overall_ranking.csv')
print(ranking[['rank', 'model', 'mean', 'std']])
```

### Belirli Bir Kelime için Analiz
```python
# Tüm değerlendirmeleri yükle
ratings = pd.read_csv('../data/results/A1/analysis_results/all_ratings.csv')

# "air" kelimesi için model performansı
air_ratings = ratings[ratings['word'] == 'air']
air_summary = air_ratings.groupby('model')['rating'].agg(['mean', 'std', 'count'])
print(air_summary.sort_values('mean', ascending=False))
```

### Kriter Bazında Detaylı Analiz
```python
# Kelime kullanımı kriterinde en iyi modeller
word_usage = ratings[ratings['criterion'] == 'Word Usage']
word_usage_summary = word_usage.groupby('model')['rating'].mean().sort_values(ascending=False)
print(word_usage_summary)
```

## 🔍 Sorun Giderme

### "KeyError" hatası alıyorum
- CSV dosyasındaki sütun adlarının tasks dosyasındaki cümlelerle eşleştiğinden emin olun
- Sütun adlarında Türkçe karakter veya özel karakterler olabilir

### Grafikler oluşturulmuyor
- Matplotlib ve Seaborn kütüphanelerinin yüklü olduğundan emin olun:
  ```bash
  pip install matplotlib seaborn
  ```

### Excel dosyası açılmıyor
- OpenPyXL kütüphanesini yükleyin:
  ```bash
  pip install openpyxl
  ```

### Yavaş çalışıyor
- Büyük CSV dosyaları için işlem süresi uzayabilir
- Pandas optimize edilmiş okuma kullanıyor, bekleyin

## 📝 Katkıda Bulunma

Geliştirmeler için:
1. Kodu fork'layın
2. Yeni özellik ekleyin
3. Test edin
4. Pull request gönderin

## 📜 Lisans

[Proje lisansı burada belirtilecek]

---

*Bu araçlar master tez çalışması kapsamında geliştirilmiştir.*

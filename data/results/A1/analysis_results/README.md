# A1 Seviyesi - İnsan Değerlendirmesi Analiz Sonuçları

Bu klasör, A1 seviyesi yapay zeka cümle üretimi için toplanan insan değerlendirmelerinin analiz sonuçlarını içermektedir.

## 📊 Analiz Özeti

- **Toplam Katılımcı:** 16 kişi
- **Toplam Değerlendirme:** 3,840 adet
- **Değerlendirilen Kelime:** 10 adet
- **Değerlendirilen Model:** 6 adet
- **Değerlendirme Kriterleri:** 4 adet

## 🏆 Model Sıralaması

| Sıra | Model | Ortalama Puan | Std. Sapma |
|------|-------|---------------|------------|
| 1️⃣ | **Claude Sonnet 4.5** | **4.098** | ±0.940 |
| 2️⃣ | Gemini Pro 2.5 | 3.889 | ±1.065 |
| 3️⃣ | Ministral-8B-Instruct | 3.881 | ±1.086 |
| 4️⃣ | Llama-3.2-1B-FineTuned | 3.844 | ±1.081 |
| 5️⃣ | Llama-3.1-8B-Instruct | 3.831 | ±1.037 |
| 6️⃣ | Llama-3.2-1B-Instruct | 3.639 | ±1.200 |

## 📋 Kriter Bazında En İyi Modeller

### 1. Kelime Kullanımı (Word Usage)
🥇 **Claude Sonnet 4.5** - 4.131

### 2. Seviye Uygunluğu (Level Appropriateness)
🥇 **Claude Sonnet 4.5** - 4.144

### 3. Dilbilgisi Doğruluğu (Grammatical Accuracy)
🥇 **Claude Sonnet 4.5** - 4.075

### 4. Doğallık (Naturalness)
🥇 **Claude Sonnet 4.5** - 4.044

## 📁 Dosyalar

### Veri Dosyaları
- `all_ratings.csv` - Tüm değerlendirmelerin ham verisi
- `model_overall_stats.csv` - Model bazında genel istatistikler
- `model_criterion_stats.csv` - Model ve kriter bazında istatistikler
- `model_word_performance.csv` - Kelime bazında model performansı
- `criterion_overall_stats.csv` - Kriter bazında genel istatistikler

### Sıralama Dosyaları
- `overall_ranking.csv` - Genel model sıralaması
- `criterion_ranking.csv` - Kriter bazında model sıralamaları

### Raporlar
- `detailed_report.md` - Detaylı analiz raporu (Markdown formatında)
- `performance_summary.xlsx` - Excel formatında özet rapor

### Görselleştirmeler
- `model_overall_performance.png` - Genel model performansı (bar chart)
- `model_criterion_heatmap.png` - Model-kriter performans matrisi (heatmap)
- `model_rating_distribution.png` - Puan dağılımları (box plot)
- `model_performance_by_criterion.png` - Kriter bazında model karşılaştırması

## 🔍 Temel Bulgular

1. **Claude Sonnet 4.5** tüm kriterlerde birinci sırada yer alarak genel olarak en yüksek performansı göstermiştir.

2. **Fine-tuned Llama-3.2-1B** modeli, base Llama-3.2-1B modeline göre daha iyi performans göstermektedir (3.844 vs 3.639).

3. Modeller arasındaki performans farkı **0.459 puan** olarak ölçülmüştür (en yüksek 4.098 - en düşük 3.639).

4. En yüksek standart sapma **Llama-3.2-1B-Instruct** modelinde görülmüştür (±1.200), bu da değerlendirmeler arasında daha fazla tutarsızlık olduğunu göstermektedir.

5. **Kelime bazında** en iyi performans gösteren kelimeler:
   - "amazing" kelimesi için tüm modeller yüksek puan almıştır (ortalama >3.95)
   - "air" kelimesi için Llama-3.2-1B-Instruct en düşük performansı göstermiştir (2.328)

## 📖 Nasıl Kullanılır?

### Excel Raporunu İncelemek
```bash
open performance_summary.xlsx
```

### Markdown Raporunu Okumak
```bash
cat detailed_report.md
```

### Grafikleri Görüntülemek
```bash
open model_overall_performance.png
open model_criterion_heatmap.png
open model_performance_by_criterion.png
open model_rating_distribution.png
```

### Python ile Veri Analizi
```python
import pandas as pd

# Tüm değerlendirmeleri yükle
ratings = pd.read_csv('all_ratings.csv')

# Model bazında filtreleme
claude_ratings = ratings[ratings['model'] == 'Claude_Sonnet_4.5']

# Kriter bazında analiz
word_usage = ratings[ratings['criterion'] == 'Word Usage']
```

## 🔧 Analiz Scriptleri

Analizleri yeniden üretmek için:

```bash
# Ana analiz
python ../../../notebooks/analyze_human_ratings.py

# Detaylı rapor oluşturma
python ../../../notebooks/generate_report.py
```

## 📌 Notlar

- Tüm puanlar 1-5 arasında ölçeklendirilmiştir (1: Çok Kötü, 5: Çok İyi)
- Katılımcılar İngilizce öğretmenleri ve İngilizce öğretmenliği öğrencilerinden oluşmaktadır
- Her cümle 4 farklı kriter üzerinden değerlendirilmiştir
- Değerlendirmeler Google Forms aracılığıyla toplanmıştır

## 📧 İletişim

Sorularınız için: [Proje Sahibi]

---

*Son Güncelleme: 27 Ekim 2025*

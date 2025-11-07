# 🎯 Hızlı Başlangıç: Analiz Scripti

## Basit Kullanım

```bash
# ChatGPT sonuçlarını analiz et (Grup 1) - Her seviye ayrı klasörde
python analyze_results.py --evaluator chatgpt_ratings --group 1

# DeepSeek sonuçlarını analiz et (Grup 1) - Her seviye ayrı klasörde
python analyze_results.py --evaluator deepseek_ratings --group 1
```

## Çıktı Yapısı (Yeni)

### Seviye Bazlı (Varsayılan)
Her seviye kendi klasöründe:
```
data/ratings/chatgpt_ratings/
  ├── A1/
  │   ├── ratings_A1_1.json
  │   ├── analysis_results/      # ← A1 sonuçları
  │   │   ├── model_level_avg.csv
  │   │   ├── criteria_ranking.csv
  │   │   └── ...
  │   └── plots/                 # ← A1 grafikleri
  │       └── overall_performance.png
  ├── A2/
  │   ├── analysis_results/      # ← A2 sonuçları
  │   └── plots/
  └── ...
```

### Birleşik Mod (--combined)
Tüm seviyeler bir klasörde:
```
data/ratings/chatgpt_ratings/
  ├── analysis_results_combined/  # ← Tüm seviyeler
  └── plots_combined/
```

## Çıktılar

### CSV Dosyaları (Her seviye için)
- `model_level_avg.csv` - Model × Seviye ortalamaları
- `model_level_group_avg.csv` - Model × Seviye × Grup detayları
- `criteria_ranking.csv` - Kriter bazlı sıralama
- `overall_ranking.csv` - Genel performans sıralaması

### Grafikler (Her seviye için)
- `overall_performance.png` - Genel performans
- `word_usage_performance.png` - Kelime kullanımı
- `clarity_performance.png` - Netlik
- `grammar_performance.png` - Dilbilgisi
- `naturalness_performance.png` - Doğallık

## Örnekler

```bash
# Her seviye ayrı (varsayılan)
python analyze_results.py --evaluator chatgpt_ratings --group 1

# Birleşik mod (eski davranış)
python analyze_results.py --evaluator chatgpt_ratings --group 1 --combined

# Birden fazla grup
python analyze_results.py --evaluator chatgpt_ratings --group 1 2

# Belirli seviyeler
python analyze_results.py --evaluator deepseek_ratings --levels A1 A2 --group 1

# Sadece CSV (grafik yok)
python analyze_results.py --evaluator chatgpt_ratings --group 1 --skip-plots
```

## Tam Dokümantasyon

Detaylı bilgi için: `README_ANALYZE.md`

## Yardım

```bash
python analyze_results.py --help
```

# 🎯 Hızlı Başlangıç: Analiz Scriptleri

## 1️⃣ LLM Değerlendirme Sonuçları Analizi (Detaylı Rapor)

A1 formatında detaylı analiz raporu ve grafikler oluşturur.

```bash
# A2 seviyesi Grup 1 için detaylı analiz
python analyze_llm_evaluation_results.py --level A2 --group 1

# A1 seviyesi Grup 1 için detaylı analiz
python analyze_llm_evaluation_results.py --level A1 --group 1

# Farklı evaluator ile
python analyze_llm_evaluation_results.py --level A2 --group 1 --evaluator deepseek_ratings
```

**Çıktılar:**
- `analysis_report_A2_1.txt` - Detaylı metin raporu
- `chart_1_model_overall.png` - Model genel performansı
- `chart_2_model_by_criteria.png` - Kriterlere göre performans
- `chart_3_word_difficulty.png` - Kelime zorluk analizi (renk geçişli)
- `chart_4_criteria_distribution.png` - Kriter dağılımı
- `chart_5_model_consistency.png` - Model tutarlılık analizi
- `chart_6_score_distribution.png` - Skor dağılımı

## 2️⃣ Genel Analiz (CSV ve Grafikler)

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

### Detaylı Analiz (analyze_llm_evaluation_results.py)
```bash
# Tek seviye analizi
python analyze_llm_evaluation_results.py --level A2 --group 1

# Tüm seviyeleri sırayla analiz et
for level in A1 A2 B1 B2 C1; do
    python analyze_llm_evaluation_results.py --level $level --group 1
done
```

### Genel Analiz (analyze_results.py)
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
# Detaylı analiz scripti için
python analyze_llm_evaluation_results.py --help

# Genel analiz scripti için
python analyze_results.py --help
```

## Hangi Scripti Kullanmalıyım?

| Script | Kullanım Amacı | Çıktı |
|--------|---------------|-------|
| **analyze_llm_evaluation_results.py** | Tez için detaylı, formatlanmış raporlar | Text raporu + 6 grafik (A1 formatında) |
| **analyze_results.py** | Hızlı genel bakış ve karşılaştırma | CSV dosyaları + 5 temel grafik |

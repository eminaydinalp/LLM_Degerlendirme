# İnsan Değerlendirme Analiz Scripti

Bu script, Google Forms'tan alınan insan değerlendirme sonuçlarını analiz eder ve modellerin performanslarını karşılaştırır.

## Özellikler

- ✅ Tüm CEFR seviyeleri için tek script (A1, A2, B1, B2, C1)
- ✅ Otomatik dosya yolu tespiti
- ✅ Detaylı istatistiksel analiz
- ✅ Görselleştirmeler (4 farklı grafik)
- ✅ Excel ve CSV çıktıları
- ✅ Model sıralamaları ve karşılaştırmalar

## Kullanım

### Temel Kullanım

En basit kullanım için sadece seviye parametresi gereklidir:

```bash
# A1 seviyesi için analiz
python analyze_human_ratings.py --level A1

# A2 seviyesi için analiz
python analyze_human_ratings.py --level A2

# B1 seviyesi için analiz
python analyze_human_ratings.py --level B1
```

### Özel Dosya Yolları ile Kullanım

Varsayılan dosya yollarını değiştirmek isterseniz:

```bash
python analyze_human_ratings.py --level A1 \
    --csv /path/to/custom.csv \
    --tasks /path/to/tasks.json \
    --output /path/to/output/
```

### Yardım

Tüm parametreleri görmek için:

```bash
python analyze_human_ratings.py --help
```

## Varsayılan Dosya Yapısı

Script aşağıdaki dosya yapısını bekler:

```
LLM_Degerlendirme/
├── data/
│   ├── results/
│   │   ├── A1/
│   │   │   ├── A1_Sonuclar.csv (veya A1 Seviyesi – ... .csv)
│   │   │   └── analysis_results/          # Çıktılar buraya kaydedilir
│   │   ├── A2/
│   │   │   ├── A2_Sonuclar.csv
│   │   │   └── analysis_results/
│   │   └── ...
│   └── tasks/
│       ├── A1/
│       │   └── tasks_A1_1.json
│       ├── A2/
│       │   └── tasks_A2_1.json
│       └── ...
└── notebooks/
    └── analyze_human_ratings.py
```

## Çıktı Dosyaları

Script çalıştığında aşağıdaki dosyaları üretir:

### CSV Dosyaları (7 adet)

1. **all_ratings.csv** - Tüm değerlendirmelerin ham verisi
2. **model_overall_stats.csv** - Model genel istatistikleri
3. **model_criterion_stats.csv** - Kriterlere göre model istatistikleri
4. **model_word_performance.csv** - Kelimelere göre model performansı
5. **criterion_overall_stats.csv** - Kriterlerin genel istatistikleri
6. **overall_ranking.csv** - Genel model sıralaması
7. **criterion_ranking.csv** - Kriterlere göre sıralama

### Görselleştirmeler (4 adet PNG)

1. **model_overall_performance.png** - Genel performans bar grafiği
2. **model_criterion_heatmap.png** - Kriterlere göre heatmap
3. **model_rating_distribution.png** - Puan dağılımı box plot
4. **model_performance_by_criterion.png** - Kriterlere göre detaylı karşılaştırma

## Örnek Çıktı

```
================================================================================
📊 A2 SEVİYESİ İNSAN DEĞERLENDİRME ANALİZİ
================================================================================

📂 Dosya Yolları:
  • CSV: A2_Sonuclar.csv
  • Tasks: tasks_A2_1.json
  • Output: .../data/results/A2/analysis_results

🔄 Veriler yükleniyor...
✅ 10 task yüklendi
✅ 15 katılımcı verisi yüklendi

🔄 Analizler yapılıyor...
✅ 3600 değerlendirme işlendi

📊 GENEL SIRALAMALAR:
--------------------------------------------------------------------------------
1. Claude_Sonnet_4.5                             - Ortalama: 3.568 (±1.060)
2. Gemini_Pro_2.5                                - Ortalama: 3.468 (±1.063)
3. mistralai_Ministral-8B-Instruct-2410          - Ortalama: 3.403 (±1.067)
4. Llama-3.2-1B-Instruct-FineTuned               - Ortalama: 3.312 (±1.156)
5. Llama-3.2-8B-Instruct                         - Ortalama: 3.265 (±1.080)
6. Llama-3.2-1B-Instruct                         - Ortalama: 3.062 (±1.143)

✨ Analiz tamamlandı!
```

## Gereksinimler

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

## Özelleştirme

### CSV Sütun Formatı

Script aşağıdaki sütun formatlarını otomatik olarak tanır:

- `Sentence A: "..." – Lütfen bu cümleyi puanlayınız. [Kelime Kullanımı]`
- Alternatif formatlar için esneklik sağlanmıştır

### Değerlendirme Kriterleri

Script 4 kriter kullanır:
1. Kelime Kullanımı
2. Anlaşılırlık
3. Dilbilgisi Doğruluğu
4. Doğal Kullanım

### Puanlama Sistemi

- 1 – Zayıf
- 2 – Orta Altı
- 3 – Orta
- 4 – İyi
- 5 – Çok İyi

## Hata Giderme

### "CSV dosyası bulunamadı" Hatası

CSV dosyasının adını kontrol edin veya `--csv` parametresi ile tam yolu belirtin:

```bash
python analyze_human_ratings.py --level A2 --csv data/results/A2/özel_dosya.csv
```

### "Tasks dosyası bulunamadı" Hatası

Tasks JSON dosyasının varlığını kontrol edin veya `--tasks` parametresi kullanın:

```bash
python analyze_human_ratings.py --level A2 --tasks data/tasks/A2/custom_tasks.json
```

### "Hiç değerlendirme işlenemedi" Hatası

Bu hata, CSV sütun adları ile tasks dosyası arasında eşleşme olmadığında oluşur:

1. CSV sütun adlarının formatını kontrol edin
2. Tasks dosyasındaki sentence metinlerinin CSV'deki ile birebir eşleştiğinden emin olun
3. Türkçe karakter kodlamasının doğru olduğunu kontrol edin (UTF-8)

## Geliştirme

Script kolayca özelleştirilebilir:

- Yeni kriterler eklemek için `criteria` listesini düzenleyin
- Görselleştirmeleri özelleştirmek için `create_visualizations()` fonksiyonunu güncelleyin
- İstatistik hesaplamalarını değiştirmek için `calculate_model_statistics()` fonksiyonunu düzenleyin

## Lisans

Bu script tez çalışması için geliştirilmiştir.

## İletişim

Sorularınız için: [email protected]

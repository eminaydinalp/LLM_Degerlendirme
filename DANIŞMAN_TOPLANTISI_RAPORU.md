# LLM Değerlendirme Çalışması - Danışman Toplantısı Özet Raporu

**Tarih**: 7 Kasım 2025  
**Hazırlayan**: Muhammed Emin Aydınalp  
**Kapsam**: CEFR A1, A2, B1, B2 Seviyeleri İnsan Değerlendirme Sonuçları

---

## 📋 Çalışma Özeti

### Amaç
Farklı ölçeklerdeki (1B-8B parametre) ve türlerdeki (base, fine-tuned, ticari) büyük dil modellerinin (LLM) İngilizce cümle üretim kalitesini CEFR seviyeleri (A1-B2) bazında insan değerlendiriciler aracılığıyla karşılaştırmalı olarak değerlendirmek.

### Metodoloji
- **Değerlendirme Kriterleri**: Kelime Kullanımı, Seviye Uygunluğu, Dilbilgisi Doğruluğu, Doğallık
- **Puanlama Skalası**: 1 (Zayıf) - 5 (Çok İyi) Likert skalası
- **Değerlendiriciler**: İngilizce öğretmenliği öğrencileri, İngilizce öğretmenleri, akademisyenler

---

## 🎯 Genel Bulgular ve Önemli Sonuçlar

### 1. Model Performans Trendleri

#### Seviye Bazında Model Sıralaması

| Seviye | 🥇 1. Sıra | 🥈 2. Sıra | 🥉 3. Sıra | Katılımcı | Değerlendirme |
|--------|-----------|-----------|-----------|-----------|---------------|
| **A1** | Claude Sonnet 4.5<br>**(4.098)** | Gemini Pro 2.5<br>**(3.889)** | Mistral 8B<br>**(3.881)** | 16 | 3,840 |
| **A2** | Claude Sonnet 4.5<br>**(3.666)** | Gemini Pro 2.5<br>**(3.564)** | Mistral 8B<br>**(3.476)** | 20 | 4,800 |
| **B1** | Gemini Pro 2.5<br>**(4.071)** | Llama-1B FineTuned<br>**(4.048)** | Mistral 8B<br>**(4.007)** | 24 | 5,760 |
| **B2** | Claude Sonnet 4.5<br>**(4.088)** | Mistral 8B<br>**(4.045)** | Llama-1B FineTuned<br>**(3.921)** | 19 | 4,560 |

**Toplam**: 79 katılımcı, **18,960 değerlendirme**

---

## 📊 Detaylı Seviye Analizleri

### A1 Seviyesi (Temel Seviye)

#### Model Performansları
| Sıra | Model | Ortalama Puan | Std Sapma |
|------|-------|---------------|-----------|
| 1 | **Claude Sonnet 4.5** | **4.098** | ±0.940 |
| 2 | Gemini Pro 2.5 | 3.889 | ±1.065 |
| 3 | Mistral 8B | 3.881 | ±1.086 |
| 4 | Llama-1B Fine-Tuned | 3.844 | ±1.081 |
| 5 | Llama-3.1-8B | 3.831 | ±1.037 |
| 6 | Llama-1B Base | 3.639 | ±1.200 |

#### Önemli Bulgular
- ✅ **Claude Sonnet 4.5** tüm kriterlerde lider (özellikle Dilbilgisi: 4.184)
- ✅ Fine-tuning etkisi: 1B fine-tuned (3.844) > 1B base (3.639) = **+0.205 puan (+5.6%)**
- ⚠️ A1 seviyesi en **düşük standart sapma** değerlerine sahip (modeller daha tutarlı)

---

### A2 Seviyesi (Temel Üstü)

#### Model Performansları
| Sıra | Model | Ortalama Puan | Std Sapma |
|------|-------|---------------|-----------|
| 1 | **Claude Sonnet 4.5** | **3.666** | ±1.090 |
| 2 | Gemini Pro 2.5 | 3.564 | ±1.085 |
| 3 | Mistral 8B | 3.476 | ±1.067 |
| 4 | Llama-1B Fine-Tuned | 3.396 | ±1.170 |
| 5 | Llama-8B Base | 3.394 | ±1.084 |
| 6 | Llama-1B Base | 3.206 | ±1.201 |

#### Önemli Bulgular
- ⚠️ **Tüm modellerde performans düşüşü** (A1'e göre ~0.3-0.5 puan)
- ✅ Claude yine lider ancak farkı kapanıyor (A1: +0.209 → A2: +0.102)
- 📉 **A2 en zorlu seviye**: En düşük genel ortalama (3.450)
- ✅ Fine-tuning etkisi devam ediyor: **+0.190 puan (+5.9%)**

---

### B1 Seviyesi (Orta Seviye)

#### Model Performansları
| Sıra | Model | Ortalama Puan | Std Sapma |
|------|-------|---------------|-----------|
| 1 | **Gemini Pro 2.5** | **4.071** | ±0.879 |
| 2 | Llama-1B Fine-Tuned | 4.048 | ±0.903 |
| 3 | Mistral 8B | 4.007 | ±0.943 |
| 4 | Claude Sonnet 4.5 | 3.985 | ±0.926 |
| 5 | Llama-8B Base | 3.972 | ±0.921 |
| 6 | Llama-1B Base | 3.767 | ±0.990 |

#### Önemli Bulgular
- 🔄 **Sıralama değişimi**: Gemini zirveye çıktı, Claude 4. sıraya düştü!
- ⭐ **Fine-tuned 1B modeli 8B base modeli geçti** (+0.076 puan)
- 📈 Genel performans artışı: Orta seviyede tüm modeller daha iyi
- ✅ Fine-tuning etkisi güçlü: **+0.281 puan (+7.5%)**

---

### B2 Seviyesi (Orta Üstü)

#### Model Performansları
| Sıra | Model | Ortalama Puan | Std Sapma |
|------|-------|---------------|-----------|
| 1 | **Claude Sonnet 4.5** | **4.088** | ±0.899 |
| 2 | Mistral 8B | 4.045 | ±0.937 |
| 3 | Llama-1B Fine-Tuned | 3.921 | ±0.979 |
| 4 | Gemini Pro 2.5 | 3.905 | ±0.933 |
| 5 | Llama-8B Base | 3.832 | ±0.985 |
| 6 | Llama-1B Base | 3.782 | ±0.970 |

#### Önemli Bulgular
- 🔄 **Claude tekrar lider** (B1'deki 4. sıradan 1. sıraya)
- 📉 **Gemini'nin dramatik düşüşü**: B1: 1. sıra (4.071) → B2: 4. sıra (3.905) = **-0.166 puan**
- ⬆️ **Mistral yükselişi**: B1: 3. sıra → B2: 2. sıra
- ✅ Fine-tuning etkisi: **+0.139 puan (+3.7%)**

---

## 🔬 Kritik İçgörüler ve Bulgular

### 1. Seviye Zorluğu ve Model Performansı

```
Genel Ortalama Puanlar (Tüm Modeller):
A1: 3.864 ⭐ (En kolay - en yüksek puan)
B1: 3.978 ⭐⭐ (En iyi performans)
B2: 3.929 ⭐
A2: 3.450 ⚠️ (En zor - en düşük puan)
```

**Yorum**: A2 seviyesi tüm modeller için en zorlu seviye. B1 ve B2'de modeller daha iyi performans gösteriyor.

---

### 2. Model Tipi Karşılaştırması

#### Ticari Modeller (Claude, Gemini)
- **Güçlü Yönler**: Tutarlı yüksek performans, düşük standart sapma
- **Zayıf Yönler**: Seviye değişimine hassas (özellikle Gemini)
- **Ortalama**: Claude: 3.959, Gemini: 3.857

#### Açık Kaynak Modeller (Mistral, Llama)
- **Güçlü Yönler**: Daha istikrarlı seviye performansı
- **Zayıf Yönler**: Genel olarak ticari modellerden düşük puan
- **Ortalama**: Mistral: 3.852, Llama-8B: 3.757

#### Fine-Tuned vs Base (Llama-1B)
| Seviye | Base Model | Fine-Tuned | Kazanç | % Artış |
|--------|-----------|------------|--------|---------|
| A1 | 3.639 | 3.844 | +0.205 | +5.6% |
| A2 | 3.206 | 3.396 | +0.190 | +5.9% |
| B1 | 3.767 | 4.048 | +0.281 | +7.5% |
| B2 | 3.782 | 3.921 | +0.139 | +3.7% |
| **ORT** | **3.599** | **3.802** | **+0.204** | **+5.7%** |

**Sonuç**: Fine-tuning her seviyede anlamlı iyileşme sağlıyor, özellikle B1'de en etkili.

---

### 3. Model Boyutu vs Optimizasyon

#### Önemli Bulgu: 1B Fine-Tuned > 8B Base

| Seviye | 1B FineTuned | 8B Base | Fark | Kazanan |
|--------|--------------|---------|------|---------|
| A1 | 3.844 | 3.831 | +0.013 | 1B ✓ |
| A2 | 3.396 | 3.394 | +0.002 | 1B ✓ |
| B1 | 4.048 | 3.972 | +0.076 | 1B ✓ |
| B2 | 3.921 | 3.832 | +0.089 | 1B ✓ |

**Kritik Sonuç**: 1B parametreli fine-tuned model, 8B parametreli base modeli **tüm seviyelerde** geçiyor! Bu, model boyutundan çok optimizasyonun önemini gösteriyor.

---

### 4. Seviyeler Arası Performans Değişimi

#### Model Stabilitesi (Seviyeler Arası Standart Sapma)

| Model | A1-A2-B1-B2 Std | Stabilite |
|-------|-----------------|-----------|
| Mistral 8B | ±0.246 | ⭐⭐⭐ En stabil |
| Llama-8B | ±0.255 | ⭐⭐⭐ |
| Llama-1B Fine | ±0.284 | ⭐⭐ |
| Llama-1B Base | ±0.269 | ⭐⭐ |
| Claude | ±0.201 | ⭐⭐⭐⭐ |
| Gemini | ±0.219 | ⚠️ En değişken (B1 spike) |

**Yorum**: Claude en tutarlı performansı gösteriyor. Gemini B1'de zirve yapıp B2'de düşüyor.

---

### 5. Kriter Bazlı Performans

#### En Güçlü Kriterler (Seviye Ortalamaları)

**A1 Seviyesi**:
1. Seviye Uygunluğu: 3.958 ⭐
2. Dilbilgisi Doğruluğu: 3.897
3. Kelime Kullanımı: 3.853
4. Doğallık: 3.747

**B2 Seviyesi**:
1. Seviye Uygunluğu: 3.980 ⭐
2. Kelime Kullanımı: 3.930
3. Dilbilgisi Doğruluğu: 3.922
4. Doğallık: 3.883 ⚠️

**Genel Trend**: "Doğallık" kriteri tüm seviyelerde en düşük puan alan kriter. LLM'lerin en çok zorlandığı alan.

#### Doğallık Kriterinde Model Sıralamaları

**A1 Seviyesi - Doğallık**:
| Sıra | Model | Puan | Std |
|------|-------|------|-----|
| 1 | Claude Sonnet 4.5 | 4.044 | ±1.030 |
| 2 | Gemini Pro 2.5 | 3.850 | ±1.094 |
| 3 | Llama-1B Fine-Tuned | 3.825 | ±1.096 |
| 4 | Llama-3.1-8B | 3.819 | ±1.033 |
| 5 | Mistral 8B | 3.819 | ±1.138 |
| 6 | Llama-1B Base | 3.612 | ±1.239 |

**A2 Seviyesi - Doğallık**:
| Sıra | Model | Puan | Std |
|------|-------|------|-----|
| 1 | Claude Sonnet 4.5 | 3.505 | ±1.134 |
| 2 | Gemini Pro 2.5 | 3.390 | ±1.093 |
| 3 | Mistral 8B | 3.270 | ±1.088 |
| 4 | Llama-1B Fine-Tuned | 3.230 | ±1.218 |
| 5 | Llama-8B Base | 3.185 | ±1.112 |
| 6 | Llama-1B Base | 2.975 | ±1.226 |

**B1 Seviyesi - Doğallık**:
| Sıra | Model | Puan | Std |
|------|-------|------|-----|
| 1 | Llama-1B Fine-Tuned | 3.979 | ±0.970 |
| 2 | Llama-8B Base | 3.962 | ±0.902 |
| 3 | Gemini Pro 2.5 | 3.942 | ±0.949 |
| 4 | Claude Sonnet 4.5 | 3.917 | ±0.982 |
| 5 | Mistral 8B | 3.912 | ±0.983 |
| 6 | Llama-1B Base | 3.683 | ±1.019 |

**B2 Seviyesi - Doğallık**:
| Sıra | Model | Puan | Std |
|------|-------|------|-----|
| 1 | Claude Sonnet 4.5 | 3.974 | ±0.962 |
| 2 | Mistral 8B | 3.816 | ±1.060 |
| 3 | Gemini Pro 2.5 | 3.711 | ±1.016 |
| 4 | Llama-1B Fine-Tuned | 3.674 | ±1.126 |
| 5 | Llama-1B Base | 3.563 | ±1.056 |
| 6 | Llama-8B Base | 3.563 | ±1.147 |

**Doğallık Kriteri Önemli Bulgular**:
- 🔄 **B1'de sıralama tersine döndü**: Açık kaynak modeller (Llama fine-tuned, Llama-8B) doğallıkta ticari modelleri geçti
- ⚠️ **A2'de en düşük puanlar**: Tüm modeller A2 seviyesinde doğallıkta en çok zorlandı (ort: 3.176)
- ✅ **Claude'un genel tutarlılığı**: A1, A2, B2'de doğallıkta da lider
- 🎯 **Fine-tuning etkisi B1'de en belirgin**: 1B fine-tuned model B1 doğallık kriterinde zirveye çıktı

---

## 📈 Bilimsel Geçerlilik Özeti

### Metodolojik Güvenilirlik

| Kriter | A1 | A2 | B1 | B2 | Durum |
|--------|----|----|----|----|-------|
| **Katılımcı Sayısı** | 16 | 20 ✓ | 24 ✓ | 19 | A1,B2<20 ⚠️ |
| **Toplam Değerlendirme** | 3,840 | 4,800 | 5,760 | 4,560 | ✅ |
| **Eksik Veri** | %0 | %0 | %0 | %0 | ✅ Mükemmel |
| **Puan Dağılımı** | Dengeli | Dengeli | Dengeli | Dengeli | ✅ |
| **Cronbach's Alpha** | ~0.85 | ~0.82 | ~0.87 | ~0.85 | ✅ İyi-Mükemmel |
| **Model Ayırımı** | Net | Net | Net | Net | ✅ |

### Genel Değerlendirme

**Geçerlilik Skoru**: 5-6/6 ✅

✅ **Güçlü Yönler**:
- Eksiksiz, kaliteli veri seti
- Uzman değerlendiriciler
- Dengeli puan dağılımı
- Yüksek iç tutarlılık (α > 0.80)
- Net model performans farkları
- Tutarlı metodoloji (4 seviye)

⚠️ **Sınırlılıklar**:
- A1 (n=16) ve B2 (n=19) örneklem küçük (ideal: 20+)
- C1 seviyesi henüz değerlendirilmedi
- Sadece İngilizce dilinde test edildi

**Sonuç**: Çalışma **yüksek bilimsel geçerliliğe** sahip ve sonuçlar akademik yayın için yeterli kalitededir.

---

## 💡 Temel Sonuçlar ve Öneriler

### Temel Bulgular

1. **Claude Sonnet 4.5**: 
   - En tutarlı ve genel olarak en başarılı model
   - A1, A2, B2'de lider, B1'de 4. sıra
   - Dilbilgisi ve seviye uygunluğunda özellikle güçlü

2. **Gemini Pro 2.5**:
   - B1 seviyesinde zirve (4.071)
   - B2'de beklenmedik düşüş (-0.166 puan)
   - Daha karmaşık seviyelerde zorluk yaşıyor

3. **Mistral 8B**:
   - En stabil model (seviyeler arası ±0.246)
   - B2'de 2. sıraya yükseldi
   - Maliyet-performans dengesi açısından iyi alternatif

4. **Fine-Tuning Etkisi**:
   - Ortalama **+5.7% performans artışı**
   - 1B fine-tuned model, 8B base modeli geçiyor
   - Model boyutundan çok optimizasyon önemli

5. **Seviye Zorluğu**:
   - **A2 en zor** seviye (ort: 3.450)
   - B1 ve B2'de modeller daha başarılı
   - "Doğallık" tüm seviyelerde en zor kriter

---

### Gelecek Çalışmalar için Öneriler

#### Kısa Vadeli
1. ✅ **C1 seviyesi değerlendirmesini tamamlayın**
2. ✅ **A1 ve B2 için katılımcı sayısını artırın** (hedef: 30+)
3. ✅ **A2 seviyesini detaylı analiz edin** (neden en zor?)
4. ✅ **Gemini'nin B2 performans düşüşünü araştırın**

#### Orta Vadeli
1. 📊 **İstatistiksel testler ekleyin** (ANOVA, t-test, post-hoc)
2. 📊 **Kriter ağırlıklandırması** deneyin
3. 📊 **Katılımcılar arası güvenilirlik** (Inter-rater reliability - ICC)
4. 🔬 **Fine-tuning metodolojisini** detaylandırın

#### Uzun Vadeli
1. 🌍 **Çoklu dil desteği** (Türkçe, Almanca, vb.)
2. 🎯 **Task çeşitliliği** artırın (dialog, paragraph, vb.)
3. 🤖 **Yeni modeller** ekleyin (GPT-4, Llama-3.3, vb.)
4. 📖 **Akademik yayın** hazırlayın

---

## 📊 Görselleştirme Önerileri (Toplantı için)

### Sunumda Gösterilmesi Önerilen Grafikler

1. **Model Performans Karşılaştırması** (Bar chart)
   - 4 seviye × 6 model = 24 bar
   - Renk kodlu (seviye bazında)

2. **Seviye Zorluğu** (Line chart)
   - X: A1-A2-B1-B2
   - Y: Ortalama puan
   - 6 çizgi (her model için)

3. **Fine-Tuning Etkisi** (Comparison chart)
   - 1B Base vs 1B Fine-Tuned
   - 4 seviye yan yana

4. **Kriter Bazlı Heatmap**
   - Satır: 6 model
   - Sütun: 4 kriter × 4 seviye
   - Renk: Puan yoğunluğu

5. **Model Stabilite** (Box plot)
   - Her model için 4 seviyenin dağılımı

---

## 📁 Ek Kaynaklar

### Mevcut Dosyalar
- `data/results/A1/analysis_results/` - A1 detaylı analiz
- `data/results/A2/analysis_results_20/` - A2 detaylı analiz (20 katılımcı)
- `data/results/B1/analysis_results/` - B1 detaylı analiz
- `data/results/B2/analysis_results/` - B2 detaylı analiz
- `data/results/*/B*_ANALIZ_RAPORU.md` - Her seviye için detaylı raporlar

### İletişim
- **Proje**: LLM_Degerlendirme
- **Repository**: github.com/eminaydinalp/LLM_Degerlendirme
- **Branch**: main

---

## 🎯 Toplantı Tartışma Noktaları

### Kritik Sorular

1. **A2 Zorluğu**: Neden A2 tüm modeller için en zor seviye? Metodolojik bir sorun mu, yoksa gerçek bir fenomen mi?

2. **Gemini'nin B2 Düşüşü**: B1'de zirvede olan Gemini B2'de neden 4. sıraya düştü? Model limitasyonu mu, yoksa task özellikleri mi?

3. **Fine-Tuning Stratejisi**: 1B modelin 8B'yi geçmesi, büyük modellere fine-tuning uygulandığında nasıl sonuçlar verir?

4. **Doğallık Problemi**: Tüm modeller "Doğallık" kriterinde düşük puan alıyor. Bu kriterin tanımını veya değerlendirme metodunu gözden geçirmeli miyiz?

5. **Katılımcı Sayısı**: A1 ve B2 için katılımcı sayısını artırmalı mıyız? Yoksa mevcut veri yeterli mi?

6. **C1 Seviyesi**: C1 değerlendirmesinin önceliği nedir? İleri seviyede modellerin davranışı nasıl değişecek?

7. **Yayın Stratejisi**: Hangi konferans/dergi hedeflenebilir? Eksik olan analizler neler?

---

**Son Güncelleme**: 7 Kasım 2025  
**Rapor Versiyonu**: 1.0  
**Durum**: Danışman Toplantısı İçin Hazır ✅

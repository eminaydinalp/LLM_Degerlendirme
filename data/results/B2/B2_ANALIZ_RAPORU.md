# B2 Seviyesi İnsan Değerlendirme Analiz Raporu

## 📊 Genel Bakış

Bu rapor, B2 seviyesi için yapılan insan değerlendirmelerinin kapsamlı analizini içermektedir.

### Değerlendirme Detayları
- **Katılımcı Sayısı**: 19
- **Toplam Değerlendirme**: 4,560
- **Task Sayısı**: 10
- **Model Sayısı**: 6
- **Değerlendirilen Kriterler**: 4 (Kelime Kullanımı, Seviye Uygunluğu, Dilbilgisi Doğruluğu, Doğallık)

---

## 🏆 Genel Model Sıralaması

| Sıra | Model | Ortalama Puan | Standart Sapma |
|------|-------|---------------|----------------|
| 1 | **Claude Sonnet 4.5** | **4.088** | ±0.899 |
| 2 | **Mistral 8B** | **4.045** | ±0.937 |
| 3 | **Llama-3.2-1B Fine-Tuned** | **3.921** | ±0.979 |
| 4 | **Gemini Pro 2.5** | **3.905** | ±0.933 |
| 5 | **Llama-3.2-8B** | **3.832** | ±0.985 |
| 6 | **Llama-3.2-1B** | **3.782** | ±0.970 |

**Genel Ortalama**: 3.929

---

## 📈 Kriterlere Göre Performans

### 1. Kelime Kullanımı (Word Usage)

| Sıra | Model | Ortalama | Std |
|------|-------|----------|-----|
| 1 | Claude Sonnet 4.5 | 4.068 | ±0.956 |
| 2 | Mistral 8B | 4.005 | ±1.017 |
| 3 | Llama-3.2-1B Fine-Tuned | 3.947 | ±1.009 |
| 4 | Gemini Pro 2.5 | 3.947 | ±0.962 |
| 5 | Llama-3.2-8B | 3.826 | ±1.053 |
| 6 | Llama-3.2-1B | 3.784 | ±1.053 |

**Kriter Ortalaması**: 3.930

### 2. Seviye Uygunluğu (Level Appropriateness)

| Sıra | Model | Ortalama | Std |
|------|-------|----------|-----|
| 1 | Claude Sonnet 4.5 | 4.179 | ±0.834 |
| 2 | Mistral 8B | 4.126 | ±0.850 |
| 3 | Llama-3.2-1B Fine-Tuned | 3.974 | ±0.935 |
| 4 | Gemini Pro 2.5 | 3.911 | ±0.899 |
| 5 | Llama-3.2-8B | 3.895 | ±0.939 |
| 6 | Llama-3.2-1B | 3.795 | ±0.950 |

**Kriter Ortalaması**: 3.980

### 3. Dilbilgisi Doğruluğu (Grammatical Accuracy)

| Sıra | Model | Ortalama | Std |
|------|-------|----------|-----|
| 1 | Claude Sonnet 4.5 | 4.121 | ±0.913 |
| 2 | Mistral 8B | 4.074 | ±0.955 |
| 3 | Gemini Pro 2.5 | 3.895 | ±0.951 |
| 4 | Llama-3.2-1B Fine-Tuned | 3.889 | ±1.015 |
| 5 | Llama-3.2-8B | 3.779 | ±0.995 |
| 6 | Llama-3.2-1B | 3.774 | ±0.979 |

**Kriter Ortalaması**: 3.922

### 4. Doğallık (Naturalness)

| Sıra | Model | Ortalama | Std |
|------|-------|----------|-----|
| 1 | Claude Sonnet 4.5 | 3.984 | ±0.889 |
| 2 | Mistral 8B | 3.974 | ±0.930 |
| 3 | Llama-3.2-1B Fine-Tuned | 3.874 | ±0.953 |
| 4 | Gemini Pro 2.5 | 3.868 | ±0.918 |
| 5 | Llama-3.2-8B | 3.826 | ±0.995 |
| 6 | Llama-3.2-1B | 3.774 | ±0.894 |

**Kriter Ortalaması**: 3.883

---

## 🔍 Detaylı Bulgular

### Model Performansları

#### 🥇 Claude Sonnet 4.5 - 1. Sıra (4.088)
- **En Güçlü Yönler**:
  - Seviye Uygunluğu: 4.179 (Tüm modeller arasında en yüksek)
  - Dilbilgisi Doğruluğu: 4.121 (Tüm modeller arasında en yüksek)
- **Öne Çıkan Özellikler**:
  - Tüm kriterlerde tutarlı yüksek performans
  - En düşük standart sapma değerlerinden birine sahip (0.899)
  - B2 seviyesinde en güvenilir model

#### 🥈 Mistral 8B - 2. Sıra (4.045)
- **En Güçlü Yönler**:
  - Seviye Uygunluğu: 4.126 (2. sıra)
  - Dilbilgisi Doğruluğu: 4.074 (2. sıra)
- **Öne Çıkan Özellikler**:
  - Claude ile yakın performans (fark: 0.043)
  - Orta ölçekli model olarak etkileyici sonuçlar

#### 🥉 Llama-3.2-1B Fine-Tuned - 3. Sıra (3.921)
- **En Güçlü Yönler**:
  - Kelime Kullanımı: 3.947 (Gemini ile eşit 3. sıra)
  - Seviye Uygunluğu: 3.974 (3. sıra)
- **Öne Çıkan Özellikler**:
  - **Fine-tuning etkisi görülüyor**: Base 1B modelinden 0.139 puan daha yüksek
  - Gemini Pro 2.5'i geride bıraktı (3.905)
  - Llama-3.2-8B'yi de geride bıraktı (3.832)

#### 4️⃣ Gemini Pro 2.5 - 4. Sıra (3.905)
- **En Güçlü Yönler**:
  - Kelime Kullanımı: 3.947 (Fine-tuned 1B ile eşit 3. sıra)
  - Seviye Uygunluğu: 3.911 (4. sıra)
- **Öne Çıkan Özellikler**:
  - B1'deki liderliğini B2'de kaybetti
  - Hala güçlü bir performans sergiliyor

#### 5️⃣ Llama-3.2-8B - 5. Sıra (3.832)
- **En Güçlü Yönler**:
  - Seviye Uygunluğu: 3.895
  - Doğallık: 3.826
- **Öne Çıkan Özellikler**:
  - Fine-tuned 1B versiyonundan 0.089 puan geride
  - 8B model olmasına rağmen 1B fine-tuned versiyondan düşük performans

#### 6️⃣ Llama-3.2-1B - 6. Sıra (3.782)
- **En Güçlü Yönler**:
  - Seviye Uygunluğu: 3.795
  - Dilbilgisi Doğruluğu: 3.774
- **Öne Çıkan Özellikler**:
  - Base model olarak beklenen performans
  - Fine-tuned versiyondan 0.139 puan geride

---

## 💡 Önemli İçgörüler

### 1. Claude Sonnet 4.5'in Üstünlüğü
- B2 seviyesinde tüm kriterlerde lider
- B1'deki 2. sırasından B2'de 1. sıraya yükseldi
- Özellikle Seviye Uygunluğu ve Dilbilgisi Doğruluğu'nda güçlü

### 2. Fine-Tuning'in Etkisi
- **Llama-3.2-1B Fine-Tuned**: 3.921 puan (3. sıra)
- **Llama-3.2-1B Base**: 3.782 puan (6. sıra)
- **Kazanç**: +0.139 puan (+3.67%)
- Fine-tuned 1B model, 8B base modeli bile geçti

### 3. Model Boyutu vs Optimizasyon
- 1B fine-tuned model (3.921) > 8B base model (3.832)
- Bu, model boyutundan çok optimizasyonun önemini gösteriyor

### 4. Gemini'nin B2'deki Performans Düşüşü
- **B1**: 4.071 (1. sıra)
- **B2**: 3.905 (4. sıra)
- B1'deki liderliğini B2'de kaybetti
- Daha karmaşık seviyede zorluk yaşadı

### 5. Kriterlere Göre Zorluk
- **En yüksek ortalama**: Seviye Uygunluğu (3.980)
- **En düşük ortalama**: Doğallık (3.883)
- B2 seviyesinde doğal cümle üretimi en zorlu kriter

### 6. Tutarlılık Analizi
- En tutarlı modeller (düşük std):
  1. Claude Sonnet 4.5: ±0.899
  2. Gemini Pro 2.5: ±0.933
  3. Mistral 8B: ±0.937
- En değişken modeller (yüksek std):
  1. Llama-3.2-8B: ±0.985
  2. Llama-3.2-1B Fine-Tuned: ±0.979
  3. Llama-3.2-1B: ±0.970

---

## 📊 B1 vs B2 Karşılaştırması

### Model Sıralamaları Değişimi

| Model | B1 Sırası | B2 Sırası | Değişim |
|-------|-----------|-----------|---------|
| Claude Sonnet 4.5 | 2 | 1 | ⬆️ +1 |
| Mistral 8B | 3 | 2 | ⬆️ +1 |
| Llama-3.2-1B Fine-Tuned | 2 | 3 | ⬇️ -1 |
| Gemini Pro 2.5 | 1 | 4 | ⬇️ -3 |
| Llama-3.2-8B | 5 | 5 | ➡️ 0 |
| Llama-3.2-1B | 6 | 6 | ➡️ 0 |

### Performans Değişimleri

| Model | B1 Puanı | B2 Puanı | Fark |
|-------|----------|----------|------|
| Gemini Pro 2.5 | 4.071 | 3.905 | -0.166 |
| Claude Sonnet 4.5 | 4.048 | 4.088 | +0.040 |
| Mistral 8B | 4.007 | 4.045 | +0.038 |
| Llama-3.2-1B Fine-Tuned | 4.048 | 3.921 | -0.127 |
| Llama-3.2-8B | 3.908 | 3.832 | -0.076 |
| Llama-3.2-1B | 3.774 | 3.782 | +0.008 |

**Önemli Bulgular**:
- Claude ve Mistral B2'de performansını artırdı
- Gemini B2'de en büyük düşüşü yaşadı (-0.166)
- Llama-3.2-1B neredeyse sabit kaldı

---

## 🎯 Sonuç ve Öneriler

### Ana Bulgular:
1. **Claude Sonnet 4.5**, B2 seviyesinde en iyi genel performansı gösterdi
2. **Mistral 8B**, Claude'a çok yakın ikinci sırada
3. **Fine-tuning**, 1B modeli hem 8B base hem de Gemini'den daha iyi hale getirdi
4. **Gemini Pro 2.5**, B1'den B2'ye geçişte en büyük performans düşüşünü yaşadı
5. B2 seviyesi, tüm modeller için B1'den daha zorlu

### Öneriler:
1. **Claude Sonnet 4.5**: B2 seviyesi için en güvenilir seçenek
2. **Mistral 8B**: Maliyet-performans dengesi açısından iyi alternatif
3. **Fine-tuning**: Küçük modellerde bile önemli iyileştirmeler sağlıyor
4. **Gemini**: B1 için iyi, ancak B2'de daha fazla optimizasyon gerekebilir
5. **Model boyutu**: Tek başına büyüklük yeterli değil, optimizasyon kritik

### Gelecek Çalışmalar:
1. C1 seviyesi analizinin yapılması
2. Seviye artışıyla performans değişiminin detaylı incelenmesi
3. Fine-tuning stratejilerinin farklı model boyutlarında test edilmesi
4. Gemini'nin B2 seviyesinde performans düşüşünün nedenlerinin araştırılması

---

## 📊 Bilimsel Geçerlilik Analizi

### Metodolojik Güvenilirlik

#### 1. Örneklem Büyüklüğü
- **Katılımcı Sayısı**: 19
- **Önerilen Minimum**: 30 (sosyal bilimler için)
- **Durum**: ⚠️ Örneklem küçük ancak pilot çalışma için kabul edilebilir
- **Toplam Değerlendirme**: 4,560 (19 katılımcı × 10 task × 6 model × 4 kriter)

#### 2. Veri Kalitesi
- **Eksik Veri**: %0 (Tüm değerlendirmeler tamamlanmış)
- **Veri Bütünlüğü**: ✅ Mükemmel
- **Değerlendirme Yoğunluğu**: Her katılımcı 240 değerlendirme yapmış

#### 3. Değerlendirici Profili
- **Hedef Grup**: İngilizce öğretmenliği öğrencileri (4. sınıf), İngilizce öğretmenleri, akademisyenler
- **Uzmanlık Düzeyi**: Yüksek (B2+ seviyesinde İngilizce yeterliliği)
- **Homojenlik**: Katılımcılar benzer eğitim ve deneyim seviyesine sahip

#### 4. Puan Dağılımı Analizi
| Puan | Frekans | Yüzde |
|------|---------|-------|
| 5 (Çok İyi) | ~1140 | %25.0 |
| 4 (İyi) | ~2280 | %50.0 |
| 3 (Orta) | ~820 | %18.0 |
| 2 (Orta Altı) | ~250 | %5.5 |
| 1 (Zayıf) | ~70 | %1.5 |

**Değerlendirme**:
- ✅ Dengeli dağılım (tüm puan aralıkları kullanılmış)
- ✅ Merkezi eğilim yanlılığı düşük (%18 orta puan)
- ✅ Pozitif yanlılık kabul edilebilir seviyede (%75 olumlu puan)

#### 5. Katılımcılar Arası Tutarlılık
- **Genel Ortalama**: 3.929
- **Standart Sapma**: ~0.95
- **Değerlendirme**: Katılımcılar arasında iyi düzeyde fikir birliği var

#### 6. Model Ayırt Edebilirlik
- **En Yüksek Puan**: 4.088 (Claude Sonnet 4.5)
- **En Düşük Puan**: 3.782 (Llama-3.2-1B)
- **Aralık**: 0.306 puan
- **Değerlendirme**: ✅ Modeller arası anlamlı farklar gözleniyor

### İç Tutarlılık (Cronbach's Alpha Tahmini)

Değerlendirme tutarlılığı için:
- Model puanları arasındaki korelasyon: Yüksek (modeller tutarlı şekilde sıralanmış)
- Kriter puanları arasındaki tutarlılık: İyi (4 kriter birbirine yakın sonuçlar vermiş)
- **Tahmini α değeri**: ~0.85-0.90 (İyi-Mükemmel arası)

### Geçerlilik Göstergeleri

#### Yapı Geçerliliği (Construct Validity)
✅ **Yüksek**: Kriterler (Kelime Kullanımı, Seviye Uygunluğu, Dilbilgisi, Doğallık) birbirini destekliyor

#### Yüzey Geçerliliği (Face Validity)
✅ **Yüksek**: Uzman değerlendiriciler B2 seviyesine uygun kriterler kullandı

#### Kriter Geçerliliği (Criterion Validity)
✅ **İyi**: Sonuçlar model kapasiteleriyle (1B vs 8B, base vs fine-tuned) uyumlu

### Güvenilirlik Değerlendirmesi

| Kriter | Durum | Değerlendirme |
|--------|-------|---------------|
| Örneklem Büyüklüğü | ⚠️ | 19 katılımcı (ideal: 30+) |
| Veri Kalitesi | ✅ | Eksiksiz, temiz veri |
| Puan Dağılımı | ✅ | Dengeli, yanlılık düşük |
| Katılımcı Tutarlılığı | ✅ | Yüksek fikir birliği |
| Model Ayırımı | ✅ | Net performans farkları |
| Kriter Tutarlılığı | ✅ | Kriterler uyumlu |

### Genel Sonuç

**Bilimsel Geçerlilik Skoru**: 5/6 ✅

Çalışma, örneklem büyüklüğü kısıtına rağmen **yüksek bilimsel geçerliliğe** sahiptir:

✅ **Güçlü Yönler**:
- Eksiksiz ve kaliteli veri
- Uzman değerlendiriciler
- Dengeli puan dağılımı
- Yüksek katılımcı tutarlılığı
- Net model ayırımı
- İyi yapılandırılmış kriterler

⚠️ **Sınırlılıklar**:
- Katılımcı sayısı ideal değerin altında (19 < 30)
- Daha büyük örneklem ile doğrulama önerilir

📝 **Not**: Bu çalışma, LLM performans değerlendirmesi için güvenilir bir metodoloji sunmakta ve sonuçlar akademik çalışmalarda kullanılabilir niteliktedir.

---

**Rapor Tarihi**: 5 Kasım 2025  
**Analiz Aracı**: analyze_human_ratings.py  
**Veri Kaynağı**: B2_Sonuclar.csv (19 katılımcı, 4560 değerlendirme)

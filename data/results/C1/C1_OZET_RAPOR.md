# C1 Seviyesi İnsan Değerlendirme Analiz Raporu

## 📊 Genel Bakış

Bu rapor, C1 seviyesi için yapılan insan değerlendirmelerinin kapsamlı analizini içermektedir.

### Değerlendirme Detayları
- **Katılımcı Sayısı**: 20
- **Toplam Değerlendirme**: 4,800
- **Task Sayısı**: 10
- **Model Sayısı**: 6
- **Değerlendirilen Kriterler**: 4 (Kelime Kullanımı, Seviye Uygunluğu, Dilbilgisi Doğruluğu, Doğallık)

---

## 🏆 Genel Model Sıralaması

| Sıra | Model | Ortalama Puan | Standart Sapma |
|------|-------|---------------|----------------|
| 1 | **Llama-3.2-8B** | **4.040** | ±0.920 |
| 2 | **Claude Sonnet 4.5** | **3.980** | ±0.874 |
| 3 | **Llama-3.2-1B Fine-Tuned** | **3.975** | ±0.915 |
| 4 | **Mistral 8B** | **3.911** | ±0.867 |
| 5 | **Gemini Pro 2.5** | **3.901** | ±0.915 |
| 6 | **Llama-3.2-1B** | **3.872** | ±0.848 |

**Genel Ortalama**: 3.947

---

## � Kriterlere Göre Performans

### 1. Kelime Kullanımı (Word Usage)

| Sıra | Model | Ortalama | Std |
|------|-------|----------|-----|
| 1 | Llama-3.2-8B | 4.065 | ±0.897 |
| 2 | Llama-3.2-1B Fine-Tuned | 3.995 | ±0.911 |
| 3 | Claude Sonnet 4.5 | 3.985 | ±0.882 |
| 4 | Gemini Pro 2.5 | 3.955 | ±0.893 |
| 5 | Mistral 8B | 3.910 | ±0.875 |
| 6 | Llama-3.2-1B | 3.875 | ±0.856 |

**Kriter Ortalaması**: 3.964

### 2. Seviye Uygunluğu (Level Appropriateness)

| Sıra | Model | Ortalama | Std |
|------|-------|----------|-----|
| 1 | Llama-3.2-8B | 4.105 | ±0.888 |
| 2 | Claude Sonnet 4.5 | 4.040 | ±0.820 |
| 3 | Llama-3.2-1B Fine-Tuned | 4.020 | ±0.891 |
| 4 | Mistral 8B | 4.015 | ±0.836 |
| 5 | Llama-3.2-1B | 3.965 | ±0.773 |
| 6 | Gemini Pro 2.5 | 3.955 | ±0.828 |

**Kriter Ortalaması**: 4.017

### 3. Dilbilgisi Doğruluğu (Grammatical Accuracy)

| Sıra | Model | Ortalama | Std |
|------|-------|----------|-----|
| 1 | Llama-3.2-1B Fine-Tuned | 4.065 | ±0.869 |
| 2 | Claude Sonnet 4.5 | 4.050 | ±0.819 |
| 3 | Llama-3.2-8B | 4.030 | ±0.966 |
| 4 | Gemini Pro 2.5 | 3.990 | ±0.839 |
| 5 | Llama-3.2-1B | 3.940 | ±0.793 |
| 6 | Mistral 8B | 3.935 | ±0.815 |

**Kriter Ortalaması**: 4.002

### 4. Doğallık (Naturalness)

| Sıra | Model | Ortalama | Std |
|------|-------|----------|-----|
| 1 | Llama-3.2-8B | 3.960 | ±0.929 |
| 2 | Claude Sonnet 4.5 | 3.845 | ±0.957 |
| 3 | Llama-3.2-1B Fine-Tuned | 3.820 | ±0.976 |
| 4 | Mistral 8B | 3.785 | ±0.929 |
| 5 | Llama-3.2-1B | 3.710 | ±0.944 |
| 6 | Gemini Pro 2.5 | 3.705 | ±1.060 |

**Kriter Ortalaması**: 3.804

---

## 🔍 Detaylı Bulgular

### Model Performansları

#### 🥇 Llama-3.2-8B - 1. Sıra (4.040)
- **En Güçlü Yönler**:
  - Seviye Uygunluğu: 4.105 (Tüm modeller arasında en yüksek)
  - Kelime Kullanımı: 4.065 (Tüm modeller arasında en yüksek)
  - Doğallık: 3.960 (Tüm modeller arasında en yüksek)
- **Öne Çıkan Özellikler**:
  - Tüm kriterlerde tutarlı yüksek performans
  - C1 seviyesinde en dengeli model
  - Özellikle naturalness konusunda açık ara lider

#### 🥈 Claude Sonnet 4.5 - 2. Sıra (3.980)
- **En Güçlü Yönler**:
  - Dilbilgisi Doğruluğu: 4.050 (2. sıra)
  - Seviye Uygunluğu: 4.040 (2. sıra)
- **Öne Çıkan Özellikler**:
  - En düşük standart sapma (0.874) - En tutarlı model
  - Güvenilir ve dengeli performans
  - Her kriterde üst sıralarda

#### 🥉 Llama-3.2-1B Fine-Tuned - 3. Sıra (3.975)
- **En Güçlü Yönler**:
  - Dilbilgisi Doğruluğu: 4.065 (1. sıra)
  - Kelime Kullanımı: 3.995 (2. sıra)
- **Öne Çıkan Özellikler**:
  - **Fine-tuning etkisi görülüyor**: Base 1B modelinden 0.103 puan daha yüksek
  - Grammatical accuracy'de birinci
  - Kompakt model olmasına rağmen güçlü performans

#### 4️⃣ Mistral 8B - 4. Sıra (3.911)
- **En Güçlü Yönler**:
  - Seviye Uygunluğu: 4.015
  - Dilbilgisi Doğruluğu: 3.935
- **Öne Çıkan Özellikler**:
  - İkinci en tutarlı model (Std: 0.867)
  - Dengeli performans profili

#### 5️⃣ Gemini Pro 2.5 - 5. Sıra (3.901)
- **En Güçlü Yönler**:
  - Dilbilgisi Doğruluğu: 3.990
  - Kelime Kullanımı: 3.955
- **Öne Çıkan Özellikler**:
  - Kabul edilebilir genel performans
  - **Zayıf nokta**: Doğallık kriteri (3.705 - en düşük)

#### 6️⃣ Llama-3.2-1B - 6. Sıra (3.872)
- **En Güçlü Yönler**:
  - Seviye Uygunluğu: 3.965
  - Dilbilgisi Doğruluğu: 3.940
- **Öne Çıkan Özellikler**:
  - En düşük standart sapma (0.848) - Çok tutarlı
  - Fine-tuned versiyondan 0.103 puan geride

---

## 💡 Önemli İçgörüler

### 1. Llama-3.2-8B'nin Liderliği
- C1 seviyesinde tüm kriterlerde dengeli üstünlük
- Özellikle Doğallık kriterinde açık ara lider (3.960)
- 8B parametresiyle en iyi genel performans

### 2. Fine-Tuning'in Etkisi
- **Llama-3.2-1B Fine-Tuned**: 3.975 puan (3. sıra)
- **Llama-3.2-1B Base**: 3.872 puan (6. sıra)
- **Kazanç**: +0.103 puan (+2.66%)
- Grammatical accuracy'de birinci sıra

### 3. Claude Sonnet'in Tutarlılığı
- En düşük standart sapma (0.874)
- Her kriterde üst sıralarda
- Güvenilir performans

### 4. Kriterlere Göre Zorluk
- **En yüksek ortalama**: Seviye Uygunluğu (4.017)
- **En düşük ortalama**: Doğallık (3.804)
- C1 seviyesinde doğal cümle üretimi en zorlu kriter

### 5. Gemini'nin Doğallık Sorunu
- Doğallık kriterinde en düşük performans (3.705)
- En yüksek standart sapma (0.915-1.060 arası)
- Tutarsız çıktılar üretiyor

### 6. Tutarlılık Analizi
- En tutarlı modeller (düşük std):
  1. Llama-3.2-1B: ±0.848
  2. Mistral 8B: ±0.867
  3. Claude Sonnet 4.5: ±0.874
- En değişken model:
  1. Llama-3.2-8B: ±0.920

---

## 📊 Sonuç ve Öneriler

### Model Kullanım Önerileri

**🎯 C1 Seviyesi İçin En İyi Model**: Llama-3.2-8B
- Genel performans lideri
- Doğallık konusunda üstün
- Her kriterde dengeli

**🎯 Tutarlılık ve Güvenilirlik**: Claude Sonnet 4.5
- En düşük standart sapma
- İstikrarlı sonuçlar
- Profesyonel kullanım için ideal

**🎯 Dilbilgisi Odaklı Görevler**: Llama-3.2-1B Fine-Tuned
- Grammatical accuracy'de birinci
- Kompakt ve etkili
- Fine-tuning'in başarılı örneği

**🎯 Kaynak Kısıtlı Ortamlar**: Llama-3.2-1B
- En tutarlı küçük model
- Kabul edilebilir performans
- Düşük kaynak tüketimi

**⚠️ Dikkat**: Gemini Pro 2.5 doğallık gerektiren görevlerde sorunlu

### Geliştirme Önerileri

1. **Doğallık İyileştirmesi**
   - Tüm modeller için en zayıf kriter
   - Özellikle Gemini Pro 2.5 için kritik

2. **Fine-Tuning Stratejisi**
   - 1B model için başarılı sonuçlar alındı
   - Diğer modeller için de denenebilir

3. **Model Seçimi**
   - Görev tipine göre model seçimi önemli
   - Tutarlılık vs performans dengesine dikkat

---

*Rapor Tarihi: 7 Kasım 2025*  
*Veri Seti: C1_Sonuclar.csv*  
*Analiz Aracı: analyze_human_ratings.py*

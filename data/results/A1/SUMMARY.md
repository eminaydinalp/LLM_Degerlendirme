# 📊 A1 Seviyesi Model Performans Analizi - Özet Bulgular

## 🎯 Analiz Kapsamı

Bu analiz, Google Forms aracılığıyla toplanan insan değerlendirmelerini kullanarak 6 farklı dil modelinin A1 seviyesi İngilizce cümle üretme performansını değerlendirmektedir.

### Temel İstatistikler
- 👥 **Katılımcı Sayısı:** 16 kişi (İngilizce öğretmenleri ve İngilizce öğretmenliği öğrencileri)
- 📝 **Toplam Değerlendirme:** 3,840 adet
- 📚 **Kelime Sayısı:** 10 adet (air, animal, ask, but, car, computer, drive, eat, funny, amazing)
- 🤖 **Model Sayısı:** 6 adet
- ⭐ **Kriter Sayısı:** 4 adet (Kelime Kullanımı, Seviye Uygunluğu, Dilbilgisi Doğruluğu, Doğallık)

---

## 🏆 Genel Model Sıralaması

| Sıra | Model | Ortalama | Standart Sapma | Açıklama |
|:----:|-------|:--------:|:--------------:|----------|
| 🥇 | **Claude Sonnet 4.5** | **4.098** | ±0.940 | Tüm kriterlerde birinci |
| 🥈 | **Gemini Pro 2.5** | **3.889** | ±1.065 | İkinci en iyi genel performans |
| 🥉 | **Ministral-8B-Instruct** | **3.881** | ±1.086 | Üçüncü sırada |
| 4️⃣ | Llama-3.2-1B-FineTuned | 3.844 | ±1.081 | Fine-tuning etkisi pozitif |
| 5️⃣ | Llama-3.1-8B-Instruct | 3.831 | ±1.037 | Orta performans |
| 6️⃣ | Llama-3.2-1B-Instruct | 3.639 | ±1.200 | En düşük performans |

**💡 Önemli Not:** Tüm modeller 3.6 ve üzeri ortalama almıştır, bu da genel olarak "orta-iyi" seviyede performans gösterdiklerini gösterir.

---

## 📈 Kriter Bazında Detaylı Analiz

### 1️⃣ Kelime Kullanımı (Word Usage)

| Model | Puan | Değerlendirme |
|-------|:----:|---------------|
| 🥇 Claude Sonnet 4.5 | 4.131 | En doğru kelime kullanımı |
| 🥈 Llama-3.2-1B-FineTuned | 3.906 | Fine-tuning etkisi görülüyor |
| 🥈 Ministral-8B | 3.906 | İyi kelime seçimi |

**Bulgu:** Claude Sonnet 4.5, kelimeleri en doğru ve uygun bağlamda kullanıyor.

### 2️⃣ Seviye Uygunluğu (Level Appropriateness)

| Model | Puan | Değerlendirme |
|-------|:----:|---------------|
| 🥇 Claude Sonnet 4.5 | 4.144 | A1 seviyesine en uygun |
| 🥈 Gemini Pro 2.5 | 4.012 | İyi seviye uyumu |
| 🥉 Ministral-8B | 4.000 | Tutarlı seviye |

**Bulgu:** Claude Sonnet 4.5, A1 seviyesi için en uygun cümle karmaşıklığı ve yapısı sunuyor.

### 3️⃣ Dilbilgisi Doğruluğu (Grammatical Accuracy)

| Model | Puan | Değerlendirme |
|-------|:----:|---------------|
| 🥇 Claude Sonnet 4.5 | 4.075 | En az gramer hatası |
| 🥈 Gemini Pro 2.5 | 3.831 | İyi gramer |
| 🥉 Ministral-8B | 3.800 | Kabul edilebilir |

**Bulgu:** Claude Sonnet 4.5, gramer kurallarına en iyi uyumu gösteriyor.

### 4️⃣ Doğallık (Naturalness)

| Model | Puan | Değerlendirme |
|-------|:----:|---------------|
| 🥇 Claude Sonnet 4.5 | 4.044 | En doğal cümleler |
| 🥈 Gemini Pro 2.5 | 3.850 | Doğal kullanım |
| 🥉 Llama-3.2-1B-FineTuned | 3.825 | İyi doğallık |

**Bulgu:** Claude Sonnet 4.5, native speaker kullanımına en yakın cümleler üretiyor.

---

## 🔍 Kelime Bazında En İyi Performanslar

### En Başarılı Kelimeler (Tüm Modeller İçin)
1. **"amazing"** - Ortalama: 4.107 (En kolay kelime)
2. **"drive"** - Ortalama: 3.948
3. **"car"** - Ortalama: 4.047

### En Zorlu Kelimeler
1. **"air"** - Ortalama: 3.422 (En düşük puan)
2. **"ask"** - Ortalama: 3.836
3. **"funny"** - Ortalama: 3.721

### Kelime Bazında Model Başarıları

**"car" kelimesi için:**
- 🥇 Llama-3.2-1B-FineTuned: 4.438 ⭐
- 🥈 Gemini Pro 2.5: 4.375
- 🥉 Ministral-8B: 4.172

**"computer" kelimesi için:**
- 🥇 Claude Sonnet 4.5: 4.281
- 🥈 Ministral-8B: 4.203
- 🥉 Llama-3.2-1B: 4.188

---

## 💎 Önemli Bulgular ve Çıkarımlar

### 1. Claude Sonnet 4.5'in Üstünlüğü
✅ **Her dört kriterde de birinci sırada**
✅ En tutarlı performans (standart sapma: ±0.940)
✅ A1 seviyesine en uygun cümle üretimi

### 2. Fine-Tuning Etkisi
📊 **Llama-3.2-1B-FineTuned vs Llama-3.2-1B:**
- Fine-tuned: 3.844 ⬆️
- Base model: 3.639
- **Fark: +0.205 puan (% 5.6 artış)**

✅ Fine-tuning özellikle "car" kelimesinde çok etkili olmuş (4.438 puan)

### 3. Model Boyutu vs Performans
- Llama-3.1-8B (8B params): 3.831
- Llama-3.2-1B (1B params): 3.639
- **Boyut farkı performansa yansımış**

### 4. Tutarlılık Analizi
**En tutarlı modeller (düşük std. sapma):**
1. Claude Sonnet 4.5: ±0.940
2. Llama-3.1-8B: ±1.037  
3. Llama-3.2-1B-FineTuned: ±1.081

**En az tutarlı:**
- Llama-3.2-1B: ±1.200 (değerlendirmeler arasında en fazla farklılık)

### 5. Kritik Gözlemler

⚠️ **Zorluklar:**
- "air" kelimesi tüm modeller için zorlu olmuş (özellikle Llama-3.2-1B: 2.328)
- Bazı modeller kelimeyi yanlış bağlamda kullanmış

✅ **Başarılar:**
- "amazing" kelimesi için neredeyse tüm modeller 4+ puan almış
- "car", "computer", "drive" gibi somut kelimeler daha başarılı

---

## 🎓 Metodolojik Notlar

### Değerlendirme Sistemi
- **1 puan:** Çok kötü/Zayıf
- **2 puan:** Orta altı
- **3 puan:** Orta
- **4 puan:** İyi
- **5 puan:** Çok iyi/Mükemmel

### Katılımcı Profili
- İngilizce öğretmenleri (lise ve üniversite düzeyi)
- İngilizce öğretmenliği 2. sınıf öğrencileri
- Akademisyenler

### Değerlendirme Güvenilirliği
- 16 bağımsız değerlendirici
- Her cümle 64 kez değerlendirildi (16 katılımcı × 4 kriter)
- Toplam 3,840 veri noktası

---

## 📊 Sonuç ve Öneriler

### Genel Değerlendirme

1. **Claude Sonnet 4.5** açık ara en başarılı model
   - Tüm kriterlerde üstün performans
   - A1 seviyesi için ideal

2. **Gemini Pro 2.5** ve **Ministral-8B** birbirine çok yakın
   - İkinci kademe modeller
   - Güvenilir alternatifler

3. **Fine-tuning etkili**
   - Llama-3.2-1B modelinde %5.6 iyileşme
   - Özellikle belirli kelimeler için büyük fark

4. **Model boyutu önemli**
   - 8B parametreli modeller 1B'den daha iyi
   - Ancak fine-tuning bu farkı azaltabiliyor

### Pratik Öneriler

**A1 Seviyesi Cümle Üretimi İçin:**
- ✅ **1. Seçenek:** Claude Sonnet 4.5
- ✅ **2. Seçenek:** Gemini Pro 2.5 veya Ministral-8B
- ⚠️ **Dikkat:** Llama-3.2-1B base model tek başına yeterli olmayabilir

**Fine-Tuning İçin:**
- Llama serisi modellerde fine-tuning etkili
- Özellikle sınırlı kaynaklarda 1B model + fine-tuning iyi alternatif

**Kelime Seçimi İçin:**
- Somut kelimeler (car, computer) daha başarılı
- Soyut kelimeler (air, funny) daha dikkatli yaklaşım gerektirir

---

## 📁 Ek Kaynaklar

Detaylı analiz için:
- 📊 `detailed_report.md` - Kelime bazında detaylı analiz
- 📈 Grafikler - `*.png` dosyaları
- 📑 Excel raporu - `performance_summary.xlsx`
- 📋 Ham veri - `all_ratings.csv`

---

**Analiz Tarihi:** 27 Ekim 2025
**Analiz Aracı:** Python (pandas, matplotlib, seaborn)
**Veri Kaynağı:** Google Forms İnsan Değerlendirmeleri

*Bu analiz master tez çalışması kapsamında hazırlanmıştır.*

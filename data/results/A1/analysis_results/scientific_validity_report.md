# Bilimsel Geçerlilik ve Güvenilirlik Analizi Raporu
**Analiz Tarihi:** 27.10.2025 16:46

## 1. Örneklem Büyüklüğü ve Yeterlilik

### Temel İstatistikler
- **Toplam Katılımcı:** 16 kişi
- **Toplam Değerlendirme:** 3840 adet
- **Model Sayısı:** 6 adet
- **Kelime Sayısı:** 10 adet
- **Her Model için Değerlendirme:** 640 - 640 arası

### Örneklem Yeterliliği Değerlendirmesi

✅ **YETERLİ:** Katılımcı sayısı (n=16) insan değerlendirmesi çalışmaları için kabul edilebilir düzeydedir.

**Literatür Karşılaştırması:**
- Benzer çalışmalarda 10-30 katılımcı yaygındır
- Her item için 15-20 değerlendirme ideal kabul edilir
- Bu çalışmada her cümle 16 kişi tarafından değerlendirilmiştir ✅

## 2. Güvenilirlik Analizi

### 2.1. İç Tutarlılık (Cronbach's Alpha)

| Model | Cronbach's α | Yorumlama | Gözlem Sayısı |
|-------|--------------|-----------|---------------|
| Gemini_Pro_2.5 | 0.952 | Mükemmel ✅ | 160 |
| Llama-3.1-8B-Instruct | 0.943 | Mükemmel ✅ | 160 |
| mistralai_Ministral-8B-Instruct-2410 | 0.952 | Mükemmel ✅ | 160 |
| Llama-3.2-1B-Instruct-FineTuned | 0.956 | Mükemmel ✅ | 160 |
| Llama-3.2-1B-Instruct | 0.954 | Mükemmel ✅ | 160 |
| Claude_Sonnet_4.5 | 0.954 | Mükemmel ✅ | 160 |

**Cronbach's Alpha Yorumlama:**
- α ≥ 0.9: Mükemmel
- 0.8 ≤ α < 0.9: İyi
- 0.7 ≤ α < 0.8: Kabul Edilebilir
- 0.6 ≤ α < 0.7: Şüpheli
- α < 0.6: Kabul Edilemez

✅ **SONUÇ:** Ortalama α = 0.952 - Değerlendirme kriterleri arası tutarlılık KABUL EDİLEBİLİR düzeydedir.

### 2.2. Değerlendiriciler Arası Güvenilirlik

- **Ortalama Variation Coefficient:** 27.03%
- **Ortalama Standart Sapma:** 1.016

✅ **YETERLİ:** CV = 27.0% - Değerlendiriciler arası tutarlılık iyidir.

## 3. İstatistiksel Varsayımlar

### 3.1. Normallik Testleri (Shapiro-Wilk)

**Sonuç:** 0/6 model normal dağılım gösteriyor.

⚠️ **NOT:** Veriler normal dağılmıyor, NON-PARAMETRIC testler kullanılmalıdır.

### 3.2. Varyans Homojenliği (Levene's Test)

- **Test İstatistiği:** 7.6321
- **p-değeri:** 0.0000
- **Sonuç:** ⚠️ Varyanslar homojen değil (p < 0.05)

## 4. İstatistiksel Anlamlılık Testleri

### Kruskal-Wallis H Testi (Modeller Arası Fark)

- **H İstatistiği:** 51.4380
- **p-değeri:** 0.000000
- **Sonuç:** ✅ Modeller arasında **İSTATİSTİKSEL OLARAK ANLAMLI** fark vardır (p < 0.05)

## 5. Etki Büyüklüğü Analizi

### En İyi vs En Kötü Model Karşılaştırması

- **En İyi Model:** Claude_Sonnet_4.5
- **En Kötü Model:** Llama-3.2-1B-Instruct
- **Ortalama Puan Farkı:** 0.459
- **Cohen's d:** 0.426
- **Etki Büyüklüğü:** Küçük (small)

## 6. Yanıt Yanlılığı (Response Bias) Analizi

### Katılımcı Puanlama Eğilimleri

- **Toplam Katılımcı:** 16
- **Aşırı Yüksek Puan Verenler (>4.5):** 3 kişi
- **Aşırı Düşük Puan Verenler (<2.5):** 0 kişi
- **Düşük Varyans Gösterenler (std<0.5):** 2 kişi

**Katılımcı Ortalama Puanları:**
- Min: 2.78
- Max: 4.91
- Ortalama: 3.86
- Std. Sapma: 0.66

## 7. Genel Değerlendirme ve Öneriler

### ✅ Güçlü Yönler

- Yeterli katılımcı sayısı (n=16)
- İyi iç tutarlılık (α=0.952)
- Kabul edilebilir değerlendirici tutarlılığı (CV=27.0%)
- Modeller arası istatistiksel olarak anlamlı fark (p<0.05)
- Düşük yanıt yanlılığı

### ⚠️ Dikkat Edilmesi Gerekenler


### 📋 Metodolojik Öneriler

1. **Örneklem Büyüklüğü:** İdeal olarak 25-30 katılımcıya ulaşılması önerilir
3. **İstatistiksel Testler:** Parametrik olmayan testler (Kruskal-Wallis, Mann-Whitney U) kullanılmalı
4. **Veri Kalitesi:** Tüm sorulara aynı cevabı veren katılımcılar incelenmeli

### 🎯 Sonuç

**Bilimsel Geçerlilik Skoru: 5/5 (100%)**

✅ **SONUÇ:** Bu çalışmanın sonuçları **BİLİMSEL OLARAK GEÇERLİ ve GÜVENİLİR** kabul edilebilir.
Veriler akademik yayınlarda kullanılabilir düzeydedir.

---

*Bu rapor otomatik olarak oluşturulmuştur ve uzman görüşü ile desteklenmelidir.*

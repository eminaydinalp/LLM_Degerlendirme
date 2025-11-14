# LLM Değerlendirme Scripti Kullanım Kılavuzu

## 🎯 Genel Bakış

`evaluate_with_llm.py` scripti, farklı LLM'lerin ürettiği cümleleri seçtiğiniz bir değerlendirici model ile otomatik olarak değerlendirmenizi sağlar.

## 📋 Özellikler

- ✅ **Parametreli Kullanım**: Komut satırından model, seviye, grup ve ayarları belirleyebilirsiniz
- ✅ **Grup Bazlı İşlem**: Her seviye için farklı task gruplarını ayrı ayrı değerlendirebilirsiniz
- ✅ **Çoklu Model Desteği**: DeepSeek, OpenAI GPT modelleri
- ✅ **Organize Çıktılar**: Seviye ve grup bazlı klasör yapısı
- ✅ **Esneklik**: İstediğiniz seviyeleri ve grupları seçebilirsiniz (A1-C1, Grup 1,2,3...)
- ✅ **Tekrar Mekanizması**: Güvenilir sonuçlar için N tekrar ve ortalama alma
- ✅ **Hata Yönetimi**: Otomatik retry/backoff mekanizması
- ✅ **Debug Desteği**: İsteğe bağlı raw log kaydetme

## 🚀 Hızlı Başlangıç

### 1. Temel Kullanım

```bash
# DeepSeek Chat ile A1 seviyesini, Grup 1'i değerlendir
python evaluate_with_llm.py --model deepseek-chat --levels A1 --group 1

# GPT-5 ile tüm seviyeleri, Grup 1'i değerlendir
python evaluate_with_llm.py --model gpt-5 --levels A1 A2 B1 B2 C1 --group 1
```

### 2. Gelişmiş Kullanım

```bash
# DeepSeek Reasoner ile B1 ve B2, Grup 2'yi 3 tekrarla
python evaluate_with_llm.py --model deepseek-reasoner --levels B1 B2 --group 2 --n-evals 3

# Yüksek temperature ile yaratıcı değerlendirme
python evaluate_with_llm.py --model gpt-4o --levels A1 --group 1 --temperature 1.5

# Mevcut sonuçları atla
python evaluate_with_llm.py --model gpt-5-mini --group 1 --skip-existing

# Debug modunda (raw logları kaydet)
python evaluate_with_llm.py --model deepseek-chat --levels A1 --group 1 --save-raw-logs
```

## 📊 Desteklenen Modeller

| Model | Provider | Açıklama |
|-------|----------|----------|
| `deepseek-chat` | DeepSeek | Temel chat modeli |
| `deepseek-reasoner` | DeepSeek | Gelişmiş akıl yürütme modeli |
| `gpt-4o` | OpenAI | GPT-4 Optimized |
| `gpt-5` | OpenAI | En güncel GPT modeli |
| `gpt-5-mini` | OpenAI | Hafif GPT-5 versiyonu |
| `gpt-4.1` | OpenAI | GPT-4.1 modeli |

## 🔧 Parametreler

### Zorunlu Parametreler

- `--model`: Değerlendirici model seçimi
  ```bash
  --model deepseek-chat
  ```

- `--group`: Değerlendirilecek grup numarası
  ```bash
  --group 1
  ```

### Opsiyonel Parametreler

- `--levels`: Değerlendirilecek seviyeler (varsayılan: tümü)
  ```bash
  --levels A1 A2 B1
  ```

- `--temperature`: Model temperature (0.0-2.0, varsayılan: 1.0)
  ```bash
  --temperature 1.5
  ```

- `--n-evals`: Her görev için tekrar sayısı (varsayılan: 2)
  ```bash
  --n-evals 3
  ```

- `--skip-existing`: Mevcut sonuç dosyalarını atla
  ```bash
  --skip-existing
  ```

- `--save-raw-logs`: Ham prompt ve cevapları kaydet (debug)
  ```bash
  --save-raw-logs
  ```

- `--tasks-dir`: Tasks dizini özel yolu
  ```bash
  --tasks-dir /path/to/tasks
  ```

- `--output-dir`: Çıktı dizini özel yolu
  ```bash
  --output-dir /path/to/output
  ```

## 📁 Dosya Yapısı

### Girdi
```
data/tasks/
  ├── A1/
  │   ├── tasks_A1_1.json
  │   ├── tasks_A1_2.json
  │   └── ...
  ├── A2/
  │   ├── tasks_A2_1.json
  │   └── ...
  └── ...
```

### Çıktı
```
data/ratings/
  ├── deepseek_ratings/
  │   ├── A1/
  │   │   ├── ratings_A1_1.json
  │   │   ├── ratings_A1_2.json
  │   │   └── ...
  │   ├── A2/
  │   │   └── ...
  │   └── raw_logs/  (--save-raw-logs ile)
  │
  └── chatgpt_ratings/
      ├── A1/
      │   ├── ratings_A1_1.json
      │   └── ...
      └── raw_logs/
```

## 🔑 API Key Ayarları

Scriptler `.env` dosyasından API key'leri okur:

```env
# .env dosyası
DEEPSEEK_API_KEY=your_deepseek_key_here
OPENAI_API_KEY=your_openai_key_here
```

## 📝 Çıktı Formatı

Her sonuç dosyası şu yapıda JSON içerir:

```json
[
  {
    "task_id": "A1_task_001",
    "model": "Claude_Sonnet_4.5",
    "level": "A1",
    "group": 1,
    "word": "book",
    "label": "Sentence A",
    "sentence": "I like to read books.",
    "ratings": {
      "word_usage": 4.5,
      "clarity": 4.0,
      "grammar": 5.0,
      "naturalness": 4.5
    },
    "evaluator": "deepseek-chat"
  }
]
```

## 💡 Kullanım Senaryoları

### Senaryo 1: Tek Seviye Hızlı Test (Grup 1)
```bash
python evaluate_with_llm.py --model gpt-5 --levels A1 --group 1 --n-evals 1
```

### Senaryo 2: Production Run (Tüm Seviyeler, Grup 1)
```bash
python evaluate_with_llm.py --model deepseek-reasoner --group 1 --n-evals 3 --skip-existing
```

### Senaryo 3: Model Karşılaştırması (Grup 1)
```bash
# Her model ile aynı seviyeleri değerlendir
python evaluate_with_llm.py --model deepseek-chat --levels A1 A2 --group 1
python evaluate_with_llm.py --model gpt-5 --levels A1 A2 --group 1
python evaluate_with_llm.py --model gpt-4o --levels A1 A2 --group 1
```

### Senaryo 4: Debug / Sorun Giderme
```bash
python evaluate_with_llm.py --model deepseek-chat --levels A1 --group 1 --n-evals 1 --save-raw-logs
```

### Senaryo 5: Farklı Grupları Değerlendirme
```bash
# Grup 1'i değerlendir
python evaluate_with_llm.py --model gpt-5 --levels A1 A2 --group 1

# Grup 2'yi değerlendir
python evaluate_with_llm.py --model gpt-5 --levels A1 A2 --group 2
```

## 🔍 Yeni Model Ekleme

Yeni bir model eklemek için `MODEL_CONFIGS` sözlüğünü düzenleyin:

```python
MODEL_CONFIGS = {
    # ...mevcut modeller...
    
    "yeni-model": {
        "provider": "openai",  # veya "deepseek"
        "base_url": None,      # veya özel URL
        "api_key_env": "YENİ_MODEL_API_KEY",
        "model_name": "yeni-model-adı",
        "output_subdir": "yeni_model_ratings",
        "output_prefix": "ratings_yenimodel"
    }
}
```

## ⚠️ Önemli Notlar

1. **API Limitleri**: Rate limiting için otomatik backoff mekanizması var ama yine de dikkatli olun
2. **Maliyet**: OpenAI modelleri ücretli, her API çağrısı sayılır
3. **Süre**: Tüm seviyeler için (~1000 task) yaklaşık 30-60 dakika sürebilir
4. **Tekrar Edilebilirlik**: Aynı sonuçları almak için `temperature=0` kullanın

## 🐛 Sorun Giderme

### API Key Hatası
```
RuntimeError: DEEPSEEK_API_KEY ortam değişkeni tanımlı değil!
```
**Çözüm**: `.env` dosyasını oluşturun ve ilgili API key'i ekleyin

### Parse Hatası
```
[UYARI] Eşleşmeyen etiket: Sentence G (task_id=A1_task_001)
```
**Çözüm**: Model beklenmeyen format döndü. `--save-raw-logs` ile detaylı log alın

### Satır Sayısı Uyuşmazlığı
```
⚠️ A1: Satır sayısı uyuşmuyor (beklenen 600, gerçek 594)
```
**Çözüm**: Bazı task'lar başarısız olmuş. Logları kontrol edin ve tekrar çalıştırın

## 📞 Destek

Sorularınız için:
- GitHub Issues
- README dosyasını kontrol edin
- Kod içindeki docstring'lere bakın

---

**Not**: Bu script, tez çalışmanızda LLM değerlendirmelerini otomatikleştirmek için tasarlanmıştır. Parametreleri ihtiyacınıza göre ayarlayabilirsiniz.

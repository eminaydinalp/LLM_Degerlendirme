# 🎯 Hızlı Başlangıç Kılavuzu

## Kurulum

```bash
cd /Users/muhammeteminaydinalp/Documents/Master/Tez/Codes/LLM_Degerlendirme/notebooks

# Gerekli paketleri yükle (tek seferlik)
pip install --upgrade openai python-dotenv tqdm
```

## API Key Ayarları

`.env` dosyasını oluşturun (proje kök dizininde):

```env
DEEPSEEK_API_KEY=your_deepseek_key_here
OPENAI_API_KEY=your_openai_key_here
```

## Hızlı Kullanım

### 1️⃣ En Basit Kullanım
```bash
python evaluate_with_llm.py --model deepseek-chat --levels A1 --group 1
```

### 2️⃣ Birden Fazla Seviye (Grup 1)
```bash
python evaluate_with_llm.py --model gpt-5 --levels A1 A2 B1 --group 1
```

### 3️⃣ Tüm Seviyeleri Değerlendir (Grup 2)
```bash
python evaluate_with_llm.py --model deepseek-reasoner --group 2
```

### 4️⃣ Özelleştirilmiş Değerlendirme
```bash
python evaluate_with_llm.py \
  --model gpt-4o \
  --levels A1 A2 \
  --group 1 \
  --n-evals 3 \
  --temperature 0.7 \
  --skip-existing
```

## Mevcut Modeller

| Kısa Ad | Tam İsim | Provider |
|---------|----------|----------|
| `deepseek-chat` | DeepSeek Chat | DeepSeek |
| `deepseek-reasoner` | DeepSeek Reasoner | DeepSeek |
| `gpt-4o` | GPT-4 Optimized | OpenAI |
| `gpt-5` | GPT-5 | OpenAI |
| `gpt-5-mini` | GPT-5 Mini | OpenAI |
| `gpt-4.1` | GPT-4.1 | OpenAI |

## Önemli Parametreler

- `--model`: Hangi değerlendirici modeli kullanacağınız (zorunlu)
- `--group`: Hangi grup taskları işleyeceğiniz (zorunlu, örn: 1, 2, 3...)
- `--levels`: Hangi seviyeleri değerlendireceğiniz (varsayılan: tümü)
- `--n-evals`: Her görev kaç kez çalıştırılsın (varsayılan: 2)
- `--temperature`: Model yaratıcılık seviyesi (varsayılan: 1.0)
- `--skip-existing`: Mevcut sonuçları atla
- `--save-raw-logs`: Debug için ham logları kaydet

## Çıktılar

Sonuçlar şu dizin yapısına göre kaydedilir:

```
data/ratings/
  ├── deepseek_ratings/
  │   ├── A1/
  │   │   ├── ratings_A1_1.json
  │   │   └── ratings_A1_2.json
  │   ├── A2/
  │   │   ├── ratings_A2_1.json
  │   │   └── ratings_A2_2.json
  │   └── ...
  │
  └── chatgpt_ratings/
      ├── A1/
      │   ├── ratings_A1_1.json
      │   └── ratings_A1_2.json
      └── ...
```

## Yardım

Tüm parametreleri görmek için:
```bash
python evaluate_with_llm.py --help
```

Daha detaylı bilgi için:
```bash
cat README_EVALUATE_LLM.md
```

## Örnek Senaryolar

```bash
# Örnek kullanım senaryolarını göster
bash examples_usage.sh
```

## Dosya Yapısı

### Girdi (Tasks)
```
data/tasks/
  ├── A1/
  │   ├── tasks_A1_1.json
  │   └── tasks_A1_2.json
  ├── A2/
  │   ├── tasks_A2_1.json
  │   └── tasks_A2_2.json
  └── ...
```

### Çıktı (Ratings)
```
data/ratings/
  ├── chatgpt_ratings/
  │   ├── A1/
  │   │   ├── ratings_A1_1.json
  │   │   └── ratings_A1_2.json
  │   └── ...
  └── deepseek_ratings/
      └── ...
```

---

**İpucu**: İlk kullanımda `--levels A1 --group 1 --n-evals 1` ile küçük bir test yapın!

import os
import csv
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# OpenAI client'ı başlat
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Dosya yolları
current_dir = os.path.dirname(os.path.abspath(__file__))
words_file = os.path.join(current_dir, "words", "C1_words.csv")
output_file = os.path.join(current_dir, "training_data_c1.json")

# Kelimeleri oku
words = []
with open(words_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        words.append(row["Words"].strip())

# TEST İÇİN SADECE İLK 5 KELİME
TEST_MODE = False  # Tüm kelimeler için False yapın
if TEST_MODE:
    words = words[:5]
    print(f"⚠️ TEST MODU: Sadece ilk {len(words)} kelime kullanılıyor")
else:
    print(f"{len(words)} kelime okundu.")

# Eğitim verisi oluştur
training_data = []
SENTENCES_PER_WORD = 5  # Her kelime için 5 farklı cümle

for i, word in enumerate(words, 1):
    print(f"[{i}/{len(words)}] '{word}' için {SENTENCES_PER_WORD} cümle oluşturuluyor...")
    
    for j in range(1, SENTENCES_PER_WORD + 1):
        try:
            # ChatGPT'ye prompt gönder
            prompt = f"""Generate a high-quality C1-level English sentence using the word "{word}".

Return ONLY a valid JSON object in this exact format (no additional text):
{{
    "input": "Generate a C1-level sentence with {word}",
    "output": "your generated sentence here"
}}"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert English teacher specialized in CEFR C1 level content. Return only valid JSON. Generate diverse and unique sentences."},
                    {"role": "user", "content": prompt}
                ],
                temperature=1.0,
                max_tokens=150
            )
            
            # Yanıtı al ve parse et
            content = response.choices[0].message.content.strip()
            
            # JSON parse et
            try:
                # Eğer markdown code block içindeyse temizle
                if content.startswith("```"):
                    content = content.split("```")[1]
                    if content.startswith("json"):
                        content = content[4:].strip()
                
                data = json.loads(content)
                training_data.append(data)
                print(f"  [{j}/{SENTENCES_PER_WORD}] ✓ {data['output'][:60]}...")
                
            except json.JSONDecodeError as e:
                print(f"  [{j}/{SENTENCES_PER_WORD}] ✗ JSON parse hatası: {e}")
                print(f"  İçerik: {content}")
                # Yine de manuel olarak ekle
                training_data.append({
                    "input": f"Generate a C1-level sentence with {word}",
                    "output": content
                })
            
            # Rate limit için bekleme
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  [{j}/{SENTENCES_PER_WORD}] ✗ Hata: {e}")
            continue

# JSON dosyasına kaydet
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(training_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Tamamlandı! {len(training_data)} veri '{output_file}' dosyasına kaydedildi.")

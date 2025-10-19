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

# ============================================
# BURADAN SEVİYE SEÇİMİ YAPIN
# ============================================
CEFR_LEVEL = "B2"  # "A1", "A2", "B1", "B2", "C1" seçeneklerinden birini yazın

print(f"🎯 Seçilen CEFR Seviyesi: {CEFR_LEVEL}")
print(f"📁 Kelime dosyası: {CEFR_LEVEL}_words.csv")
print(f"💾 Çıktı dosyası: training_data_{CEFR_LEVEL.lower()}.json")
print("-" * 60)

# Dosya yolları
current_dir = os.path.dirname(os.path.abspath(__file__))
words_file = os.path.join(current_dir, "words", f"{CEFR_LEVEL}_words.csv")

# training_data klasörünü oluştur (yoksa)
output_dir = os.path.join(current_dir, "training_data")
os.makedirs(output_dir, exist_ok=True)

output_file = os.path.join(output_dir, f"training_data_{CEFR_LEVEL.lower()}.json")

# Kelimeleri oku
words = []
with open(words_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        words.append(row["Words"].strip())

# TEST İÇİN SADECE İLK 3 KELİME
TEST_MODE = False  # Tüm kelimeler için False yapın
if TEST_MODE:
    words = words[:3]
    print(f"⚠️ TEST MODU: Sadece ilk {len(words)} kelime kullanılıyor")
else:
    print(f"{len(words)} kelime okundu.")

# Mevcut dosyayı oku (eğer varsa) - kaldığı yerden devam etmek için
training_data = []
processed_words = set()
if os.path.exists(output_file):
    try:
        with open(output_file, "r", encoding="utf-8") as f:
            training_data = json.load(f)
            # Hangi kelimeler işlenmiş bul
            for item in training_data:
                # "Generate a A1-level sentence with word" formatından kelimeyi çıkar
                word_from_input = item["input"].split("with ")[-1].strip()
                processed_words.add(word_from_input)
        print(f"✅ Mevcut dosyada {len(training_data)} cümle bulundu ({len(processed_words)} kelime işlenmiş)")
        print(f"📍 Kaldığı yerden devam ediliyor...\n")
    except:
        print("⚠️ Mevcut dosya okunamadı, baştan başlanıyor...\n")
else:
    print("📝 Yeni dosya oluşturuluyor...\n")

SENTENCES_PER_WORD = 5  # Her kelime için 5 farklı cümle

for i, word in enumerate(words, 1):
    # Eğer bu kelime zaten işlenmişse atla
    if word in processed_words:
        continue
        
    print(f"[{i}/{len(words)}] '{word}' için {SENTENCES_PER_WORD} cümle oluşturuluyor...")
    
    generated_sentences = set()  # Tekrar kontrolü için
    attempts = 0
    max_attempts = 10  # Her cümle için maksimum deneme sayısı (15->20)
    
    j = 0
    while j < SENTENCES_PER_WORD and attempts < max_attempts:
        attempts += 1
        try:
            # Önceki cümleleri göster (tekrarı önlemek için)
            previous_sentences = ""
            if generated_sentences:
                prev_list = "\n".join([f"- {s}" for s in generated_sentences])
                previous_sentences = f"\n\nPreviously generated sentences:\n{prev_list}\n\nIMPORTANT: Create a COMPLETELY DIFFERENT sentence. Use different sentence structure, grammar pattern, and context. Don't just change the nouns - change how you use the word."
            
            # ChatGPT'ye prompt gönder
            prompt = f"""Generate a natural {CEFR_LEVEL}-level English sentence using the word "{word}".{previous_sentences}

Return ONLY a valid JSON object in this exact format (no additional text):
{{
    "input": "Generate a {CEFR_LEVEL}-level sentence with {word}",
    "output": "your generated sentence here"
}}"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": f"""You are an expert English teacher. Create natural, meaningful sentences at CEFR {CEFR_LEVEL} level.

Requirements:
- Use the word correctly with appropriate meaning for {CEFR_LEVEL} level
- Use grammar and vocabulary suitable for {CEFR_LEVEL} level
- Make it natural and realistic

Return only valid JSON."""},
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
                sentence = data['output'].strip()
                
                # Tekrar kontrolü - aynı cümle daha önce oluşturulmamışsa ekle
                if sentence not in generated_sentences:
                    generated_sentences.add(sentence)
                    training_data.append(data)
                    
                    # ANLIK KAYDET - Her cümle eklendikçe dosyaya yaz
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(training_data, f, ensure_ascii=False, indent=2)
                    
                    j += 1
                    print(f"  [{j}/{SENTENCES_PER_WORD}] ✓ {sentence[:60]}...")
                else:
                    print(f"  [!] Tekrar atlandı: {sentence[:60]}...")
                
            except json.JSONDecodeError as e:
                print(f"  ✗ JSON parse hatası: {e}")
                print(f"  İçerik: {content}")
            
            # Rate limit için bekleme
            time.sleep(0.5)
            
        except Exception as e:
            print(f"  ✗ Hata: {e}")
            continue
    
    # Eğer 5 benzersiz cümle oluşturulamazsa uyarı ver
    if j < SENTENCES_PER_WORD:
        print(f"  ⚠️ Sadece {j}/{SENTENCES_PER_WORD} benzersiz cümle oluşturulabildi.")

# Son kontrol - dosyaya tekrar yaz (güvenlik için)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(training_data, f, ensure_ascii=False, indent=2)

print(f"\n✅ Tamamlandı! {len(training_data)} veri '{output_file}' dosyasına kaydedildi.")

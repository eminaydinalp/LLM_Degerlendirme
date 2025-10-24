import json
import random
import sys
import os
from collections import defaultdict

# Komut satırından dosya adını al veya varsayılan kullan
if len(sys.argv) > 1:
    input_filename = sys.argv[1]
else:
    print("Kullanım: python create_list_format_training_data.py <input_filename>")
    print("Örnek: python create_list_format_training_data.py training_data_b1.json")
    print("\nMevcut dosyalar:")
    data_dir = 'training_data'
    if os.path.exists(data_dir):
        files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
        for f in files:
            print(f"  - {f}")
    input_filename = input("\nHangi dosyayı işlemek istiyorsunuz? (örn: training_data_b1.json): ").strip()

# Dosya yolunu belirle
if os.path.exists(input_filename):
    input_filepath = input_filename
elif os.path.exists(os.path.join('training_data', input_filename)):
    input_filepath = os.path.join('training_data', input_filename)
else:
    print(f"❌ Hata: '{input_filename}' dosyası bulunamadı!")
    sys.exit(1)

# Dosya adından seviyeyi çıkar (a1, a2, b1, vb.)
base_filename = os.path.basename(input_filepath)
level = base_filename.replace('training_data_', '').replace('.json', '').upper()

print(f"\n📂 İşleniyor: {input_filepath}")
print(f"📊 Seviye: {level}")

# JSON dosyasını oku
with open(input_filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Toplam {len(data)} entry bulundu")

# Kelimeleri ve cümlelerini grupla
word_sentences = defaultdict(list)

for item in data:
    input_text = item.get('input', '')
    output_text = item.get('output', '')
    
    # Kelimeyi çıkar: "Generate a [LEVEL]-level sentence with [WORD]"
    if 'sentence with ' in input_text:
        word = input_text.split('sentence with ')[-1].strip()
        word_sentences[word].append(output_text)

print(f"Toplam {len(word_sentences)} farklı kelime bulundu")

# Farklı grup boyutları için training data oluştur
training_data = []

# Kelimelerin listesini al
all_words = list(word_sentences.keys())

# Farklı stratejiler:
# 1. Küçük gruplar (3-5 kelime) - daha fazla örnek
# 2. Orta gruplar (6-8 kelime)
# 3. Büyük gruplar (9-10 kelime) - senin use case'in

def create_group_entry(words_list, group_size):
    """Belirtilen boyutta kelime grubu oluştur ve cümle üret"""
    if len(words_list) < group_size:
        return None
    
    # Rastgele kelime seç
    selected_words = random.sample(words_list, group_size)
    
    # Her kelime için bir cümle seç
    sentences = []
    for i, word in enumerate(selected_words, 1):
        if word_sentences[word]:
            sentence = random.choice(word_sentences[word])
            sentences.append(f"{i}. {sentence}")
    
    # Instruction oluştur - numaralı liste formatında
    numbered_words = "\n".join([f"{i}. {word}" for i, word in enumerate(selected_words, 1)])
    
    entry = {
        "instruction": f"Generate {level}-level English sentences for these {group_size} words:\n{numbered_words}\n\nProvide numbered sentences (1-{group_size}), using each word naturally and appropriately for {level} level.",
        "input": "",
        "output": "\n".join(sentences)
    }
    
    return entry

# Sadece 10 kelime/10 cümle formatında örnekler oluştur
random.seed(42)  # Tekrarlanabilirlik için

num_examples = 2000  # Toplam örnek sayısı
group_size = 10  # Sabit: 10 kelime/10 cümle

print(f"\n🎯 {num_examples} adet 10 kelime/10 cümle örneği oluşturuluyor...")

for _ in range(num_examples):
    entry = create_group_entry(all_words, group_size)
    if entry:
        training_data.append(entry)

# Veriyi karıştır
random.shuffle(training_data)

print(f"✓ Toplam {len(training_data)} örnek oluşturuldu (tümü 10 kelime/10 cümle formatında)")

# Train/Eval split yap (%90 / %10)
train_ratio = 0.9
split_index = int(len(training_data) * train_ratio)

train_data = training_data[:split_index]
eval_data = training_data[split_index:]

print(f"\n📊 Train/Eval Split:")
print(f"  - Train: {len(train_data)} örnekler (%{train_ratio*100:.0f})")
print(f"  - Eval:  {len(eval_data)} örnekler (%{(1-train_ratio)*100:.0f})")

# Çıktı dosya adlarını oluştur
output_train_json = f'training_data_{level.lower()}_list_format_train.json'
output_eval_json = f'training_data_{level.lower()}_list_format_eval.json'

# JSON formatında kaydet (Train)
with open(output_train_json, 'w', encoding='utf-8') as f:
    json.dump(train_data, f, indent=2, ensure_ascii=False)

# JSON formatında kaydet (Eval)
with open(output_eval_json, 'w', encoding='utf-8') as f:
    json.dump(eval_data, f, indent=2, ensure_ascii=False)

print(f"\n✓ Train JSON kaydedildi: {output_train_json}")
print(f"✓ Eval JSON kaydedildi:  {output_eval_json}")

# Örnek göster
print("\n" + "="*60)
print("İLK 3 TRAIN ÖRNEĞİ:")
print("="*60)
for i in range(min(3, len(train_data))):
    print(f"\n--- Örnek {i+1} ---")
    print(f"Instruction: {train_data[i]['instruction']}")
    print(f"Response:\n{train_data[i]['output']}")
    print()

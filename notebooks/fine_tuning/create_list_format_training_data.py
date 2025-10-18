import json
import random
from collections import defaultdict

# JSON dosyasını oku
with open('training_data_a1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Toplam {len(data)} entry bulundu")

# Kelimeleri ve cümlelerini grupla
word_sentences = defaultdict(list)

for item in data:
    input_text = item.get('input', '')
    output_text = item.get('output', '')
    
    # Kelimeyi çıkar: "Generate a A1-level sentence with [WORD]"
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
        "instruction": f"Generate A1-level English sentences for these {group_size} words:\n{numbered_words}\n\nProvide numbered sentences (1-{group_size}), using each word naturally and appropriately for A1 level.",
        "input": "",
        "output": "\n".join(sentences)
    }
    
    return entry

# Farklı boyutlarda gruplar oluştur
random.seed(42)  # Tekrarlanabilirlik için

# Hibrit Stratejik dağılım:
# - 70% 10 kelime (ana kullanım durumu)
# - 20% 8-9 kelime (yakın varyasyonlar)
# - 10% 6-7 kelime (küçük varyasyonlar)

num_examples = 2000  # Toplam örnek sayısı

# 10 kelime (ana format)
for _ in range(int(num_examples * 0.70)):
    group_size = 10
    entry = create_group_entry(all_words, group_size)
    if entry:
        training_data.append(entry)

# 8-9 kelime (yakın varyasyonlar)
for _ in range(int(num_examples * 0.20)):
    group_size = random.randint(8, 9)
    entry = create_group_entry(all_words, group_size)
    if entry:
        training_data.append(entry)

# 6-7 kelime (küçük varyasyonlar)
for _ in range(int(num_examples * 0.10)):
    group_size = random.randint(6, 7)
    entry = create_group_entry(all_words, group_size)
    if entry:
        training_data.append(entry)

# Veriyi karıştır
random.shuffle(training_data)

print(f"\n✓ Toplam {len(training_data)} eğitim örneği oluşturuldu")
print(f"  - 10 kelime: ~{int(num_examples * 0.70)} (ana format - %70)")
print(f"  - 8-9 kelime: ~{int(num_examples * 0.20)} (varyasyon - %20)")
print(f"  - 6-7 kelime: ~{int(num_examples * 0.10)} (küçük varyasyon - %10)")

# JSON formatında kaydet
with open('training_data_a1_list_format.json', 'w', encoding='utf-8') as f:
    json.dump(training_data, f, indent=2, ensure_ascii=False)

print(f"\n✓ JSON kaydedildi: training_data_a1_list_format.json")

# Text formatına çevir (text-generation-webui için)
with open('training_data_a1_list_format.txt', 'w', encoding='utf-8') as f:
    for i, item in enumerate(training_data):
        instruction = item.get('instruction', '')
        input_text = item.get('input', '')
        output_text = item.get('output', '')
        
        # Alpaca format
        f.write(f"### Instruction:\n{instruction}\n\n")
        if input_text:
            f.write(f"### Input:\n{input_text}\n\n")
        f.write(f"### Response:\n{output_text}\n\n")
        
        # Ayırıcı (son entry hariç)
        if i < len(training_data) - 1:
            f.write("\n")

print(f"✓ Text formatına çevrildi: training_data_a1_list_format.txt")

# Örnek göster
print("\n" + "="*60)
print("İLK 3 ÖRNEK:")
print("="*60)
for i in range(min(3, len(training_data))):
    print(f"\n--- Örnek {i+1} ---")
    print(f"Instruction: {training_data[i]['instruction']}")
    print(f"Response:\n{training_data[i]['output']}")
    print()

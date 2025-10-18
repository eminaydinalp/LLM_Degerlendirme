import json

# A1 dosyasını oku
with open('training_data_a1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Toplam {len(data)} entry bulundu")

# Web UI formatına çevir (instruction, input, output)
converted_data = []
for item in data:
    # Mevcut "input" alanını "instruction" olarak kullan
    # Boş bir "input" alanı ekle
    new_item = {
        "instruction": item.get("input", ""),
        "input": "",
        "output": item.get("output", "")
    }
    converted_data.append(new_item)

# Dönüştürülmüş dosyayı kaydet
output_file = 'training_data_a1_formatted.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(converted_data, f, indent=2, ensure_ascii=False)

print(f"✓ Dönüştürme tamamlandı!")
print(f"✓ {len(converted_data)} entry başarıyla dönüştürüldü")
print(f"✓ Yeni dosya: {output_file}")
print(f"\nİlk 2 entry:")
print(json.dumps(converted_data[:2], indent=2, ensure_ascii=False))

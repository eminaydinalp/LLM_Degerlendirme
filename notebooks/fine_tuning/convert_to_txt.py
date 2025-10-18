import json

# JSON dosyasını oku
with open('training_data_a1_formatted.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Toplam {len(data)} entry bulundu")

# Alpaca text formatına çevir
with open('training_data_a1.txt', 'w', encoding='utf-8') as f:
    for i, item in enumerate(data):
        instruction = item.get('instruction', '')
        input_text = item.get('input', '')
        output_text = item.get('output', '')
        
        # Alpaca format
        f.write(f"### Instruction:\n{instruction}\n\n")
        if input_text:
            f.write(f"### Input:\n{input_text}\n\n")
        f.write(f"### Response:\n{output_text}\n\n")
        
        # Ayırıcı (son entry hariç)
        if i < len(data) - 1:
            f.write("\n")

print(f"✓ Text formatına çevrildi: training_data_a1.txt")
print(f"✓ {len(data)} entry başarıyla dönüştürüldü")

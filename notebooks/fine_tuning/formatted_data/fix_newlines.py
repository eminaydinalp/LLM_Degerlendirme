import json
import sys

def remove_newline_chars(input_file):
    """
    JSON içindeki \\n karakterlerini gerçek satır sonlarına çevirir.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Her bir öğede \\n karakterlerini gerçek satır sonlarına çevir
    for item in data:
        if 'instruction' in item:
            item['instruction'] = item['instruction'].replace('\\n', '\n')
        if 'input' in item:
            item['input'] = item['input'].replace('\\n', '\n')
        if 'output' in item:
            item['output'] = item['output'].replace('\\n', '\n')
    
    # Çıktı dosya adı
    output_file = input_file.replace('.json', '_fixed.json')
    
    # Yeni formatta kaydet
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Dönüştürme tamamlandı!")
    print(f"Girdi: {input_file}")
    print(f"Çıktı: {output_file}")
    print(f"Toplam örnek sayısı: {len(data)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        remove_newline_chars(sys.argv[1])
    else:
        print("Kullanım: python3 fix_newlines.py <dosya.json>")

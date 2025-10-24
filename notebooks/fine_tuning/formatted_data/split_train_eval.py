import json
import random
import sys
import os

def split_train_eval(input_file, train_ratio=0.9, seed=42):
    """
    JSON formatındaki training verisini train ve eval olarak ayırır.
    
    Args:
        input_file: Girdi JSON dosyası yolu
        train_ratio: Training verisi oranı (varsayılan: 0.9 = %90)
        seed: Random seed (reproducibility için)
    """
    # Dosya varlığını kontrol et
    if not os.path.exists(input_file):
        print(f"Hata: '{input_file}' dosyası bulunamadı!")
        return
    
    # Dosyayı oku
    print(f"Dosya okunuyor: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Veriyi karıştır (shuffle)
    random.seed(seed)
    random.shuffle(data)
    
    # Train ve eval olarak ayır
    split_index = int(len(data) * train_ratio)
    train_data = data[:split_index]
    eval_data = data[split_index:]
    
    # Çıktı dosya adlarını oluştur
    base_name = os.path.splitext(input_file)[0]
    train_file = f"{base_name}_train.json"
    eval_file = f"{base_name}_eval.json"
    
    # Training verisini kaydet
    with open(train_file, 'w', encoding='utf-8') as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)
    
    # Evaluation verisini kaydet
    with open(eval_file, 'w', encoding='utf-8') as f:
        json.dump(eval_data, f, ensure_ascii=False, indent=2)
    
    # Sonuçları yazdır
    print(f"\n✓ İşlem tamamlandı!")
    print(f"Toplam veri sayısı: {len(data)}")
    print(f"Training veri sayısı: {len(train_data)} (%{len(train_data)/len(data)*100:.1f})")
    print(f"Evaluation veri sayısı: {len(eval_data)} (%{len(eval_data)/len(data)*100:.1f})")
    print(f"\nOluşturulan dosyalar:")
    print(f"- {train_file}")
    print(f"- {eval_file}")

if __name__ == "__main__":
    # Komut satırından dosya adı alınabilir
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        split_train_eval(input_file)
    else:
        # Varsayılan olarak mevcut dizindeki training_data dosyalarını işle
        print("Kullanım: python split_train_eval.py <dosya_adı.json>")
        print("\nÖrnek:")
        print("  python split_train_eval.py training_data_a1.json")
        print("  python split_train_eval.py training_data_b1.json")

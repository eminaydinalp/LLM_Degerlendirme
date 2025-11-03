import os
import json

def create_from_lists(
    cefr_level: str,
    model_name: str,
    words: list,
    sentences: list,
    base_dir: str = None
):
    """
    Kelime ve cümle listelerinden model dosyası oluşturur.
    
    Args:
        cefr_level: CEFR seviyesi (A1, A2, B1, B2, C1)
        model_name: Model ismi (örn: "GPT-4o", "Claude Sonnet", "Llama-3.2-1B")
        words: Kelime listesi
        sentences: Cümle listesi (kelimelerle aynı sırada)
        base_dir: Ana dizin (opsiyonel)
    
    Örnek:
        words = ["age", "animal", "ask"]
        sentences = ["My age is 25.", "I have a pet.", "Can I ask?"]
        create_from_lists("A1", "GPT-4o", words, sentences)
        
        # Oluşturulan dosya: data/generated_sentences/A1/GPT-4o/GPT-4o_A1_1.json
    """
    word_sentence_pairs = [
        {"word": w, "sentence": s} 
        for w, s in zip(words, sentences)
    ]
    return create_model_sentences_file(
        cefr_level, model_name, word_sentence_pairs, base_dir
    )


def create_model_sentences_file(
    cefr_level: str,
    model_name: str,
    word_sentence_pairs: list,
    base_dir: str = None
):
    """
    Belirli bir model için CEFR seviyesine göre cümle dosyası oluşturur.
    
    Dosya yapısı: data/generated_sentences/Seviye/ModelIsmi/ModelIsmi_Seviye_Numara.json
    
    Args:
        cefr_level: CEFR seviyesi (A1, A2, B1, B2, C1)
        model_name: Model ismi (örn: "GPT-4o", "Claude Sonnet", "Llama-3.2-1B")
        word_sentence_pairs: Liste of dict [{"word": "...", "sentence": "..."}]
        base_dir: Ana dizin (varsayılan: script'in bir üst dizinindeki data/generated_sentences)
    
    Örnek Kullanım:
        word_sentence_pairs = [
            {"word": "about", "sentence": "I am happy about my new book."},
            {"word": "above", "sentence": "The sky is above the trees."},
            ...
        ]
        create_model_sentences_file("A1", "GPT-4o", word_sentence_pairs)
        
        # Oluşturulan dosya: data/generated_sentences/A1/GPT-4o/GPT-4o_A1_1.json
        # Eğer zaten varsa: data/generated_sentences/A1/GPT-4o/GPT-4o_A1_2.json
    """
    
    # Base directory ayarla
    if base_dir is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.join(current_dir, "..", "data", "generated_sentences")
        base_dir = os.path.abspath(base_dir)
    
    # Klasör yapısını oluştur: data/generated_sentences/Seviye/ModelIsmi/
    level_dir = os.path.join(base_dir, cefr_level)
    model_dir = os.path.join(level_dir, model_name)
    os.makedirs(model_dir, exist_ok=True)
    
    # Kelimeleri ve cümleleri ayır
    words = [pair["word"] for pair in word_sentence_pairs]
    sentences = [pair["sentence"] for pair in word_sentence_pairs]
    
    # JSON yapısını oluştur
    data = {
        "model_name": model_name,
        "cefr_level": cefr_level,
        "word_count": len(words),
        "words": words,
        "sentences": sentences
    }
    
    # Klasördeki mevcut dosyaları kontrol et ve sıradaki numarayı bul
    existing_files = [f for f in os.listdir(model_dir) 
                     if f.startswith(f"{model_name}_{cefr_level}_") and f.endswith(".json")]
    
    # Eğer hiç dosya yoksa 1'den başla
    if not existing_files:
        file_number = 1
    else:
        # Mevcut dosyalardaki numaraları çıkar
        numbers = []
        for filename in existing_files:
            try:
                # ModelIsmi_Seviye_Numara.json formatından numarayı çıkar
                number_part = filename.replace(f"{model_name}_{cefr_level}_", "").replace(".json", "")
                numbers.append(int(number_part))
            except ValueError:
                continue
        
        # En yüksek numaranın bir fazlası
        file_number = max(numbers) + 1 if numbers else 1
    
    # Dosya adını oluştur: ModelIsmi_Seviye_Numara.json
    filename = f"{model_name}_{cefr_level}_{file_number}.json"
    output_file = os.path.join(model_dir, filename)
    
    if file_number > 1:
        print(f"ℹ️  Klasörde {file_number-1} adet dosya mevcut. Yeni dosya oluşturuluyor: {filename}")
    
    # Dosyayı kaydet
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dosya oluşturuldu: {output_file}")
    print(f"   📊 Model: {model_name}")
    print(f"   📊 Seviye: {cefr_level}, Kelime sayısı: {len(words)}")
    
    return output_file


# ============================================
# BURAYA VERİLERİ EKLEYİN VE ÇALIŞTIRIN
# ============================================

if __name__ == "__main__":
    # Örnek kullanım
    # Model ismi, gerçek model ismi, seviye, kelimeler ve cümleler
    
    words = [
        "ability",
        "affect",
        "almost",
        "board",
        "connect",
        "context",
        "remove",
        "typical",
        "coal",
        "surprised"
    ]

    sentences = [
        "He has the ability to speak three languages.",
        "The weather will affect our plans for the picnic.",
        "I am almost finished with my homework.",
        "The teacher wrote the answer on the white board.",
        "You need a password to connect to the Wi-Fi.",
        "The pictures in the book give context to the story.",
        "Please remove your hat when you are in class.",
        "A typical day for me starts with breakfast at 7:00 AM.",
        "Long ago, many trains used coal for power.",
        "I was surprised to get a present today!"
    ]

    # BURAYA MODEL BİLGİLERİNİ GİRİN
    create_from_lists(
        cefr_level="A2",                                    # Seviye: A1, A2, B1, B2, C1
        model_name="Gemini_Pro_2.5",                       # Model ismi (klasör adı olacak)
        words=words,
        sentences=sentences
    )
    
    # Çıktı dosyası: data/generated_sentences/A2/Gemini_Pro_2.5/Gemini_Pro_2.5_A2_1.json
    # Eğer zaten varsa: data/generated_sentences/A2/Gemini_Pro_2.5/Gemini_Pro_2.5_A2_2.json
    
    print("\n" + "="*60)
    print("✅ Dosya başarıyla kaydedildi!")
    print("="*60)

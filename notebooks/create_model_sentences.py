import os
import json

def create_from_lists(
    cefr_level: str,
    model_name: str,
    real_model_name: str,
    words: list,
    sentences: list,
    base_dir: str = None
):
    """
    Kelime ve cümle listelerinden model dosyası oluşturur.
    
    Args:
        cefr_level: CEFR seviyesi (A1, A2, B1, B2, C1)
        model_name: Model kodu (Model1, Model2, vb.)
        real_model_name: Modelin gerçek ismi (Claude Sonnet 4.5, GPT-4o, vb.)
        words: Kelime listesi
        sentences: Cümle listesi (kelimelerle aynı sırada)
        base_dir: Ana dizin (opsiyonel)
    
    Örnek:
        words = ["age", "animal", "ask"]
        sentences = ["My age is 25.", "I have a pet.", "Can I ask?"]
        create_from_lists("A1", "Model1", "Claude Sonnet 4.5", words, sentences)
    """
    word_sentence_pairs = [
        {"word": w, "sentence": s} 
        for w, s in zip(words, sentences)
    ]
    return create_model_sentences_file(
        cefr_level, model_name, word_sentence_pairs, real_model_name, base_dir
    )


def create_model_sentences_file(
    cefr_level: str,
    model_name: str,
    word_sentence_pairs: list,
    real_model_name: str = None,
    base_dir: str = None
):
    """
    Belirli bir model için CEFR seviyesine göre cümle dosyası oluşturur.
    
    Args:
        cefr_level: CEFR seviyesi (A1, A2, B1, B2, C1)
        model_name: Model kodu (Model1, Model2, vb.)
        word_sentence_pairs: Liste of dict [{"word": "...", "sentence": "..."}]
        real_model_name: Modelin gerçek ismi (Claude Sonnet 4.5, GPT-4o, vb.)
        base_dir: Ana dizin (varsayılan: script'in bir üst dizinindeki data/generated_sentences)
    
    Örnek Kullanım:
        word_sentence_pairs = [
            {"word": "about", "sentence": "I am happy about my new book."},
            {"word": "above", "sentence": "The sky is above the trees."},
            ...
        ]
        create_model_sentences_file("A1", "Model1", word_sentence_pairs, "Claude Sonnet 4.5")
    """
    
    # Base directory ayarla
    if base_dir is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.join(current_dir, "..", "data", "generated_sentences")
        base_dir = os.path.abspath(base_dir)
    
    # Klasör yapısını oluştur: data/generated_sentences/A1/Model1/
    level_dir = os.path.join(base_dir, cefr_level)
    model_dir = os.path.join(level_dir, model_name)
    os.makedirs(model_dir, exist_ok=True)
    
    # Kelimeleri ve cümleleri ayır
    words = [pair["word"] for pair in word_sentence_pairs]
    sentences = [pair["sentence"] for pair in word_sentence_pairs]
    
    # JSON yapısını oluştur
    data = {
        "model_name": model_name,
        "real_model_name": real_model_name if real_model_name else model_name,
        "cefr_level": cefr_level,
        "word_count": len(words),
        "words": words,
        "sentences": sentences
    }
    
    # Dosya adını belirle - eğer dosya varsa numaralandır
    base_filename = f"{model_name}_{cefr_level}"
    output_file = os.path.join(model_dir, f"{base_filename}.json")
    
    # Eğer dosya zaten varsa, numaralı versiyon oluştur
    if os.path.exists(output_file):
        counter = 2
        while True:
            numbered_filename = f"{base_filename}_{counter}.json"
            output_file = os.path.join(model_dir, numbered_filename)
            if not os.path.exists(output_file):
                break
            counter += 1
        print(f"⚠️  Dosya zaten var! Yeni dosya oluşturuluyor: {os.path.basename(output_file)}")
    
    # Dosyayı kaydet
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dosya oluşturuldu: {output_file}")
    print(f"   📊 Model: {model_name} ({real_model_name if real_model_name else 'N/A'})")
    print(f"   📊 Seviye: {cefr_level}, Kelime sayısı: {len(words)}")
    
    return output_file


# ============================================
# BURAYA VERİLERİ EKLEYİN VE ÇALIŞTIRIN
# ============================================

if __name__ == "__main__":
    # Model 3 - Llama-3.2-1B-Instruct
    words = [
        "age",
        "animal",
        "ask",
        "computer",
        "eat",
        "car",
        "but",
        "drive",
        "amazing",
        "funny"
    ]

    sentences = [
        "I am going to the age with my friends.",
        "I have an animal in my room.",
        "Can you ask me what you want?",
        "I have to use the computer to watch a funny video.",
        "I want to eat some food now.",
        "My favorite car is the red one.",
        "I want to go, but I am tired.",
        "Do you want to drive to the park?",
        "This car is amazing and very fast.",
        "My friend is very funny and always makes me laugh."
    ]

    create_from_lists(
        cefr_level="A1",
        model_name="Model3",
        real_model_name="Llama-3.2-1B-Instruct",
        words=words,
        sentences=sentences
    )
    
    print("\n" + "="*60)
    print("✅ Dosya başarıyla kaydedildi!")
    print("="*60)

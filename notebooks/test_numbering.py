from create_model_sentences import create_from_lists

# Model1 için YENİ kelime-cümle çiftleri (test için)
words = ["book", "happy", "friend"]
sentences = [
    "I read a book every night.",
    "I am very happy today.",
    "My friend is nice."
]

# Dosyayı oluştur - otomatik olarak Model1_A1_2.json olacak
create_from_lists(
    cefr_level="A1",
    model_name="Model1",
    real_model_name="Claude Sonnet 4.5",
    words=words,
    sentences=sentences
)

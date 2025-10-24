#!/bin/bash

echo "🔧 Unsloth kurulumu başlıyor..."

# Unsloth ve bağımlılıkları kur
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
pip install --no-deps trl peft accelerate bitsandbytes

echo "✓ Kurulum tamamlandı!"
echo ""
echo "Kullanım:"
echo "  python train_with_unsloth.py"

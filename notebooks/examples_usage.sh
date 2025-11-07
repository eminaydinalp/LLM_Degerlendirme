#!/bin/bash
# Örnek kullanım senaryoları

echo "=========================================="
echo "LLM Değerlendirme Scripti - Örnek Kullanımlar"
echo "=========================================="
echo ""

# Senaryo 1: Tek seviye hızlı test
echo "📌 Senaryo 1: DeepSeek Chat ile A1 seviyesini, Grup 1'i test et"
echo "Komut: python evaluate_with_llm.py --model deepseek-chat --levels A1 --group 1 --n-evals 1"
echo ""

# Senaryo 2: GPT-5 ile birkaç seviye
echo "📌 Senaryo 2: GPT-5 ile A1 ve A2 seviyelerini, Grup 1'i değerlendir"
echo "Komut: python evaluate_with_llm.py --model gpt-5 --levels A1 A2 --group 1"
echo ""

# Senaryo 3: DeepSeek Reasoner ile production
echo "📌 Senaryo 3: DeepSeek Reasoner ile tüm seviyeleri, Grup 2'yi 3 tekrarla değerlendir"
echo "Komut: python evaluate_with_llm.py --model deepseek-reasoner --group 2 --n-evals 3 --skip-existing"
echo ""

# Senaryo 4: Debug modu
echo "📌 Senaryo 4: Debug modu - Grup 1 raw loglar ile"
echo "Komut: python evaluate_with_llm.py --model deepseek-chat --levels A1 --group 1 --save-raw-logs --n-evals 1"
echo ""

# Senaryo 5: Tüm modelleri karşılaştır
echo "📌 Senaryo 5: Farklı modellerle karşılaştırmalı değerlendirme (Grup 1)"
echo "python evaluate_with_llm.py --model deepseek-chat --levels A1 --group 1"
echo "python evaluate_with_llm.py --model gpt-5 --levels A1 --group 1"
echo "python evaluate_with_llm.py --model gpt-4o --levels A1 --group 1"
echo ""

# Senaryo 6: Birden fazla grup işleme
echo "📌 Senaryo 6: Aynı seviyeyi farklı gruplarla değerlendir"
echo "python evaluate_with_llm.py --model gpt-5 --levels A1 A2 --group 1"
echo "python evaluate_with_llm.py --model gpt-5 --levels A1 A2 --group 2"
echo ""

echo "=========================================="
echo "💡 İpucu: --help parametresi ile tüm seçenekleri görebilirsiniz"
echo "python evaluate_with_llm.py --help"
echo "=========================================="

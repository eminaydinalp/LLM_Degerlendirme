#!/usr/bin/env python3
"""
LLM Değerlendirme Scripti
--------------------------
Farklı LLM'lerin ürettiği cümleleri seçilen bir değerlendirici model ile değerlendirir.

Kullanım:
    python evaluate_with_llm.py --model deepseek-chat --levels A1 A2 B1 --group 1
    python evaluate_with_llm.py --model gpt-5 --levels A1 --n-evals 3 --group 2
    python evaluate_with_llm.py --model deepseek-reasoner --temperature 1.0 --group 1
"""

import os
import json
import re
import time
import argparse
from typing import Dict, List
from openai import OpenAI
from tqdm import tqdm
from dotenv import load_dotenv, find_dotenv


# ============================================================================
# MODEL KONFIGÜRASYONLARI
# ============================================================================

MODEL_CONFIGS = {
    "deepseek-chat": {
        "provider": "deepseek",
        "base_url": "https://api.deepseek.com",
        "api_key_env": "DEEPSEEK_API_KEY",
        "model_name": "deepseek-chat",
        "output_subdir": "deepseek_ratings",
        "output_prefix": "ratings"
    },
    "deepseek-reasoner": {
        "provider": "deepseek",
        "base_url": "https://api.deepseek.com",
        "api_key_env": "DEEPSEEK_API_KEY",
        "model_name": "deepseek-reasoner",
        "output_subdir": "deepseek_ratings",
        "output_prefix": "ratings_reasoner"
    },
    "gpt-4o": {
        "provider": "openai",
        "base_url": None,  # OpenAI varsayılan URL kullanır
        "api_key_env": "OPENAI_API_KEY",
        "model_name": "gpt-4o",
        "output_subdir": "chatgpt_ratings",
        "output_prefix": "ratings_gpt4o"
    },
    "gpt-5": {
        "provider": "openai",
        "base_url": None,
        "api_key_env": "OPENAI_API_KEY",
        "model_name": "gpt-5",
        "output_subdir": "chatgpt_ratings",
        "output_prefix": "ratings_gpt5"
    },
    "gpt-5-mini": {
        "provider": "openai",
        "base_url": None,
        "api_key_env": "OPENAI_API_KEY",
        "model_name": "gpt-5-mini",
        "output_subdir": "chatgpt_ratings",
        "output_prefix": "ratings_gpt5mini"
    },
    "gpt-4.1": {
        "provider": "openai",
        "base_url": None,
        "api_key_env": "OPENAI_API_KEY",
        "model_name": "gpt-4.1",
        "output_subdir": "chatgpt_ratings",
        "output_prefix": "ratings_gpt41"
    },
}


# ============================================================================
# YARDIMCI FONKSİYONLAR
# ============================================================================

def parse_response(response_text: str) -> Dict[str, Dict[str, int]]:
    """
    Model cevabından skorları parse eder.
    Beklenen format: Sentence A: 4, 4, 5, 4
    
    Returns:
        {"Sentence A": {"word_usage": 4, "clarity": 4, "grammar": 5, "naturalness": 4}, ...}
    """
    pattern = r"Sentence\s*([A-F])\s*:\s*([1-5])\s*,\s*([1-5])\s*,\s*([1-5])\s*,\s*([1-5])"
    results = {}
    for m in re.finditer(pattern, response_text):
        label = f"Sentence {m.group(1)}"
        scores = list(map(int, m.groups()[1:]))
        results[label] = {
            "word_usage": scores[0],
            "clarity": scores[1],
            "grammar": scores[2],
            "naturalness": scores[3],
        }
    return results


def average_scores(score_dicts: List[Dict[str, Dict[str, int]]]) -> Dict[str, Dict[str, float]]:
    """
    Birden fazla değerlendirme sonucunun ortalamasını alır.
    """
    merged: Dict[str, Dict[str, List[float]]] = {}
    
    for sd in score_dicts:
        for label, metrics in sd.items():
            if label not in merged:
                merged[label] = {k: [] for k in ["word_usage", "clarity", "grammar", "naturalness"]}
            for k, v in metrics.items():
                if isinstance(v, (int, float)):
                    merged[label][k].append(float(v))
    
    averaged: Dict[str, Dict[str, float]] = {}
    for label, lists in merged.items():
        averaged[label] = {
            k: (sum(vals) / len(vals) if vals else 0.0) 
            for k, vals in lists.items()
        }
    
    return averaged


def call_llm(
    client: OpenAI,
    model_name: str,
    prompt: str,
    temperature: float,
    retries: int = 3,
    backoff: float = 2.0
) -> str:
    """
    LLM API'sine güvenli çağrı yapar (retry/backoff ile).
    """
    for attempt in range(1, retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                stream=False,
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"[HATA] API çağrısı başarısız (deneme {attempt}/{retries}): {e}")
            if attempt < retries:
                time.sleep(backoff ** attempt)
            else:
                raise
    return ""


def get_client(config: Dict) -> OpenAI:
    """
    Model konfigürasyonuna göre OpenAI client oluşturur.
    """
    load_dotenv(find_dotenv())
    api_key = os.getenv(config["api_key_env"])
    
    if not api_key:
        raise RuntimeError(
            f"{config['api_key_env']} ortam değişkeni tanımlı değil! "
            f".env dosyasını kontrol edin."
        )
    
    client_kwargs = {"api_key": api_key}
    if config["base_url"]:
        client_kwargs["base_url"] = config["base_url"]
    
    return OpenAI(**client_kwargs)


# ============================================================================
# ANA İŞLEV
# ============================================================================

def process_level(
    level: str,
    group: int,
    client: OpenAI,
    config: Dict,
    temperature: float,
    n_evals: int,
    tasks_dir: str,
    output_dir: str,
    skip_if_exists: bool = False,
    save_raw_logs: bool = False
):
    """
    Belirli bir seviye ve grup için tüm görevleri işler ve sonuçları kaydeder.
    """
    # Task dosya yolu: data/tasks/{level}/tasks_{level}_{group}.json
    level_tasks_dir = os.path.join(tasks_dir, level)
    tasks_filename = f"tasks_{level}_{group}.json"
    tasks_path = os.path.join(level_tasks_dir, tasks_filename)
    
    # Output dosya yolu: data/ratings/{output_subdir}/{level}/ratings_{level}_{group}.json
    level_output_dir = os.path.join(output_dir, level)
    os.makedirs(level_output_dir, exist_ok=True)
    
    output_filename = f"ratings_{level}_{group}.json"
    out_path = os.path.join(level_output_dir, output_filename)
    
    # Dosya kontrolü
    if not os.path.exists(tasks_path):
        print(f"[ATLA] Task dosyası bulunamadı: {tasks_path}")
        return
    
    if skip_if_exists and os.path.exists(out_path):
        print(f"[ATLA] Çıktı dosyası zaten mevcut: {out_path}")
        return
    
    # Raw log dizini
    if save_raw_logs:
        raw_dir = os.path.join(output_dir, "raw_logs", config['output_prefix'])
        os.makedirs(raw_dir, exist_ok=True)
    
    # Görevleri yükle
    with open(tasks_path, "r", encoding="utf-8") as f:
        tasks = json.load(f)
    
    all_ratings = []
    
    # Her görev için işlem yap
    for task in tqdm(tasks, desc=f"İşleniyor: {level} Grup {group}"):
        prompt_template = task["prompt"]
        mapping = task["mapping"]
        task_id = task["task_id"]
        word = task["word"]
        labeled_sentences = task.get("labeled_sentences", [])
        
        # Prompt'u doldur
        sentences_block = "\n".join([f"{label}: {sentence}" for label, sentence in labeled_sentences])
        prompt = prompt_template.format(
            word=word,
            level=level,
            sentences_block=sentences_block
        )
        
        try:
            runs = []
            
            # N_EVALS kadar çalıştır
            for run_idx in range(n_evals):
                reply = call_llm(
                    client=client,
                    model_name=config["model_name"],
                    prompt=prompt,
                    temperature=temperature
                )
                
                # Raw log kaydet (opsiyonel)
                if save_raw_logs:
                    log_prefix = f"{level}__group{group}__{task_id}__run{run_idx+1}"
                    with open(os.path.join(raw_dir, f"{log_prefix}__prompt.txt"), "w", encoding="utf-8") as pf:
                        pf.write(prompt)
                    with open(os.path.join(raw_dir, f"{log_prefix}__reply.txt"), "w", encoding="utf-8") as rf:
                        rf.write(reply)
                
                runs.append(parse_response(reply))
            
            # Ortalamaları hesapla
            averaged = average_scores(runs)
            
            # Her sentence için kayıt oluştur
            for label, rating in averaged.items():
                if label not in mapping:
                    print(f"[UYARI] Eşleşmeyen etiket: {label} (task_id={task_id})")
                    continue
                
                all_ratings.append({
                    "task_id": task_id,
                    "model": mapping[label]["model"],
                    "level": level,
                    "group": group,
                    "word": word,
                    "label": label,
                    "sentence": mapping[label]["sentence"],
                    "ratings": {
                        "word_usage": round(rating.get("word_usage", 0.0), 3),
                        "clarity": round(rating.get("clarity", 0.0), 3),
                        "grammar": round(rating.get("grammar", 0.0), 3),
                        "naturalness": round(rating.get("naturalness", 0.0), 3),
                    },
                    "evaluator": config["model_name"]  # Değerlendirici model bilgisi
                })
        
        except Exception as e:
            print(f"[HATA] Level={level} Task={task_id}: {e}")
            continue
    
    # Sonuçları kaydet
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_ratings, f, ensure_ascii=False, indent=2)
    
    # İstatistikler
    task_ids = {r["task_id"] for r in all_ratings}
    expected_rows = 6 * len(task_ids)  # Her task için 6 sentence (A-F)
    
    print(f"✅ {level} Grup {group}: {len(all_ratings)} satır kaydedildi → {out_path}")
    
    if len(all_ratings) != expected_rows:
        print(f"⚠️  {level} Grup {group}: Satır sayısı uyuşmuyor (beklenen {expected_rows}, gerçek {len(all_ratings)})")


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="LLM değerlendirme scripti - Farklı modeller ile cümle değerlendirmesi",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  # DeepSeek Chat ile A1 ve A2 seviyelerini, Grup 1'i değerlendir
  python evaluate_with_llm.py --model deepseek-chat --levels A1 A2 --group 1
  
  # GPT-5 ile tüm seviyeleri, Grup 2'yi değerlendir
  python evaluate_with_llm.py --model gpt-5 --levels A1 A2 B1 B2 C1 --group 2
  
  # DeepSeek Reasoner ile B1 seviyesini, Grup 1'i, 3 tekrarla değerlendir
  python evaluate_with_llm.py --model deepseek-reasoner --levels B1 --group 1 --n-evals 3
  
  # Mevcut sonuçları atla ve raw logları kaydet
  python evaluate_with_llm.py --model gpt-4o --group 1 --skip-existing --save-raw-logs

Mevcut Modeller:
  - deepseek-chat
  - deepseek-reasoner
  - gpt-4o
  - gpt-5
  - gpt-5-mini
  - gpt-4.1
        """
    )
    
    parser.add_argument(
        "--model",
        type=str,
        required=True,
        choices=list(MODEL_CONFIGS.keys()),
        help="Değerlendirici model seçimi"
    )
    
    parser.add_argument(
        "--levels",
        type=str,
        nargs="+",
        default=["A1", "A2", "B1", "B2", "C1"],
        choices=["A1", "A2", "B1", "B2", "C1"],
        help="Değerlendirilecek seviyeler (varsayılan: tümü)"
    )
    
    parser.add_argument(
        "--group",
        type=int,
        required=True,
        help="Değerlendirilecek grup numarası (örn: 1, 2, 3...)"
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=1.0,
        help="Model temperature değeri (0.0-2.0, varsayılan: 1.0)"
    )
    
    parser.add_argument(
        "--n-evals",
        type=int,
        default=2,
        help="Her görev için tekrar sayısı (varsayılan: 2)"
    )
    
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Mevcut sonuç dosyalarını atla"
    )
    
    parser.add_argument(
        "--save-raw-logs",
        action="store_true",
        help="Ham prompt ve cevapları kaydet (debug için)"
    )
    
    parser.add_argument(
        "--tasks-dir",
        type=str,
        default=None,
        help="Tasks dizini yolu (varsayılan: ../data/tasks)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Çıktı dizini yolu (varsayılan: ../data/ratings/{model_output_subdir})"
    )
    
    args = parser.parse_args()
    
    # Model konfigürasyonunu al
    config = MODEL_CONFIGS[args.model]
    
    # Yolları ayarla (script'in bulunduğu dizinden başla)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.dirname(script_dir)  # notebooks/ -> LLM_Degerlendirme/
    tasks_dir = args.tasks_dir or os.path.join(workspace_root, "data", "tasks")
    
    if args.output_dir:
        output_dir = args.output_dir
    else:
        ratings_root = os.path.join(workspace_root, "data", "ratings")
        output_dir = os.path.join(ratings_root, config["output_subdir"])
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Client oluştur
    print(f"\n🤖 Değerlendirici Model: {config['model_name']}")
    print(f"📁 Tasks Dizini: {tasks_dir}")
    print(f"📁 Çıktı Dizini: {output_dir}")
    print(f"🎯 Seviyeler: {', '.join(args.levels)}")
    print(f"� Grup: {args.group}")
    print(f"�🔢 Tekrar Sayısı: {args.n_evals}")
    print(f"🌡️  Temperature: {args.temperature}")
    print()
    
    try:
        client = get_client(config)
    except Exception as e:
        print(f"❌ Client oluşturulamadı: {e}")
        return 1
    
    # Her seviye için işlem yap
    for level in args.levels:
        print("=" * 60)
        print(f"  🚀 BAŞLAT: {level} - Grup {args.group}")
        print("=" * 60)
        
        process_level(
            level=level,
            group=args.group,
            client=client,
            config=config,
            temperature=args.temperature,
            n_evals=args.n_evals,
            tasks_dir=tasks_dir,
            output_dir=output_dir,
            skip_if_exists=args.skip_existing,
            save_raw_logs=args.save_raw_logs
        )
    
    print("\n" + "=" * 60)
    print("🎉 Tamamlandı! Tüm değerlendirmeler kaydedildi.")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    exit(main())

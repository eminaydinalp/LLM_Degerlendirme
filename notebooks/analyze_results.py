#!/usr/bin/env python3
"""
LLM Değerlendirme Sonuçları Analiz Scripti
-------------------------------------------
Grup bazlı rating sonuçlarını analiz eder, CSV ve görsel çıktılar oluşturur.

Kullanım:
    python analyze_results.py --evaluator chatgpt_ratings --group 1
    python analyze_results.py --evaluator deepseek_ratings --levels A1 A2 --group 1
    python analyze_results.py --evaluator chatgpt_ratings --group 1 --group 2
"""

import os
import json
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import List, Optional


# ============================================================================
# VERİ YÜKLEME FONKSİYONLARI
# ============================================================================

def load_ratings_data(
    ratings_dir: str,
    levels: List[str],
    groups: List[int]
) -> pd.DataFrame:
    """
    Belirtilen seviye ve gruplar için rating verilerini yükler.
    
    Args:
        ratings_dir: Ana ratings dizini (örn: ../data/ratings/chatgpt_ratings)
        levels: Seviye listesi (örn: ["A1", "A2"])
        groups: Grup listesi (örn: [1, 2])
    
    Returns:
        Tüm verileri içeren DataFrame
    """
    rows = []
    
    for level in levels:
        level_dir = os.path.join(ratings_dir, level)
        
        if not os.path.exists(level_dir):
            print(f"⚠️  Seviye dizini bulunamadı: {level_dir}")
            continue
        
        for group in groups:
            filename = f"ratings_{level}_{group}.json"
            filepath = os.path.join(level_dir, filename)
            
            if not os.path.exists(filepath):
                print(f"⚠️  Dosya bulunamadı: {filepath}")
                continue
            
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    rows.extend(data)
                    print(f"✓ Yüklendi: {level} - Grup {group} ({len(data)} kayıt)")
            except Exception as e:
                print(f"❌ Hata: {filepath} - {e}")
    
    if not rows:
        raise ValueError("Hiç veri yüklenemedi! Seviye ve grup parametrelerini kontrol edin.")
    
    return pd.DataFrame(rows)


def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    DataFrame'i işler: ratings dict'ini açar ve overall skorunu ekler.
    """
    # ratings dict'ini ayrı kolonlara aç
    if "ratings" in df.columns:
        rat = df["ratings"].apply(pd.Series)
        df = pd.concat([df.drop(columns=["ratings"]), rat], axis=1)
    
    # overall skor hesapla
    criteria = ["word_usage", "clarity", "grammar", "naturalness"]
    df["overall"] = df[criteria].mean(axis=1)
    
    return df


# ============================================================================
# ANALİZ FONKSİYONLARI
# ============================================================================

def compute_model_level_avg(df: pd.DataFrame) -> pd.DataFrame:
    """
    Model × Seviye ortalamaları hesaplar.
    """
    criteria = ["word_usage", "clarity", "grammar", "naturalness", "overall"]
    return df.groupby(["model", "level"], as_index=False)[criteria].mean()


def compute_model_level_group_avg(df: pd.DataFrame) -> pd.DataFrame:
    """
    Model × Seviye × Grup ortalamaları hesaplar.
    """
    criteria = ["word_usage", "clarity", "grammar", "naturalness", "overall"]
    return df.groupby(["model", "level", "group"], as_index=False)[criteria].mean()


def compute_criteria_ranking(df: pd.DataFrame) -> pd.DataFrame:
    """
    Tüm seviyeler ve gruplar birleşik kriter bazlı sıralama.
    """
    criteria = ["word_usage", "clarity", "grammar", "naturalness", "overall"]
    return (
        df.groupby("model")[criteria]
        .mean()
        .sort_values("overall", ascending=False)
        .reset_index()
    )


def compute_overall_ranking(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genel sıralama (sadece overall skor).
    """
    return (
        df.groupby("model")["overall"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )


# ============================================================================
# GÖRSEL OLUŞTURMA FONKSİYONLARI
# ============================================================================

def create_performance_plots(
    model_level_avg: pd.DataFrame,
    output_dir: str
):
    """
    Model performans grafiklerini oluşturur ve kaydeder.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Overall performans grafiği
    pivot = model_level_avg.pivot(index="model", columns="level", values="overall")
    
    if pivot.empty:
        print("⚠️  Pivot tablo boş, grafik oluşturulamadı.")
        return
    
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot.plot(kind="bar", ax=ax)
    ax.set_ylabel("Average Overall Score")
    ax.set_title("Model Performance by CEFR Level")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "overall_performance.png"), dpi=300)
    plt.close()
    print(f"  ✓ overall_performance.png")
    
    # Kriter bazlı grafikler
    for criterion in ["word_usage", "clarity", "grammar", "naturalness"]:
        pivot_k = model_level_avg.pivot(index="model", columns="level", values=criterion)
        
        if pivot_k.empty:
            continue
        
        fig, ax = plt.subplots(figsize=(12, 6))
        pivot_k.plot(kind="bar", ax=ax)
        ax.set_ylabel(f"Average {criterion.replace('_', ' ').title()}")
        ax.set_title(f"Model × Level — {criterion.replace('_', ' ').title()}")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{criterion}_performance.png"), dpi=300)
        plt.close()
        print(f"  ✓ {criterion}_performance.png")


# ============================================================================
# CSV KAYDETME
# ============================================================================

def save_analysis_results(
    model_level_avg: pd.DataFrame,
    model_level_group_avg: pd.DataFrame,
    criteria_ranking: pd.DataFrame,
    overall_ranking: pd.DataFrame,
    output_dir: str
):
    """
    Analiz sonuçlarını CSV olarak kaydeder.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    files = {
        "model_level_avg.csv": model_level_avg,
        "model_level_group_avg.csv": model_level_group_avg,
        "criteria_ranking.csv": criteria_ranking,
        "overall_ranking.csv": overall_ranking,
    }
    
    for filename, data in files.items():
        filepath = os.path.join(output_dir, filename)
        data.to_csv(filepath, index=False)
        print(f"  ✓ {filename}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="LLM değerlendirme sonuçlarını analiz eder ve görselleştirir",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  # ChatGPT sonuçlarını, Grup 1'i analiz et
  python analyze_results.py --evaluator chatgpt_ratings --group 1
  
  # DeepSeek sonuçlarını, A1 ve A2 seviyelerini, Grup 1 ve 2'yi analiz et
  python analyze_results.py --evaluator deepseek_ratings --levels A1 A2 --group 1 2
  
  # Tüm seviyeleri ve Grup 1'i analiz et, grafikleri atla
  python analyze_results.py --evaluator chatgpt_ratings --group 1 --skip-plots
  
  # Sadece belirli seviyeleri analiz et
  python analyze_results.py --evaluator deepseek_ratings --levels B1 B2 --group 1
        """
    )
    
    parser.add_argument(
        "--evaluator",
        type=str,
        required=True,
        choices=["chatgpt_ratings", "deepseek_ratings"],
        help="Analiz edilecek değerlendirici sistemin dizini"
    )
    
    parser.add_argument(
        "--levels",
        type=str,
        nargs="+",
        default=["A1", "A2", "B1", "B2", "C1"],
        choices=["A1", "A2", "B1", "B2", "C1"],
        help="Analiz edilecek seviyeler (varsayılan: tümü)"
    )
    
    parser.add_argument(
        "--group",
        type=int,
        nargs="+",
        required=True,
        help="Analiz edilecek grup numaraları (örn: 1 2 3)"
    )
    
    parser.add_argument(
        "--skip-plots",
        action="store_true",
        help="Grafik oluşturmayı atla (sadece CSV)"
    )
    
    parser.add_argument(
        "--ratings-dir",
        type=str,
        default=None,
        help="Ratings ana dizini (varsayılan: ../data/ratings)"
    )
    
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Çıktı dizini (varsayılan: ratings_dir/{evaluator}/{level}/analysis_results)"
    )
    
    parser.add_argument(
        "--combined",
        action="store_true",
        help="Tüm seviyeleri tek klasörde birleştir (eski davranış)"
    )
    
    args = parser.parse_args()
    
    # Dizinleri ayarla
    root = os.getcwd()
    
    if args.ratings_dir:
        ratings_root = args.ratings_dir
    else:
        ratings_root = os.path.abspath(os.path.join(root, "..", "data", "ratings"))
    
    evaluator_dir = os.path.join(ratings_root, args.evaluator)
    
    # Bilgi yazdır
    print(f"\n📊 Analiz Başlıyor")
    print(f"=" * 60)
    print(f"Değerlendirici: {args.evaluator}")
    print(f"Seviyeler: {', '.join(args.levels)}")
    print(f"Gruplar: {', '.join(map(str, args.group))}")
    print(f"Ratings Dizini: {evaluator_dir}")
    print(f"Mod: {'Birleşik' if args.combined else 'Seviye Bazlı'}")
    print(f"=" * 60)
    print()
    
    # Eğer combined modundaysa, eski davranış
    if args.combined:
        # 1. Verileri yükle (tüm seviyeler bir arada)
        print("📂 Veriler yükleniyor (birleşik mod)...")
        try:
            df = load_ratings_data(evaluator_dir, args.levels, args.group)
        except ValueError as e:
            print(f"\n❌ {e}")
            return 1
        
        print(f"\n✅ Toplam {len(df)} kayıt yüklendi\n")
        
        # 2. DataFrame'i işle
        print("⚙️  Veriler işleniyor...")
        df = process_dataframe(df)
        
        # 3. Analizleri hesapla
        print("📈 Analizler hesaplanıyor...")
        model_level_avg = compute_model_level_avg(df)
        model_level_group_avg = compute_model_level_group_avg(df)
        criteria_ranking = compute_criteria_ranking(df)
        overall_ranking = compute_overall_ranking(df)
        
        # 4. Çıktı dizini
        if args.output_dir:
            output_base = args.output_dir
        else:
            output_base = os.path.join(evaluator_dir, "analysis_results_combined")
        
        # 5. CSV kaydet
        print(f"\n💾 CSV dosyaları kaydediliyor: {output_base}")
        save_analysis_results(
            model_level_avg,
            model_level_group_avg,
            criteria_ranking,
            overall_ranking,
            output_base
        )
        
        # 6. Grafikler oluştur
        if not args.skip_plots:
            plots_dir = os.path.join(evaluator_dir, "plots_combined")
            print(f"\n📊 Grafikler oluşturuluyor: {plots_dir}")
            create_performance_plots(model_level_avg, plots_dir)
        
        # 7. Özet
        print(f"\n{'=' * 60}")
        print("📋 ÖZET")
        print(f"{'=' * 60}")
        print(f"Analiz edilen model sayısı: {df['model'].nunique()}")
        print(f"Analiz edilen seviye sayısı: {df['level'].nunique()}")
        print(f"Analiz edilen grup sayısı: {df['group'].nunique()}")
        print(f"Toplam kayıt sayısı: {len(df)}")
        print()
        print("🏆 En İyi 5 Model (Overall Skor):")
        print(overall_ranking.head(5).to_string(index=False))
        print()
        print(f"✅ Tamamlandı! Sonuçlar {output_base} dizininde.")
        print(f"{'=' * 60}\n")
        
    else:
        # Yeni davranış: Her seviye için ayrı analiz
        all_results = []
        
        for level in args.levels:
            print(f"\n{'=' * 60}")
            print(f"📂 SEVİYE: {level}")
            print(f"{'=' * 60}")
            
            # 1. Verileri yükle (sadece bu seviye)
            try:
                df = load_ratings_data(evaluator_dir, [level], args.group)
            except ValueError as e:
                print(f"⚠️  {level} için veri yüklenemedi: {e}")
                continue
            
            if len(df) == 0:
                print(f"⚠️  {level} için kayıt bulunamadı, atlanıyor...")
                continue
            
            print(f"✅ {len(df)} kayıt yüklendi")
            
            # 2. DataFrame'i işle
            df = process_dataframe(df)
            
            # 3. Analizleri hesapla
            model_level_avg = compute_model_level_avg(df)
            model_level_group_avg = compute_model_level_group_avg(df)
            criteria_ranking = compute_criteria_ranking(df)
            overall_ranking = compute_overall_ranking(df)
            
            # 4. Çıktı dizini (seviye klasörü içinde)
            if args.output_dir:
                level_output_dir = os.path.join(args.output_dir, level)
            else:
                level_output_dir = os.path.join(evaluator_dir, level, "analysis_results")
            
            # 5. CSV kaydet
            print(f"💾 CSV dosyaları kaydediliyor: {level_output_dir}")
            save_analysis_results(
                model_level_avg,
                model_level_group_avg,
                criteria_ranking,
                overall_ranking,
                level_output_dir
            )
            
            # 6. Grafikler oluştur (seviye klasörü içinde)
            if not args.skip_plots:
                level_plots_dir = os.path.join(evaluator_dir, level, "plots")
                print(f"📊 Grafikler oluşturuluyor: {level_plots_dir}")
                create_performance_plots(model_level_avg, level_plots_dir)
            
            # Özet bilgi topla
            all_results.append({
                'level': level,
                'models': df['model'].nunique(),
                'groups': df['group'].nunique(),
                'records': len(df),
                'top_model': overall_ranking.iloc[0]['model'] if len(overall_ranking) > 0 else 'N/A',
                'top_score': overall_ranking.iloc[0]['overall'] if len(overall_ranking) > 0 else 0
            })
        
        # Genel özet
        if all_results:
            print(f"\n{'=' * 60}")
            print("📋 GENEL ÖZET")
            print(f"{'=' * 60}")
            for result in all_results:
                print(f"\n🎯 {result['level']}:")
                print(f"  - Model Sayısı: {result['models']}")
                print(f"  - Grup Sayısı: {result['groups']}")
                print(f"  - Kayıt Sayısı: {result['records']}")
                print(f"  - En İyi Model: {result['top_model']} ({result['top_score']:.3f})")
            
            print(f"\n✅ Tamamlandı! Her seviyenin sonuçları kendi klasöründe:")
            for result in all_results:
                level_dir = os.path.join(evaluator_dir, result['level'], "analysis_results")
                print(f"  - {result['level']}: {level_dir}")
            print(f"{'=' * 60}\n")
        else:
            print(f"\n❌ Hiçbir seviye için analiz yapılamadı!")
            return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

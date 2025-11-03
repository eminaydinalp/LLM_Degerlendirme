"""
Human Ratings Analysis Script
Bu script, form yanıtlarını tasks_A1_1.json dosyası ile eşleştirerek
modellerin performanslarını analiz eder.
"""

import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Dosya yolları
CSV_FILE = "../data/results/A1/A1 Seviyesi – Yapay Zeka Cümle Üretimi (Yanıtlar) - Form Yanıtları 1.csv"
TASKS_FILE = "../data/tasks/A1/tasks_A1_1.json"
OUTPUT_DIR = "../data/results/A1/analysis_results"

# Çıktı dizinini oluştur
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def parse_rating(rating_str):
    """Puanlama string'ini sayıya çevirir (örn: '3 – Orta' -> 3)"""
    if pd.isna(rating_str):
        return np.nan
    try:
        return int(str(rating_str).split(' ')[0])
    except:
        return np.nan


def load_tasks(tasks_file):
    """Tasks dosyasını yükler ve mapping bilgisini döndürür"""
    with open(tasks_file, 'r', encoding='utf-8') as f:
        tasks = json.load(f)
    return tasks


def extract_ratings_from_csv(csv_file):
    """CSV dosyasından puanları çıkarır"""
    df = pd.read_csv(csv_file)
    
    # Kriterlerin listesi
    criteria = ['Kelime Kullanımı', 'Anlaşılırlık', 'Dilbilgisi Doğruluğu', 'Doğal Kullanım']
    criteria_eng = {
        'Kelime Kullanımı': 'Word Usage',
        'Anlaşılırlık': 'Level Appropriateness', 
        'Dilbilgisi Doğruluğu': 'Grammatical Accuracy',
        'Doğal Kullanım': 'Naturalness'
    }
    
    return df, criteria, criteria_eng


def analyze_model_performance(tasks, df, criteria, criteria_eng):
    """Her model için ortalama performansı hesaplar"""
    
    # Tüm sonuçları saklamak için liste
    all_results = []
    
    # Her task için
    for task in tasks:
        word = task['word']
        mapping = task['mapping']
        
        # Her cümle (A-F) için
        for sentence_label, sentence_info in mapping.items():
            model = sentence_info['model']
            sentence_text = sentence_info['sentence']
            
            # CSV'de bu cümleye ait sütunları bul
            for criterion in criteria:
                # Sütun adı patternleri - birden fazla varyasyon dene
                patterns = [
                    f'{sentence_label}: "{sentence_text}" – Lütfen bu cümleyi puanlayınız. [{criterion}]',
                    f'Sentence {sentence_label[-1]}: "{sentence_text}" – Lütfen bu cümleyi puanlayınız. [{criterion}]',
                ]
                
                matching_col = None
                for pattern in patterns:
                    matching_cols = [col for col in df.columns if pattern in col]
                    if matching_cols:
                        matching_col = matching_cols[0]
                        break
                
                # Eğer tam eşleşme yoksa, cümle metni ve kriter ile eşleştir
                if not matching_col:
                    for col in df.columns:
                        if sentence_text in col and criterion in col:
                            matching_col = col
                            break
                
                if matching_col:
                    # Her katılımcının puanını al
                    for idx, row in df.iterrows():
                        rating = parse_rating(row[matching_col])
                        
                        if not pd.isna(rating):
                            all_results.append({
                                'word': word,
                                'model': model,
                                'sentence_label': sentence_label,
                                'sentence': sentence_text,
                                'criterion': criteria_eng[criterion],
                                'criterion_tr': criterion,
                                'rating': rating,
                                'participant_id': idx
                            })
                else:
                    print(f"⚠️  Sütun bulunamadı: {sentence_label} - {sentence_text[:30]}... - {criterion}")
    
    # DataFrame'e çevir
    results_df = pd.DataFrame(all_results)
    
    return results_df


def calculate_model_statistics(results_df):
    """Model bazında istatistikleri hesaplar"""
    
    # 1. Model bazında genel ortalamalar
    model_overall = results_df.groupby('model')['rating'].agg([
        ('mean', 'mean'),
        ('std', 'std'),
        ('count', 'count')
    ]).round(3)
    
    # 2. Model ve kriter bazında ortalamalar
    model_criterion = results_df.groupby(['model', 'criterion'])['rating'].agg([
        ('mean', 'mean'),
        ('std', 'std'),
        ('count', 'count')
    ]).round(3)
    
    # 3. Kelime bazında model performansı
    model_word = results_df.groupby(['word', 'model'])['rating'].mean().round(3)
    
    # 4. Kriter bazında genel ortalamalar
    criterion_overall = results_df.groupby('criterion')['rating'].agg([
        ('mean', 'mean'),
        ('std', 'std')
    ]).round(3)
    
    return model_overall, model_criterion, model_word, criterion_overall


def create_visualizations(results_df, model_overall, model_criterion, output_dir):
    """Görselleştirmeler oluşturur"""
    
    # Renk paleti
    sns.set_palette("husl")
    
    # 1. Model bazında genel performans (Bar plot)
    plt.figure(figsize=(12, 6))
    model_means = model_overall.sort_values('mean', ascending=False)
    plt.bar(range(len(model_means)), model_means['mean'], 
            yerr=model_means['std'], capsize=5)
    plt.xticks(range(len(model_means)), model_means.index, rotation=45, ha='right')
    plt.ylabel('Average Rating')
    plt.title('Model Performance - Overall Average Ratings')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_dir}/model_overall_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Model ve kriter bazında performans (Heatmap)
    plt.figure(figsize=(14, 8))
    pivot_data = results_df.groupby(['model', 'criterion'])['rating'].mean().unstack()
    sns.heatmap(pivot_data, annot=True, fmt='.2f', cmap='YlGnBu', 
                cbar_kws={'label': 'Average Rating'})
    plt.title('Model Performance by Criterion')
    plt.xlabel('Criterion')
    plt.ylabel('Model')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/model_criterion_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Kriter bazında box plot
    plt.figure(figsize=(14, 6))
    results_df.boxplot(column='rating', by='model', figsize=(14, 6))
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Rating')
    plt.title('Rating Distribution by Model')
    plt.suptitle('')  # Varsayılan başlığı kaldır
    plt.tight_layout()
    plt.savefig(f'{output_dir}/model_rating_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Her kriter için model karşılaştırması
    criteria = results_df['criterion'].unique()
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    axes = axes.flatten()
    
    for idx, criterion in enumerate(criteria):
        criterion_data = results_df[results_df['criterion'] == criterion]
        criterion_means = criterion_data.groupby('model')['rating'].mean().sort_values(ascending=False)
        criterion_stds = criterion_data.groupby('model')['rating'].std()
        
        axes[idx].bar(range(len(criterion_means)), criterion_means.values,
                     yerr=criterion_stds.values, capsize=5)
        axes[idx].set_xticks(range(len(criterion_means)))
        axes[idx].set_xticklabels(criterion_means.index, rotation=45, ha='right')
        axes[idx].set_ylabel('Average Rating')
        axes[idx].set_title(f'{criterion}')
        axes[idx].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/model_performance_by_criterion.png', dpi=300, bbox_inches='tight')
    plt.close()


def create_ranking_table(model_overall, model_criterion):
    """Model sıralaması tablosu oluşturur"""
    
    # Genel sıralama
    overall_ranking = model_overall.sort_values('mean', ascending=False).reset_index()
    overall_ranking['rank'] = range(1, len(overall_ranking) + 1)
    
    # Kriter bazında sıralama
    criterion_rankings = []
    for criterion in model_criterion.index.get_level_values(1).unique():
        criterion_data = model_criterion.xs(criterion, level=1).sort_values('mean', ascending=False)
        criterion_data = criterion_data.reset_index()
        criterion_data['rank'] = range(1, len(criterion_data) + 1)
        criterion_data['criterion'] = criterion
        criterion_rankings.append(criterion_data)
    
    criterion_ranking_df = pd.concat(criterion_rankings, ignore_index=True)
    
    return overall_ranking, criterion_ranking_df


def save_results(results_df, model_overall, model_criterion, model_word, 
                criterion_overall, overall_ranking, criterion_ranking_df, output_dir):
    """Sonuçları dosyalara kaydeder"""
    
    # 1. Ham veri
    results_df.to_csv(f'{output_dir}/all_ratings.csv', index=False, encoding='utf-8-sig')
    
    # 2. Model genel istatistikleri
    model_overall.to_csv(f'{output_dir}/model_overall_stats.csv', encoding='utf-8-sig')
    
    # 3. Model-kriter istatistikleri
    model_criterion.to_csv(f'{output_dir}/model_criterion_stats.csv', encoding='utf-8-sig')
    
    # 4. Kelime bazında performans
    model_word.to_csv(f'{output_dir}/model_word_performance.csv', encoding='utf-8-sig')
    
    # 5. Kriter genel istatistikleri
    criterion_overall.to_csv(f'{output_dir}/criterion_overall_stats.csv', encoding='utf-8-sig')
    
    # 6. Sıralamalar
    overall_ranking.to_csv(f'{output_dir}/overall_ranking.csv', index=False, encoding='utf-8-sig')
    criterion_ranking_df.to_csv(f'{output_dir}/criterion_ranking.csv', index=False, encoding='utf-8-sig')


def print_summary(model_overall, overall_ranking):
    """Özet istatistikleri ekrana yazdırır"""
    
    print("\n" + "="*80)
    print("MODEL PERFORMANS ANALİZİ - ÖZET")
    print("="*80)
    
    print("\n📊 GENEL SIRALAMALAR:")
    print("-" * 80)
    for idx, row in overall_ranking.iterrows():
        print(f"{row['rank']}. {row['model']:45s} - Ortalama: {row['mean']:.3f} (±{row['std']:.3f})")
    
    print("\n" + "="*80)
    print(f"Toplam Değerlendirme Sayısı: {model_overall['count'].sum():.0f}")
    print(f"Ortalama Puan (Tüm Modeller): {model_overall['mean'].mean():.3f}")
    print("="*80)


def main():
    """Ana fonksiyon"""
    
    print("🔄 Veriler yükleniyor...")
    
    # Tasks dosyasını yükle
    tasks = load_tasks(TASKS_FILE)
    print(f"✅ {len(tasks)} task yüklendi")
    
    # CSV dosyasını yükle
    df, criteria, criteria_eng = extract_ratings_from_csv(CSV_FILE)
    print(f"✅ {len(df)} katılımcı verisi yüklendi")
    
    # Analizleri yap
    print("\n🔄 Analizler yapılıyor...")
    results_df = analyze_model_performance(tasks, df, criteria, criteria_eng)
    print(f"✅ {len(results_df)} değerlendirme işlendi")
    
    # İstatistikleri hesapla
    print("\n🔄 İstatistikler hesaplanıyor...")
    model_overall, model_criterion, model_word, criterion_overall = calculate_model_statistics(results_df)
    
    # Sıralamaları oluştur
    overall_ranking, criterion_ranking_df = create_ranking_table(model_overall, model_criterion)
    
    # Görselleştirmeler
    print("\n🔄 Görselleştirmeler oluşturuluyor...")
    create_visualizations(results_df, model_overall, model_criterion, OUTPUT_DIR)
    print("✅ Grafikler kaydedildi")
    
    # Sonuçları kaydet
    print("\n🔄 Sonuçlar kaydediliyor...")
    save_results(results_df, model_overall, model_criterion, model_word,
                criterion_overall, overall_ranking, criterion_ranking_df, OUTPUT_DIR)
    print("✅ Tüm sonuçlar kaydedildi")
    
    # Özet yazdır
    print_summary(model_overall, overall_ranking)
    
    print(f"\n📁 Tüm sonuçlar şu klasöre kaydedildi: {OUTPUT_DIR}")
    print("\n✨ Analiz tamamlandı!")


if __name__ == "__main__":
    main()

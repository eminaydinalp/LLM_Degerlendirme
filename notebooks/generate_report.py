"""
Detaylı Performans Raporu Oluşturucu
Bu script, analiz sonuçlarından detaylı bir rapor oluşturur.
"""

import pandas as pd
import json
from pathlib import Path

# Dosya yolları
RESULTS_DIR = "../data/results/A1/analysis_results"
OUTPUT_FILE = f"{RESULTS_DIR}/detailed_report.md"


def create_detailed_report():
    """Detaylı rapor oluşturur"""
    
    # Sonuç dosyalarını yükle
    model_overall = pd.read_csv(f"{RESULTS_DIR}/model_overall_stats.csv", index_col=0)
    model_criterion = pd.read_csv(f"{RESULTS_DIR}/model_criterion_stats.csv")
    overall_ranking = pd.read_csv(f"{RESULTS_DIR}/overall_ranking.csv")
    criterion_ranking = pd.read_csv(f"{RESULTS_DIR}/criterion_ranking.csv")
    all_ratings = pd.read_csv(f"{RESULTS_DIR}/all_ratings.csv")
    
    # Raporu oluştur
    report = []
    report.append("# A1 Seviyesi - Model Performans Analizi Raporu\n")
    report.append(f"**Analiz Tarihi:** {pd.Timestamp.now().strftime('%d.%m.%Y %H:%M')}\n")
    report.append(f"**Toplam Katılımcı Sayısı:** {all_ratings['participant_id'].nunique()}\n")
    report.append(f"**Toplam Değerlendirme Sayısı:** {len(all_ratings)}\n")
    report.append(f"**Değerlendirilen Kelime Sayısı:** {all_ratings['word'].nunique()}\n\n")
    
    report.append("---\n\n")
    
    # 1. GENEL SIRALAMALAR
    report.append("## 1. Genel Model Sıralaması\n\n")
    report.append("| Sıra | Model | Ortalama Puan | Std. Sapma | Değerlendirme Sayısı |\n")
    report.append("|------|-------|---------------|------------|---------------------|\n")
    
    for idx, row in overall_ranking.iterrows():
        report.append(f"| {row['rank']} | {row['model']} | {row['mean']:.3f} | ±{row['std']:.3f} | {int(row['count'])} |\n")
    
    report.append("\n")
    
    # 2. KRİTER BAZINDA PERFORMANS
    report.append("## 2. Kriter Bazında Model Performansı\n\n")
    
    criteria = ['Word Usage', 'Level Appropriateness', 'Grammatical Accuracy', 'Naturalness']
    criteria_tr = {
        'Word Usage': 'Kelime Kullanımı',
        'Level Appropriateness': 'Seviye Uygunluğu',
        'Grammatical Accuracy': 'Dilbilgisi Doğruluğu',
        'Naturalness': 'Doğallık'
    }
    
    for criterion in criteria:
        report.append(f"### 2.{criteria.index(criterion)+1}. {criteria_tr[criterion]} ({criterion})\n\n")
        
        criterion_data = criterion_ranking[criterion_ranking['criterion'] == criterion].sort_values('rank')
        
        report.append("| Sıra | Model | Ortalama Puan | Std. Sapma |\n")
        report.append("|------|-------|---------------|------------|\n")
        
        for idx, row in criterion_data.iterrows():
            report.append(f"| {row['rank']} | {row['model']} | {row['mean']:.3f} | ±{row['std']:.3f} |\n")
        
        report.append("\n")
    
    # 3. KELİME BAZINDA PERFORMANS
    report.append("## 3. Kelime Bazında Model Performansı\n\n")
    
    model_word = pd.read_csv(f"{RESULTS_DIR}/model_word_performance.csv")
    words = all_ratings['word'].unique()
    
    for word in sorted(words):
        report.append(f"### {word}\n\n")
        word_data = all_ratings[all_ratings['word'] == word].groupby('model')['rating'].agg(['mean', 'std', 'count']).sort_values('mean', ascending=False)
        
        report.append("| Model | Ortalama Puan | Std. Sapma | Değerlendirme Sayısı |\n")
        report.append("|-------|---------------|------------|---------------------|\n")
        
        for model, row in word_data.iterrows():
            report.append(f"| {model} | {row['mean']:.3f} | ±{row['std']:.3f} | {int(row['count'])} |\n")
        
        report.append("\n")
    
    # 4. İSTATİSTİKSEL ÖZET
    report.append("## 4. İstatistiksel Özet\n\n")
    
    report.append(f"- **En Yüksek Ortalama Puan:** {model_overall['mean'].max():.3f} ({model_overall['mean'].idxmax()})\n")
    report.append(f"- **En Düşük Ortalama Puan:** {model_overall['mean'].min():.3f} ({model_overall['mean'].idxmin()})\n")
    report.append(f"- **Ortalama Puan Aralığı:** {model_overall['mean'].max() - model_overall['mean'].min():.3f}\n")
    report.append(f"- **Genel Ortalama:** {model_overall['mean'].mean():.3f}\n")
    report.append(f"- **Genel Standart Sapma:** {model_overall['mean'].std():.3f}\n\n")
    
    # 5. MODEL KARŞILAŞTIRMALARI
    report.append("## 5. Önemli Gözlemler\n\n")
    
    # En iyi ve en kötü performans gösteren modeller
    best_model = overall_ranking.iloc[0]
    worst_model = overall_ranking.iloc[-1]
    
    report.append(f"### 5.1. En İyi Performans\n")
    report.append(f"**{best_model['model']}** modeli {best_model['mean']:.3f} ortalama puan ile en iyi performansı göstermiştir.\n\n")
    
    report.append(f"### 5.2. En Düşük Performans\n")
    report.append(f"**{worst_model['model']}** modeli {worst_model['mean']:.3f} ortalama puan ile en düşük performansı göstermiştir.\n\n")
    
    # Her kriter için en iyi model
    report.append(f"### 5.3. Kriter Bazında En İyi Modeller\n\n")
    for criterion in criteria:
        best_in_criterion = criterion_ranking[criterion_ranking['criterion'] == criterion].iloc[0]
        report.append(f"- **{criteria_tr[criterion]}:** {best_in_criterion['model']} ({best_in_criterion['mean']:.3f})\n")
    
    report.append("\n")
    
    # 6. SONUÇ VE ÖNERİLER
    report.append("## 6. Sonuç\n\n")
    report.append(f"Bu analizde {all_ratings['participant_id'].nunique()} katılımcıdan toplanan ")
    report.append(f"{len(all_ratings)} değerlendirme üzerinden 6 farklı modelin A1 seviyesi cümle üretme ")
    report.append(f"performansı incelenmiştir.\n\n")
    
    report.append("**Temel Bulgular:**\n")
    report.append(f"1. Claude Sonnet 4.5 modeli genel olarak en yüksek performansı göstermiştir (Ortalama: {best_model['mean']:.3f})\n")
    report.append(f"2. Tüm modellerin ortalama puanı {model_overall['mean'].mean():.3f} olarak hesaplanmıştır\n")
    report.append(f"3. Modeller arası performans farkı {model_overall['mean'].max() - model_overall['mean'].min():.3f} puan olarak ölçülmüştür\n")
    
    report.append("\n---\n\n")
    report.append("*Bu rapor otomatik olarak oluşturulmuştur.*\n")
    
    # Dosyaya yaz
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.writelines(report)
    
    print(f"✅ Detaylı rapor oluşturuldu: {OUTPUT_FILE}")


def create_excel_summary():
    """Excel formatında özet rapor oluşturur"""
    
    # Tüm sonuçları yükle
    model_overall = pd.read_csv(f"{RESULTS_DIR}/model_overall_stats.csv", index_col=0)
    model_criterion = pd.read_csv(f"{RESULTS_DIR}/model_criterion_stats.csv")
    overall_ranking = pd.read_csv(f"{RESULTS_DIR}/overall_ranking.csv")
    criterion_ranking = pd.read_csv(f"{RESULTS_DIR}/criterion_ranking.csv")
    
    # Excel dosyası oluştur
    excel_file = f"{RESULTS_DIR}/performance_summary.xlsx"
    
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        overall_ranking.to_excel(writer, sheet_name='Genel Sıralama', index=False)
        
        # Kriter bazında sıralamalar için ayrı sayfalar
        for criterion in criterion_ranking['criterion'].unique():
            criterion_data = criterion_ranking[criterion_ranking['criterion'] == criterion]
            sheet_name = criterion[:30]  # Excel sayfa adı limiti
            criterion_data.to_excel(writer, sheet_name=sheet_name, index=False)
        
        # Model-Kriter detayları
        pivot_table = model_criterion.pivot_table(
            values='mean',
            index='model',
            columns='criterion',
            aggfunc='first'
        )
        pivot_table.to_excel(writer, sheet_name='Model-Kriter Matrisi')
    
    print(f"✅ Excel özet raporu oluşturuldu: {excel_file}")


if __name__ == "__main__":
    print("📊 Detaylı rapor oluşturuluyor...\n")
    create_detailed_report()
    create_excel_summary()
    print("\n✨ Raporlama tamamlandı!")

#!/usr/bin/env python3
"""
ChatGPT Rating Analysis Report Generator
-----------------------------------------
A1 formatında detaylı analiz raporu ve grafikler oluşturur.

Kullanım:
    python create_chatgpt_analysis_report.py --level A2 --group 1
    python create_chatgpt_analysis_report.py --level A1 --group 1 --evaluator chatgpt_ratings
"""

import os
import json
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from pathlib import Path


# Renk paleti (A1 ile aynı)
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#06A77D',
    'warning': '#F18F01',
    'danger': '#C73E1D',
    'info': '#6C757D'
}

# Model renkleri
MODEL_COLORS = {
    'Claude_Sonnet_4.5': '#2E86AB',
    'Gemini_Pro_2.5': '#A23B72',
    'Llama-3.2-1B-Instruct-FineTuned': '#06A77D',
    'mistralai_Ministral-8B-Instruct-2410': '#F18F01',
    'Llama-3.1-8B-Instruct': '#C73E1D',
    'Llama-3.2-1B-Instruct': '#6C757D',
    'Llama-3.2-8B-Instruct': '#8B5A3C',
    'Model1': '#4A4A4A',
}


def load_ratings(filepath):
    """Rating dosyasını yükler"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_dataframe(ratings_data):
    """JSON verisini DataFrame'e çevirir"""
    df = pd.DataFrame(ratings_data)
    
    # Ratings dict'ini ayrı kolonlara aç
    if 'ratings' in df.columns:
        ratings_df = df['ratings'].apply(pd.Series)
        df = pd.concat([df.drop(columns=['ratings']), ratings_df], axis=1)
    
    # Overall skor hesapla
    criteria = ['word_usage', 'clarity', 'grammar', 'naturalness']
    df['overall'] = df[criteria].mean(axis=1)
    
    return df


def generate_report_text(df, level, group, evaluator, output_file):
    """Detaylı text raporu oluşturur"""
    
    report = []
    report.append("=" * 80)
    report.append(f"CHATGPT RATING ANALYSIS REPORT - {level} LEVEL")
    report.append("=" * 80)
    report.append(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Source File: ratings_{level}_{group}.json")
    report.append(f"Evaluator: {df['evaluator'].iloc[0]} (ChatGPT)")
    report.append("")
    
    # SUMMARY
    report.append("-" * 80)
    report.append("SUMMARY")
    report.append("-" * 80)
    n_eval = len(df)
    n_words = df['word'].nunique()
    n_models = df['model'].nunique()
    words = sorted(df['word'].unique())
    
    report.append(f"Total Evaluations: {n_eval}")
    report.append(f"Total Words: {n_words}")
    report.append(f"Total Models: {n_models}")
    report.append(f"Words: {', '.join(words)}")
    report.append("")
    
    # OVERALL SCORES
    report.append("-" * 80)
    report.append("OVERALL SCORES")
    report.append("-" * 80)
    
    criteria_labels = {
        'word_usage': 'Word Usage (Kelime Kullanımı)',
        'clarity': 'Clarity (Netlik)',
        'grammar': 'Grammar (Dilbilgisi)',
        'naturalness': 'Naturalness (Doğallık)'
    }
    
    for crit, label in criteria_labels.items():
        avg = df[crit].mean()
        report.append(f"{label:30} : {avg:.2f} / 5.00")
    
    overall_avg = df['overall'].mean()
    report.append(f"{'Overall Average':30} : {overall_avg:.2f} / 5.00")
    report.append("")
    
    # MODEL PERFORMANCE RANKING
    report.append("-" * 80)
    report.append("MODEL PERFORMANCE RANKING")
    report.append("-" * 80)
    
    model_agg = df.groupby('model').agg({
        'word_usage': 'mean',
        'clarity': 'mean',
        'grammar': 'mean',
        'naturalness': 'mean',
        'overall': ['mean', 'std']
    }).round(2)
    
    # Flatten MultiIndex columns
    model_stats = pd.DataFrame({
        'model': model_agg.index,
        'WU': model_agg[('word_usage', 'mean')].values,
        'CL': model_agg[('clarity', 'mean')].values,
        'GR': model_agg[('grammar', 'mean')].values,
        'NT': model_agg[('naturalness', 'mean')].values,
        'AVG': model_agg[('overall', 'mean')].values,
        'STD': model_agg[('overall', 'std')].values
    })
    model_stats = model_stats.sort_values('AVG', ascending=False).reset_index(drop=True)
    model_stats['Rank'] = range(1, len(model_stats) + 1)
    
    report.append(f"{'Rank':<6} {'Model':<45} {'WU':<6} {'CL':<6} {'GR':<6} {'NT':<6} {'AVG':<6} {'STD':<5}")
    report.append("-" * 80)
    
    for _, row in model_stats.iterrows():
        report.append(
            f"{int(row['Rank']):<6} {row['model']:<45} "
            f"{row['WU']:.2f}   {row['CL']:.2f}   {row['GR']:.2f}   "
            f"{row['NT']:.2f}   {row['AVG']:.2f}   {row['STD']:.3f}"
        )
    
    report.append("")
    report.append("Legend: WU=Word Usage, CL=Clarity, GR=Grammar, NT=Naturalness, STD=Standard Deviation")
    report.append("")
    
    # WORD DIFFICULTY ANALYSIS
    report.append("-" * 80)
    report.append("WORD DIFFICULTY ANALYSIS")
    report.append("-" * 80)
    
    word_stats = df.groupby('word').agg({
        'word_usage': 'mean',
        'clarity': 'mean',
        'grammar': 'mean',
        'naturalness': 'mean',
        'overall': 'mean'
    }).round(2)
    
    word_stats = word_stats.sort_values('overall', ascending=False).reset_index()
    
    report.append(f"{'Word':<15} {'WU':<6} {'CL':<6} {'GR':<6} {'NT':<6} {'AVG':<6}")
    report.append("-" * 80)
    
    for _, row in word_stats.iterrows():
        report.append(
            f"{row['word']:<15} {row['word_usage']:.2f}   {row['clarity']:.2f}   "
            f"{row['grammar']:.2f}   {row['naturalness']:.2f}   {row['overall']:.2f}"
        )
    
    report.append("")
    
    # CRITICAL ISSUES
    report.append("-" * 80)
    report.append("CRITICAL ISSUES")
    report.append("-" * 80)
    
    critical = df[df['word_usage'] <= 1.5]
    
    if len(critical) > 0:
        report.append(f"WARNING: {len(critical)} sentences have critical word usage errors (score <= 1.5)")
        report.append("")
        
        for _, row in critical.iterrows():
            report.append(f"  Word: {row['word']}")
            report.append(f"  Model: {row['model']}")
            report.append(f"  Sentence: \"{row['sentence']}\"")
            if row['word_usage'] == 1.0:
                report.append("  Issue: Word not used or completely misused")
            else:
                report.append("  Issue: Serious word usage problem")
            report.append("")
    else:
        report.append("✓ No critical word usage errors found")
        report.append("")
    
    # SCORE DISTRIBUTION
    report.append("-" * 80)
    report.append("SCORE DISTRIBUTION")
    report.append("-" * 80)
    
    perfect = len(df[df['overall'] == 5.0])
    good = len(df[(df['overall'] >= 4.0) & (df['overall'] < 5.0)])
    poor = len(df[df['overall'] < 4.0])
    
    total = len(df)
    report.append(f"Perfect (5.0)       : {perfect:3} sentences ({perfect/total*100:5.1f}%)")
    report.append(f"Good (4.0-4.9)      : {good:3} sentences ({good/total*100:5.1f}%)")
    report.append(f"Poor (<4.0)         : {poor:3} sentences ({poor/total*100:5.1f}%)")
    report.append("")
    
    # PROBLEMATIC SENTENCES
    if poor > 0:
        report.append("-" * 80)
        report.append("PROBLEMATIC SENTENCES (Score < 4.0)")
        report.append("-" * 80)
        
        problematic = df[df['overall'] < 4.0].sort_values('overall')
        
        for _, row in problematic.iterrows():
            report.append(f"Word: {row['word']} | Model: {row['model']}")
            report.append(f"Sentence: \"{row['sentence']}\"")
            report.append(
                f"Scores - WU: {row['word_usage']:.1f}, CL: {row['clarity']:.1f}, "
                f"GR: {row['grammar']:.1f}, NT: {row['naturalness']:.1f} | "
                f"AVG: {row['overall']:.2f}"
            )
            report.append("")
    
    # KEY FINDINGS
    report.append("-" * 80)
    report.append("KEY FINDINGS")
    report.append("-" * 80)
    
    best_model = model_stats.iloc[0]
    most_consistent = model_stats.loc[model_stats['STD'].idxmin()]
    
    criteria_avg = {
        'Word Usage': df['word_usage'].mean(),
        'Clarity': df['clarity'].mean(),
        'Grammar': df['grammar'].mean(),
        'Naturalness': df['naturalness'].mean()
    }
    weakest_crit = min(criteria_avg, key=criteria_avg.get)
    strongest_crit = max(criteria_avg, key=criteria_avg.get)
    
    report.append(f"• Best Performing Model: {best_model['model']} ({best_model['AVG']:.2f}/5.0)")
    report.append(f"• Most Consistent Model: {most_consistent['model']} (std: {most_consistent['STD']:.3f})")
    report.append(f"• Weakest Criterion: {weakest_crit} ({criteria_avg[weakest_crit]:.2f})")
    report.append(f"• Strongest Criterion: {strongest_crit} ({criteria_avg[strongest_crit]:.2f})")
    report.append(f"• Perfect Score Rate: {perfect/total*100:.1f}%")
    report.append(f"• Problematic Sentences: {poor} out of {total}")
    report.append("")
    
    # RECOMMENDATIONS
    report.append("-" * 80)
    report.append("RECOMMENDATIONS")
    report.append("-" * 80)
    
    # Top performers
    top_3 = model_stats.head(3)
    for _, model in top_3.iterrows():
        if model['AVG'] >= 4.5:
            report.append(f"✓ {model['model']} shows excellent performance")
        elif model['AVG'] >= 4.0:
            report.append(f"✓ {model['model']} shows good performance")
    
    # Bottom performers
    bottom = model_stats.iloc[-1]
    if bottom['AVG'] < 4.0:
        report.append(f"✗ {bottom['model']} is NOT suitable for {level} level without improvement")
    
    # Focus areas
    if criteria_avg['Word Usage'] < 4.5:
        report.append("• Focus areas: Word usage accuracy and natural expression")
    
    # Challenging words (lowest scoring)
    low_scoring_words = word_stats.nsmallest(3, 'overall')['word'].tolist()
    if low_scoring_words:
        report.append(f"• Words requiring attention: {', '.join(low_scoring_words)} (lower scoring words)")
    
    report.append("")
    
    # VISUALIZATIONS
    report.append("-" * 80)
    report.append("VISUALIZATIONS")
    report.append("-" * 80)
    report.append("The following charts have been generated:")
    report.append("  1. chart_1_model_overall.png         - Model Overall Performance")
    report.append("  2. chart_2_model_by_criteria.png     - Model Performance by Criteria")
    report.append("  3. chart_3_word_difficulty.png       - Word Difficulty Analysis")
    report.append("  4. chart_4_criteria_distribution.png - Overall Performance by Criteria")
    report.append("  5. chart_5_model_consistency.png     - Model Consistency Analysis")
    report.append("  6. chart_6_score_distribution.png    - Score Distribution")
    report.append("")
    
    report.append("=" * 80)
    report.append("END OF REPORT")
    report.append("=" * 80)
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))
    
    print(f"✓ Report saved: {output_file}")
    
    return model_stats, word_stats


def create_charts(df, level, group, model_stats, word_stats, output_dir):
    """A1 formatında grafikler oluşturur"""
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 10
    
    # 1. Model Overall Performance
    fig, ax = plt.subplots(figsize=(12, 6))
    
    models = model_stats['model'].tolist()
    avgs = model_stats['AVG'].tolist()
    colors_list = [MODEL_COLORS.get(m, COLORS['info']) for m in models]
    
    bars = ax.barh(range(len(models)), avgs, color=colors_list, edgecolor='black', linewidth=0.5)
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(models, fontsize=10)
    ax.set_xlabel('Average Overall Score', fontsize=12, fontweight='bold')
    ax.set_title(f'{level} Level - Model Overall Performance', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 5)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, avgs)):
        ax.text(val + 0.05, i, f'{val:.2f}', va='center', fontsize=9, fontweight='bold')
    
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chart_1_model_overall.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ chart_1_model_overall.png")
    
    # 2. Model Performance by Criteria
    fig, ax = plt.subplots(figsize=(14, 7))
    
    criteria_cols = ['WU', 'CL', 'GR', 'NT']
    criteria_labels = ['Word Usage', 'Clarity', 'Grammar', 'Naturalness']
    
    x = np.arange(len(models))
    width = 0.2
    
    for i, (crit, label) in enumerate(zip(criteria_cols, criteria_labels)):
        values = model_stats[crit].tolist()
        ax.bar(x + i * width, values, width, label=label, edgecolor='black', linewidth=0.5)
    
    ax.set_xlabel('Models', fontsize=12, fontweight='bold')
    ax.set_ylabel('Average Score', fontsize=12, fontweight='bold')
    ax.set_title(f'{level} Level - Model Performance by Criteria', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models, rotation=45, ha='right', fontsize=9)
    ax.set_ylim(0, 5.5)
    ax.legend(loc='lower right', fontsize=10, bbox_to_anchor=(1.0, -0.3))
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chart_2_model_by_criteria.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ chart_2_model_by_criteria.png")
    
    # 3. Word Difficulty Analysis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    words = word_stats['word'].tolist()
    word_avgs = word_stats['overall'].tolist()
    
    # Renk geçişi oluştur (yeşilden kırmızıya: yüksek skordan düşük skora)
    import matplotlib.colors as mcolors
    cmap = plt.cm.RdYlGn  # Red-Yellow-Green colormap
    norm = mcolors.Normalize(vmin=min(word_avgs), vmax=max(word_avgs))
    colors_list = [cmap(norm(val)) for val in word_avgs]
    
    bars = ax.barh(range(len(words)), word_avgs, color=colors_list, edgecolor='black', linewidth=0.5)
    ax.set_yticks(range(len(words)))
    ax.set_yticklabels(words, fontsize=10)
    ax.set_xlabel('Average Score', fontsize=12, fontweight='bold')
    ax.set_title(f'{level} Level - Word Difficulty Analysis', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xlim(0, 5)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, word_avgs)):
        ax.text(val + 0.05, i, f'{val:.2f}', va='center', fontsize=9, fontweight='bold')
    
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chart_3_word_difficulty.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ chart_3_word_difficulty.png")
    
    # 4. Criteria Distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    
    criteria = ['word_usage', 'clarity', 'grammar', 'naturalness']
    criteria_means = [df[c].mean() for c in criteria]
    
    bars = ax.bar(criteria_labels, criteria_means, color=[COLORS['primary'], COLORS['secondary'], 
                                                            COLORS['success'], COLORS['warning']], 
                   edgecolor='black', linewidth=1)
    
    ax.set_ylabel('Average Score', fontsize=12, fontweight='bold')
    ax.set_title(f'{level} Level - Overall Performance by Criteria', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 5.5)
    
    # Add value labels
    for bar, val in zip(bars, criteria_means):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                f'{val:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chart_4_criteria_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ chart_4_criteria_distribution.png")
    
    # 5. Model Consistency Analysis
    fig, ax = plt.subplots(figsize=(12, 6))
    
    models = model_stats['model'].tolist()
    stds = model_stats['STD'].tolist()
    colors_list = [MODEL_COLORS.get(m, COLORS['info']) for m in models]
    
    bars = ax.barh(range(len(models)), stds, color=colors_list, edgecolor='black', linewidth=0.5)
    ax.set_yticks(range(len(models)))
    ax.set_yticklabels(models, fontsize=10)
    ax.set_xlabel('Standard Deviation', fontsize=12, fontweight='bold')
    ax.set_title(f'{level} Level - Model Consistency Analysis\n(Lower is Better)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, stds)):
        ax.text(val + 0.01, i, f'{val:.3f}', va='center', fontsize=9, fontweight='bold')
    
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chart_5_model_consistency.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ chart_5_model_consistency.png")
    
    # 6. Score Distribution
    fig, ax = plt.subplots(figsize=(10, 6))
    
    perfect = len(df[df['overall'] == 5.0])
    good = len(df[(df['overall'] >= 4.0) & (df['overall'] < 5.0)])
    poor = len(df[df['overall'] < 4.0])
    
    categories = ['Perfect\n(5.0)', 'Good\n(4.0-4.9)', 'Poor\n(<4.0)']
    counts = [perfect, good, poor]
    colors_list = [COLORS['success'], COLORS['warning'], COLORS['danger']]
    
    bars = ax.bar(categories, counts, color=colors_list, edgecolor='black', linewidth=1)
    
    ax.set_ylabel('Number of Sentences', fontsize=12, fontweight='bold')
    ax.set_title(f'{level} Level - Score Distribution', 
                 fontsize=14, fontweight='bold', pad=20)
    
    total = len(df)
    for bar, count in zip(bars, counts):
        height = bar.get_height()
        percentage = count / total * 100
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{count}\n({percentage:.1f}%)', 
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'chart_6_score_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()
    print("  ✓ chart_6_score_distribution.png")


def main():
    parser = argparse.ArgumentParser(
        description="A1 formatında ChatGPT rating analiz raporu oluşturur",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--level', type=str, required=True, 
                       choices=['A1', 'A2', 'B1', 'B2', 'C1'],
                       help='Seviye (A1, A2, B1, B2, C1)')
    
    parser.add_argument('--group', type=int, required=True,
                       help='Grup numarası')
    
    parser.add_argument('--evaluator', type=str, default='chatgpt_ratings',
                       help='Değerlendirici dizini (varsayılan: chatgpt_ratings)')
    
    args = parser.parse_args()
    
    # Paths
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ratings_dir = os.path.join(workspace_root, 'data', 'ratings', args.evaluator, args.level)
    ratings_file = os.path.join(ratings_dir, f'ratings_{args.level}_{args.group}.json')
    
    if not os.path.exists(ratings_file):
        print(f"❌ Rating dosyası bulunamadı: {ratings_file}")
        return 1
    
    print(f"\n📊 Analysis Report Generator")
    print("=" * 60)
    print(f"Level: {args.level}")
    print(f"Group: {args.group}")
    print(f"Evaluator: {args.evaluator}")
    print(f"Input: {ratings_file}")
    print("=" * 60)
    print()
    
    # Load data
    print("📂 Loading data...")
    ratings_data = load_ratings(ratings_file)
    df = create_dataframe(ratings_data)
    print(f"✓ Loaded {len(df)} evaluations")
    print()
    
    # Generate report
    print("📝 Generating text report...")
    report_file = os.path.join(ratings_dir, f'analysis_report_{args.level}_{args.group}.txt')
    model_stats, word_stats = generate_report_text(df, args.level, args.group, args.evaluator, report_file)
    print()
    
    # Create charts
    print("📊 Creating visualizations...")
    create_charts(df, args.level, args.group, model_stats, word_stats, ratings_dir)
    print()
    
    print("=" * 60)
    print("✅ Analysis complete!")
    print(f"📁 Output directory: {ratings_dir}")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    exit(main())

"""
C1 Level Training Plots Generator
Eğitim sonuçlarını görselleştiren plotlar oluşturur
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Paths
CHECKPOINT_PATH = "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/loras/llama1b-c1-unsloth-v2/checkpoint-290/trainer_state.json"
OUTPUT_DIR = Path("/home/muhammet/Documents/Tez/LLM_Degerlendirme/notebooks/fine_tuning/training_plots/C1")

# Load training data
print("📂 Loading training data...")
with open(CHECKPOINT_PATH, 'r') as f:
    data = json.load(f)

logs = data['log_history']
print(f"✓ Loaded {len(logs)} log entries")

# Extract data
train_steps = []
train_losses = []
eval_steps = []
eval_losses = []
learning_rates = []

for log in logs:
    if 'loss' in log and 'eval_loss' not in log:
        train_steps.append(log['step'])
        train_losses.append(log['loss'])
        if 'learning_rate' in log:
            learning_rates.append(log['learning_rate'])
    if 'eval_loss' in log:
        eval_steps.append(log['step'])
        eval_losses.append(log['eval_loss'])

print(f"✓ Train points: {len(train_steps)}")
print(f"✓ Eval points: {len(eval_steps)}")

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = {
    'train': '#2E86AB',
    'eval': '#A23B72',
    'baseline': '#F18F01',
    'grid': '#E8E8E8'
}

# ========================================================================
# Plot 1: Train vs Eval Loss
# ========================================================================
print("\n📊 Creating Plot 1: Train vs Eval Loss...")
fig, ax = plt.subplots(figsize=(12, 7))

# Plot losses
ax.plot(train_steps, train_losses, 'o-', 
        color=colors['train'], linewidth=2.5, markersize=6,
        label='Train Loss', alpha=0.8)
ax.plot(eval_steps, eval_losses, 's-', 
        color=colors['eval'], linewidth=2.5, markersize=7,
        label='Eval Loss', alpha=0.8)

# Add baseline reference
baseline_loss = 2.4024
ax.axhline(y=baseline_loss, color=colors['baseline'], 
           linestyle='--', linewidth=2, 
           label=f'Baseline Loss ({baseline_loss:.2f})', alpha=0.7)

# Styling
ax.set_xlabel('Training Step', fontsize=14, fontweight='bold')
ax.set_ylabel('Loss', fontsize=14, fontweight='bold')
ax.set_title('C1 Level Fine-Tuning: Train vs Eval Loss', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(fontsize=12, loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.3, color=colors['grid'])
ax.set_xlim(0, max(train_steps) + 10)

# Add annotations for key points
best_eval_idx = eval_losses.index(min(eval_losses))
ax.annotate(f'Best Eval\n{min(eval_losses):.4f}', 
            xy=(eval_steps[best_eval_idx], eval_losses[best_eval_idx]),
            xytext=(eval_steps[best_eval_idx] + 30, eval_losses[best_eval_idx] + 0.1),
            arrowprops=dict(arrowstyle='->', color='black', lw=1.5),
            fontsize=11, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

plt.tight_layout()
output_file = OUTPUT_DIR / "01_train_vs_eval_loss.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ========================================================================
# Plot 2: Loss Reduction (Bar Chart)
# ========================================================================
print("📊 Creating Plot 2: Loss Reduction...")
fig, ax = plt.subplots(figsize=(10, 7))

categories = ['Train Loss', 'Eval Loss', 'Perplexity']
baseline_values = [train_losses[0], eval_losses[0], 11.05]  # baseline perplexity
finetuned_values = [train_losses[-1], eval_losses[-1], 2.17]  # final perplexity
improvements = [
    ((baseline_values[0] - finetuned_values[0]) / baseline_values[0]) * 100,
    ((baseline_values[1] - finetuned_values[1]) / baseline_values[1]) * 100,
    ((baseline_values[2] - finetuned_values[2]) / baseline_values[2]) * 100
]

x = np.arange(len(categories))
width = 0.35

bars1 = ax.bar(x - width/2, baseline_values, width, 
               label='Initial/Baseline', color=colors['baseline'], alpha=0.8)
bars2 = ax.bar(x + width/2, finetuned_values, width,
               label='Fine-tuned', color=colors['train'], alpha=0.8)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add improvement percentages
for i, (imp, x_pos) in enumerate(zip(improvements, x)):
    ax.text(x_pos, max(baseline_values[i], finetuned_values[i]) + 0.5,
            f'↓ {imp:.1f}%',
            ha='center', va='bottom', fontsize=12, fontweight='bold',
            color='green', bbox=dict(boxstyle='round,pad=0.3', 
                                     facecolor='lightgreen', alpha=0.7))

ax.set_xlabel('Metric', fontsize=14, fontweight='bold')
ax.set_ylabel('Value', fontsize=14, fontweight='bold')
ax.set_title('C1 Level: Baseline vs Fine-tuned Comparison', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=12)
ax.legend(fontsize=12, loc='upper right')
ax.grid(True, axis='y', alpha=0.3, color=colors['grid'])

plt.tight_layout()
output_file = OUTPUT_DIR / "02_baseline_comparison.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ========================================================================
# Plot 3: Learning Rate Schedule
# ========================================================================
if learning_rates:
    print("📊 Creating Plot 3: Learning Rate Schedule...")
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(train_steps[:len(learning_rates)], learning_rates, 
            color='#F18F01', linewidth=2.5, label='Learning Rate')
    
    ax.set_xlabel('Training Step', fontsize=14, fontweight='bold')
    ax.set_ylabel('Learning Rate', fontsize=14, fontweight='bold')
    ax.set_title('C1 Level: Learning Rate Schedule (Cosine)', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3, color=colors['grid'])
    ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    plt.tight_layout()
    output_file = OUTPUT_DIR / "03_learning_rate_schedule.png"
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_file}")
    plt.close()

# ========================================================================
# Plot 4: Train-Eval Gap Analysis
# ========================================================================
print("📊 Creating Plot 4: Train-Eval Gap...")
fig, ax = plt.subplots(figsize=(12, 7))

# Calculate gap at eval points
gaps = []
gap_steps = []
for eval_step, eval_loss in zip(eval_steps, eval_losses):
    # Find closest train loss
    closest_train_idx = min(range(len(train_steps)), 
                           key=lambda i: abs(train_steps[i] - eval_step))
    train_loss = train_losses[closest_train_idx]
    gap = eval_loss - train_loss
    gaps.append(gap)
    gap_steps.append(eval_step)

ax.plot(gap_steps, gaps, 'o-', color='#C73E1D', 
        linewidth=2.5, markersize=8, label='Train-Eval Gap')
ax.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)

# Fill area
ax.fill_between(gap_steps, 0, gaps, alpha=0.3, color='#C73E1D')

ax.set_xlabel('Training Step', fontsize=14, fontweight='bold')
ax.set_ylabel('Gap (Eval Loss - Train Loss)', fontsize=14, fontweight='bold')
ax.set_title('C1 Level: Overfitting Analysis (Train-Eval Gap)', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3, color=colors['grid'])

# Add annotation for increasing gap
max_gap_idx = gaps.index(max(gaps))
ax.annotate('Increasing Gap\n(Overfitting)', 
            xy=(gap_steps[max_gap_idx], gaps[max_gap_idx]),
            xytext=(gap_steps[max_gap_idx] - 50, gaps[max_gap_idx] + 0.03),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=11, fontweight='bold', color='red',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

plt.tight_layout()
output_file = OUTPUT_DIR / "04_overfitting_analysis.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ========================================================================
# Plot 5: Loss Progression Timeline
# ========================================================================
print("📊 Creating Plot 5: Loss Progression Timeline...")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)

# Train loss
ax1.plot(train_steps, train_losses, 'o-', 
         color=colors['train'], linewidth=2.5, markersize=5, alpha=0.8)
ax1.set_ylabel('Train Loss', fontsize=13, fontweight='bold')
ax1.set_title('C1 Level: Detailed Loss Progression', 
              fontsize=16, fontweight='bold', pad=20)
ax1.grid(True, alpha=0.3, color=colors['grid'])

# Add percentage drops
for i in range(1, len(eval_steps)):
    prev_loss = eval_losses[i-1]
    curr_loss = eval_losses[i]
    pct_change = ((curr_loss - prev_loss) / prev_loss) * 100
    color = 'green' if pct_change < 0 else 'red'
    ax1.text(eval_steps[i], train_losses[-1] + 0.05, 
             f'{pct_change:+.1f}%',
             ha='center', fontsize=9, color=color, fontweight='bold')

# Eval loss
ax2.plot(eval_steps, eval_losses, 's-', 
         color=colors['eval'], linewidth=2.5, markersize=7, alpha=0.8)
ax2.set_xlabel('Training Step', fontsize=13, fontweight='bold')
ax2.set_ylabel('Eval Loss', fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3, color=colors['grid'])

# Mark best checkpoint
best_idx = eval_losses.index(min(eval_losses))
ax2.scatter([eval_steps[best_idx]], [eval_losses[best_idx]], 
            s=200, color='gold', marker='*', zorder=5,
            edgecolors='black', linewidths=2, label='Best Checkpoint')
ax2.legend(fontsize=11)

plt.tight_layout()
output_file = OUTPUT_DIR / "05_detailed_progression.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✓ Saved: {output_file}")
plt.close()

# ========================================================================
# Summary
# ========================================================================
print("\n" + "="*60)
print("✅ ALL PLOTS CREATED SUCCESSFULLY!")
print("="*60)
print(f"\n📁 Output Directory: {OUTPUT_DIR}")
print("\n📊 Generated Plots:")
print("  1. Train vs Eval Loss - Loss curves comparison")
print("  2. Baseline Comparison - Bar chart showing improvements")
print("  3. Learning Rate Schedule - Cosine LR decay")
print("  4. Overfitting Analysis - Train-eval gap over time")
print("  5. Detailed Progression - Timeline with percentage changes")
print("\n" + "="*60)

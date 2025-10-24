"""
TensorBoard loglarından training grafikleri oluştur
"""

import os
from tensorboard.backend.event_processing import event_accumulator
import matplotlib.pyplot as plt
import numpy as np

# Paths
TENSORBOARD_DIR = "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/loras/llama1b-a1-unsloth-v2/runs/Oct24_12-20-32_muhammet-MS-7D67"
OUTPUT_DIR = "/home/muhammet/Documents/Tez/LLM_Degerlendirme/notebooks/fine_tuning/training_plots"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load TensorBoard data
ea = event_accumulator.EventAccumulator(TENSORBOARD_DIR)
ea.Reload()

print("📊 Available tags:", ea.Tags()['scalars'])

# Set style
plt.style.use('seaborn-v0_8-darkgrid')

# Plot 1: Training Loss
if 'train/loss' in ea.Tags()['scalars']:
    train_loss = ea.Scalars('train/loss')
    steps = [x.step for x in train_loss]
    values = [x.value for x in train_loss]
    
    plt.figure(figsize=(12, 6))
    plt.plot(steps, values, linewidth=2, color='#2E86AB')
    plt.xlabel('Steps', fontsize=12)
    plt.ylabel('Training Loss', fontsize=12)
    plt.title('A1 Fine-Tuning: Training Loss Over Time', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'training_loss.png'), dpi=300, bbox_inches='tight')
    print(f"✅ Saved: training_loss.png")
    plt.close()

# Plot 2: Evaluation Loss
if 'eval/loss' in ea.Tags()['scalars']:
    eval_loss = ea.Scalars('eval/loss')
    steps = [x.step for x in eval_loss]
    values = [x.value for x in eval_loss]
    
    plt.figure(figsize=(12, 6))
    plt.plot(steps, values, linewidth=2, marker='o', markersize=8, color='#A23B72')
    plt.xlabel('Steps', fontsize=12)
    plt.ylabel('Evaluation Loss', fontsize=12)
    plt.title('A1 Fine-Tuning: Evaluation Loss Over Time', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Mark best eval loss
    best_idx = np.argmin(values)
    best_step = steps[best_idx]
    best_value = values[best_idx]
    plt.scatter([best_step], [best_value], color='red', s=200, zorder=5, marker='*')
    plt.annotate(f'Best: {best_value:.4f}\n(Step {best_step})', 
                xy=(best_step, best_value), 
                xytext=(10, -30), 
                textcoords='offset points',
                fontsize=10,
                bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'eval_loss.png'), dpi=300, bbox_inches='tight')
    print(f"✅ Saved: eval_loss.png")
    plt.close()

# Plot 3: Combined Plot
if 'train/loss' in ea.Tags()['scalars'] and 'eval/loss' in ea.Tags()['scalars']:
    train_loss = ea.Scalars('train/loss')
    eval_loss = ea.Scalars('eval/loss')
    
    train_steps = [x.step for x in train_loss]
    train_values = [x.value for x in train_loss]
    eval_steps = [x.step for x in eval_loss]
    eval_values = [x.value for x in eval_loss]
    
    plt.figure(figsize=(14, 7))
    plt.plot(train_steps, train_values, linewidth=2, label='Training Loss', color='#2E86AB', alpha=0.8)
    plt.plot(eval_steps, eval_values, linewidth=2, marker='o', markersize=6, 
             label='Evaluation Loss', color='#A23B72', alpha=0.8)
    
    plt.xlabel('Steps', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.title('A1 Fine-Tuning: Training vs Evaluation Loss', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11, loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'combined_loss.png'), dpi=300, bbox_inches='tight')
    print(f"✅ Saved: combined_loss.png")
    plt.close()

# Plot 4: Learning Rate
if 'train/learning_rate' in ea.Tags()['scalars']:
    lr_data = ea.Scalars('train/learning_rate')
    steps = [x.step for x in lr_data]
    values = [x.value for x in lr_data]
    
    plt.figure(figsize=(12, 6))
    plt.plot(steps, values, linewidth=2, color='#F18F01')
    plt.xlabel('Steps', fontsize=12)
    plt.ylabel('Learning Rate', fontsize=12)
    plt.title('A1 Fine-Tuning: Learning Rate Schedule', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'learning_rate.png'), dpi=300, bbox_inches='tight')
    print(f"✅ Saved: learning_rate.png")
    plt.close()

print(f"\n🎉 All plots saved to: {OUTPUT_DIR}")

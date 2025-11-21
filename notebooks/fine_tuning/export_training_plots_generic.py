"""
Generic Training Plots Export Script
Tüm CEFR seviyeleri için TensorBoard loglarından grafikleri export eder

Kullanım:
    python export_training_plots_generic.py A1
    python export_training_plots_generic.py A2
    python export_training_plots_generic.py B1
    python export_training_plots_generic.py B2
    python export_training_plots_generic.py C1
    python export_training_plots_generic.py all  # Tüm seviyeleri işle
"""

import os
import sys
from pathlib import Path
from tensorboard.backend.event_processing import event_accumulator
import matplotlib.pyplot as plt
import numpy as np

# Seviye konfigürasyonları
LEVEL_CONFIGS = {
    'A1': {
        'tensorboard_dir': "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/loras/llama1b-a1-unsloth-v2/runs/Oct24_12-20-32_muhammet-MS-7D67",
        'output_dir': "/home/muhammet/Documents/Tez/LLM_Degerlendirme/notebooks/fine_tuning/training_plots/A1"
    },
    'A2': {
        'tensorboard_dir': "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/loras/llama1b-a2-unsloth-v1/runs/Oct26_13-26-12_muhammet-MS-7D67",
        'output_dir': "/home/muhammet/Documents/Tez/LLM_Degerlendirme/notebooks/fine_tuning/training_plots/A2"
    },
    'B1': {
        'tensorboard_dir': "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/loras/llama1b-b1-unsloth-v1/runs/Oct26_13-55-38_muhammet-MS-7D67",
        'output_dir': "/home/muhammet/Documents/Tez/LLM_Degerlendirme/notebooks/fine_tuning/training_plots/B1"
    },
    'B2': {
        'tensorboard_dir': "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/loras/llama1b-b2-unsloth-v1/runs",
        'output_dir': "/home/muhammet/Documents/Tez/LLM_Degerlendirme/notebooks/fine_tuning/training_plots/B2",
        'find_log': True  # B2 için log dosyasını bul
    },
    'C1': {
        'tensorboard_dir': "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/loras/llama1b-c1-unsloth-v2/checkpoint-290/trainer_state.json",
        'output_dir': "/home/muhammet/Documents/Tez/LLM_Degerlendirme/notebooks/fine_tuning/training_plots/C1",
        'use_json': True  # C1 JSON kullanıyor
    }
}


def find_tensorboard_log(directory):
    """TensorBoard log dosyasını dizinde ara"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith('events.out.tfevents'):
                return os.path.join(root, file)
    return None


def export_plots_tensorboard(level, config):
    """TensorBoard loglarından grafikleri export et"""
    tensorboard_dir = config['tensorboard_dir']
    output_dir = config['output_dir']
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"{level} SEVİYESİ - TRAINING PLOTS EXPORT")
    print(f"{'='*60}")
    print(f"📁 TensorBoard dizini: {tensorboard_dir}")
    print(f"📁 Çıktı dizini: {output_dir}")
    print()
    
    # B2 için log dosyasını bul
    if config.get('find_log'):
        log_file = find_tensorboard_log(tensorboard_dir)
        if not log_file:
            print(f"❌ {level} için TensorBoard log dosyası bulunamadı!")
            return False
        print(f"✓ Log dosyası bulundu: {os.path.basename(log_file)}")
        tensorboard_dir = log_file
    
    # Load TensorBoard data
    print("📂 TensorBoard verileri yükleniyor...")
    ea = event_accumulator.EventAccumulator(tensorboard_dir)
    ea.Reload()
    
    print("📊 Mevcut metrikler:", ea.Tags()['scalars'])
    print()
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Plot 1: Training Loss
    if 'train/loss' in ea.Tags()['scalars']:
        print(f"📈 1/5: Training Loss oluşturuluyor...")
        train_loss = ea.Scalars('train/loss')
        steps = [x.step for x in train_loss]
        values = [x.value for x in train_loss]
        
        plt.figure(figsize=(12, 6))
        plt.plot(steps, values, linewidth=2, color='#2E86AB')
        plt.xlabel('Steps', fontsize=12)
        plt.ylabel('Training Loss', fontsize=12)
        plt.title(f'{level} Fine-Tuning: Training Loss Over Time', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'training_loss.png'), dpi=300, bbox_inches='tight')
        print(f"   ✅ Kaydedildi: training_loss.png")
        plt.close()
    
    # Plot 2: Evaluation Loss
    if 'eval/loss' in ea.Tags()['scalars']:
        print(f"📈 2/5: Evaluation Loss oluşturuluyor...")
        eval_loss = ea.Scalars('eval/loss')
        steps = [x.step for x in eval_loss]
        values = [x.value for x in eval_loss]
        
        plt.figure(figsize=(12, 6))
        plt.plot(steps, values, linewidth=2, marker='o', markersize=8, color='#A23B72')
        plt.xlabel('Steps', fontsize=12)
        plt.ylabel('Evaluation Loss', fontsize=12)
        plt.title(f'{level} Fine-Tuning: Evaluation Loss Over Time', fontsize=14, fontweight='bold')
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
        plt.savefig(os.path.join(output_dir, 'eval_loss.png'), dpi=300, bbox_inches='tight')
        print(f"   ✅ Kaydedildi: eval_loss.png")
        plt.close()
    
    # Plot 3: Combined Plot
    if 'train/loss' in ea.Tags()['scalars'] and 'eval/loss' in ea.Tags()['scalars']:
        print(f"📈 3/5: Combined Loss oluşturuluyor...")
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
        
        # Mark best eval loss
        best_idx = np.argmin(eval_values)
        best_step = eval_steps[best_idx]
        best_value = eval_values[best_idx]
        plt.scatter([best_step], [best_value], color='red', s=200, zorder=5, marker='*', label='Best Eval')
        
        plt.xlabel('Steps', fontsize=12)
        plt.ylabel('Loss', fontsize=12)
        plt.title(f'{level} Fine-Tuning: Training vs Evaluation Loss', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11, loc='upper right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'combined_loss.png'), dpi=300, bbox_inches='tight')
        print(f"   ✅ Kaydedildi: combined_loss.png")
        plt.close()
    
    # Plot 4: Learning Rate
    if 'train/learning_rate' in ea.Tags()['scalars']:
        print(f"📈 4/5: Learning Rate oluşturuluyor...")
        lr_data = ea.Scalars('train/learning_rate')
        steps = [x.step for x in lr_data]
        values = [x.value for x in lr_data]
        
        plt.figure(figsize=(12, 6))
        plt.plot(steps, values, linewidth=2, color='#F18F01')
        plt.xlabel('Steps', fontsize=12)
        plt.ylabel('Learning Rate', fontsize=12)
        plt.title(f'{level} Fine-Tuning: Learning Rate Schedule (Cosine)', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'learning_rate.png'), dpi=300, bbox_inches='tight')
        print(f"   ✅ Kaydedildi: learning_rate.png")
        plt.close()
    
    # Plot 5: Gradient Norm (if available)
    if 'train/grad_norm' in ea.Tags()['scalars']:
        print(f"📈 5/5: Gradient Norm oluşturuluyor...")
        grad_norm = ea.Scalars('train/grad_norm')
        steps = [x.step for x in grad_norm]
        values = [x.value for x in grad_norm]
        
        plt.figure(figsize=(12, 6))
        plt.plot(steps, values, linewidth=1, alpha=0.6, color='#06A77D')
        # Add moving average
        window = 10
        if len(values) >= window:
            moving_avg = np.convolve(values, np.ones(window)/window, mode='valid')
            plt.plot(steps[window-1:], moving_avg, linewidth=2, color='#06A77D', label=f'Moving Avg (window={window})')
        plt.xlabel('Steps', fontsize=12)
        plt.ylabel('Gradient Norm', fontsize=12)
        plt.title(f'{level} Fine-Tuning: Gradient Norm Over Time', fontsize=14, fontweight='bold')
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'gradient_norm.png'), dpi=300, bbox_inches='tight')
        print(f"   ✅ Kaydedildi: gradient_norm.png")
        plt.close()
    
    print()
    print(f"{'='*60}")
    print(f"✅ {level} - Tüm grafikler başarıyla oluşturuldu!")
    print(f"📁 Konum: {output_dir}")
    print(f"{'='*60}")
    
    return True


def export_plots_json(level, config):
    """JSON dosyasından (C1 gibi) grafikleri export et"""
    import json
    
    json_file = config['tensorboard_dir']
    output_dir = config['output_dir']
    
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\n{'='*60}")
    print(f"{level} SEVİYESİ - TRAINING PLOTS EXPORT (JSON)")
    print(f"{'='*60}")
    print(f"📁 JSON dosyası: {json_file}")
    print(f"📁 Çıktı dizini: {output_dir}")
    print()
    
    # Load training data
    print("📂 Training verileri yükleniyor...")
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    logs = data['log_history']
    print(f"✓ {len(logs)} log kaydı yüklendi")
    
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
    
    print(f"✓ Train noktaları: {len(train_steps)}")
    print(f"✓ Eval noktaları: {len(eval_steps)}")
    print()
    
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Plot 1: Combined Loss
    print(f"📈 1/3: Combined Loss oluşturuluyor...")
    plt.figure(figsize=(14, 7))
    plt.plot(train_steps, train_losses, linewidth=2, label='Training Loss', 
             color='#2E86AB', alpha=0.8)
    plt.plot(eval_steps, eval_losses, linewidth=2, marker='o', markersize=6,
             label='Evaluation Loss', color='#A23B72', alpha=0.8)
    
    # Mark best eval loss
    best_eval_idx = eval_losses.index(min(eval_losses))
    best_step = eval_steps[best_eval_idx]
    best_value = eval_losses[best_eval_idx]
    plt.scatter([best_step], [best_value], color='red', s=200, zorder=5, marker='*', label='Best Eval')
    
    plt.xlabel('Steps', fontsize=12)
    plt.ylabel('Loss', fontsize=12)
    plt.title(f'{level} Fine-Tuning: Training vs Evaluation Loss', fontsize=14, fontweight='bold')
    plt.legend(fontsize=11, loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'combined_loss.png'), dpi=300, bbox_inches='tight')
    print(f"   ✅ Kaydedildi: combined_loss.png")
    plt.close()
    
    # Plot 2: Training Loss
    print(f"📈 2/3: Training Loss oluşturuluyor...")
    plt.figure(figsize=(12, 6))
    plt.plot(train_steps, train_losses, linewidth=2, color='#2E86AB')
    plt.xlabel('Steps', fontsize=12)
    plt.ylabel('Training Loss', fontsize=12)
    plt.title(f'{level} Fine-Tuning: Training Loss Over Time', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'training_loss.png'), dpi=300, bbox_inches='tight')
    print(f"   ✅ Kaydedildi: training_loss.png")
    plt.close()
    
    # Plot 3: Learning Rate
    if learning_rates:
        print(f"📈 3/3: Learning Rate oluşturuluyor...")
        plt.figure(figsize=(12, 6))
        plt.plot(train_steps[:len(learning_rates)], learning_rates, 
                color='#F18F01', linewidth=2.5, label='Learning Rate')
        plt.xlabel('Steps', fontsize=12)
        plt.ylabel('Learning Rate', fontsize=12)
        plt.title(f'{level} Fine-Tuning: Learning Rate Schedule (Cosine)', fontsize=14, fontweight='bold')
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'learning_rate.png'), dpi=300, bbox_inches='tight')
        print(f"   ✅ Kaydedildi: learning_rate.png")
        plt.close()
    
    print()
    print(f"{'='*60}")
    print(f"✅ {level} - Tüm grafikler başarıyla oluşturuldu!")
    print(f"📁 Konum: {output_dir}")
    print(f"{'='*60}")
    
    return True


def main():
    if len(sys.argv) < 2:
        print("Kullanım: python export_training_plots_generic.py <level>")
        print("Seviyeler: A1, A2, B1, B2, C1, all")
        sys.exit(1)
    
    level_arg = sys.argv[1].upper()
    
    if level_arg == 'ALL':
        levels_to_process = list(LEVEL_CONFIGS.keys())
    elif level_arg in LEVEL_CONFIGS:
        levels_to_process = [level_arg]
    else:
        print(f"❌ Geçersiz seviye: {level_arg}")
        print(f"Geçerli seviyeler: {', '.join(LEVEL_CONFIGS.keys())}, all")
        sys.exit(1)
    
    print("\n" + "🎨 TRAINING PLOTS EXPORT - GENERIC SCRIPT".center(60))
    print(f"İşlenecek seviyeler: {', '.join(levels_to_process)}\n")
    
    success_count = 0
    for level in levels_to_process:
        config = LEVEL_CONFIGS[level]
        
        try:
            if config.get('use_json'):
                success = export_plots_json(level, config)
            else:
                success = export_plots_tensorboard(level, config)
            
            if success:
                success_count += 1
        except Exception as e:
            print(f"\n❌ {level} işlenirken hata oluştu: {e}\n")
            continue
    
    print("\n" + "="*60)
    print(f"🎉 ÖZET: {success_count}/{len(levels_to_process)} seviye başarıyla işlendi!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()

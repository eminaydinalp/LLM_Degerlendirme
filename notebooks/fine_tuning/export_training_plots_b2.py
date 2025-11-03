"""
B2 Training Plots Export Script
TensorBoard loglarından grafikleri PNG olarak export eder
"""

import os
from tensorboard.backend.event_processing import event_accumulator
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # GUI olmadan çalışması için

# Paths
LOGDIR = "/media/muhammet/3f3fe6f9-0b61-46bd-a5b7-6cabd78bbc9a/home/user/text-generation-webui/user_data/loras/llama1b-b2-unsloth-v1/runs"
OUTPUT_DIR = "/home/muhammet/Documents/Tez/LLM_Degerlendirme/notebooks/fine_tuning/training_plots/B2"

# Output directory oluştur
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 60)
print("B2 TRAINING PLOTS EXPORT")
print("=" * 60)
print(f"📁 Log directory: {LOGDIR}")
print(f"📁 Output directory: {OUTPUT_DIR}")
print()

# TensorBoard log dosyasını bul
log_file = None
for root, dirs, files in os.walk(LOGDIR):
    for file in files:
        if file.startswith('events.out.tfevents'):
            log_file = os.path.join(root, file)
            break
    if log_file:
        break

if not log_file:
    print("❌ TensorBoard log dosyası bulunamadı!")
    exit(1)

print(f"✓ Log dosyası bulundu: {os.path.basename(log_file)}")
print()

# Event Accumulator ile logları yükle
ea = event_accumulator.EventAccumulator(log_file)
ea.Reload()

print("📊 Mevcut metrikler:")
scalar_tags = ea.Tags()['scalars']
for tag in scalar_tags:
    print(f"   - {tag}")
print()

# Metrikleri extract et
def extract_metric(tag):
    events = ea.Scalars(tag)
    steps = [e.step for e in events]
    values = [e.value for e in events]
    return steps, values

# 1. Training Loss
print("📈 Grafik 1/5: Training Loss")
steps, train_loss = extract_metric('train/loss')
plt.figure(figsize=(12, 6))
plt.plot(steps, train_loss, linewidth=2, color='#2E86AB')
plt.xlabel('Steps', fontsize=12)
plt.ylabel('Loss', fontsize=12)
plt.title('B2 Training Loss', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '1_training_loss.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✓ Kaydedildi: {output_path}")

# 2. Eval Loss
print("📈 Grafik 2/5: Eval Loss")
steps, eval_loss = extract_metric('eval/loss')
plt.figure(figsize=(12, 6))
plt.plot(steps, eval_loss, linewidth=2, color='#A23B72', marker='o', markersize=4)
plt.xlabel('Steps', fontsize=12)
plt.ylabel('Loss', fontsize=12)
plt.title('B2 Evaluation Loss', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '2_eval_loss.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✓ Kaydedildi: {output_path}")

# 3. Train + Eval Loss Combined
print("📈 Grafik 3/5: Combined Loss")
train_steps, train_loss = extract_metric('train/loss')
eval_steps, eval_loss = extract_metric('eval/loss')

plt.figure(figsize=(12, 6))
plt.plot(train_steps, train_loss, linewidth=2, color='#2E86AB', label='Train Loss', alpha=0.8)
plt.plot(eval_steps, eval_loss, linewidth=2, color='#A23B72', marker='o', markersize=4, label='Eval Loss')
plt.xlabel('Steps', fontsize=12)
plt.ylabel('Loss', fontsize=12)
plt.title('B2 Training vs Evaluation Loss', fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '3_combined_loss.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✓ Kaydedildi: {output_path}")

# 4. Learning Rate
print("📈 Grafik 4/5: Learning Rate")
steps, lr = extract_metric('train/learning_rate')
plt.figure(figsize=(12, 6))
plt.plot(steps, lr, linewidth=2, color='#F18F01')
plt.xlabel('Steps', fontsize=12)
plt.ylabel('Learning Rate', fontsize=12)
plt.title('B2 Learning Rate Schedule (Cosine)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '4_learning_rate.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✓ Kaydedildi: {output_path}")

# 5. Gradient Norm
print("📈 Grafik 5/5: Gradient Norm")
steps, grad_norm = extract_metric('train/grad_norm')
plt.figure(figsize=(12, 6))
plt.plot(steps, grad_norm, linewidth=2, color='#06A77D', alpha=0.7)
plt.xlabel('Steps', fontsize=12)
plt.ylabel('Gradient Norm', fontsize=12)
plt.title('B2 Gradient Norm', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.tight_layout()
output_path = os.path.join(OUTPUT_DIR, '5_gradient_norm.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"   ✓ Kaydedildi: {output_path}")

print()
print("=" * 60)
print("✅ TÜM GRAFİKLER OLUŞTURULDU!")
print("=" * 60)
print(f"📁 Grafikleri görmek için: {OUTPUT_DIR}")
print()

# Özet bilgi
print("📊 TRAINING ÖZET:")
print(f"   - İlk train loss: {train_loss[0]:.2f}")
print(f"   - Son train loss: {train_loss[-1]:.2f}")
print(f"   - İyileşme: {((train_loss[0] - train_loss[-1]) / train_loss[0] * 100):.1f}%")
print()
print(f"   - İlk eval loss: {eval_loss[0]:.2f}")
print(f"   - En iyi eval loss: {min(eval_loss):.2f}")
print(f"   - İyileşme: {((eval_loss[0] - min(eval_loss)) / eval_loss[0] * 100):.1f}%")
print()

# Training Plots Export Scripts

## Generic Script (Önerilen)

Tüm CEFR seviyeleri için tek bir script ile grafikleri export edebilirsiniz:

```bash
# Tek bir seviye için
python export_training_plots_generic.py A1
python export_training_plots_generic.py A2
python export_training_plots_generic.py B1
python export_training_plots_generic.py B2
python export_training_plots_generic.py C1

# Tüm seviyeler için tek seferde
python export_training_plots_generic.py all
```

## Eski Scriptler (Artık Kullanılmıyor)

Eski seviye-bazlı scriptler hala mevcut ama generic script kullanılması önerilir:
- `export_training_plots.py` (A1)
- `export_training_plots_a2.py`
- `export_training_plots_b1.py`
- `export_training_plots_b2.py`
- `export_training_plots_c1.py`

## Oluşturulan Grafikler

Her seviye için şu grafikler oluşturulur:
1. **training_loss.png** - Training loss over time
2. **eval_loss.png** - Evaluation loss with best checkpoint marked
3. **combined_loss.png** - Training vs Evaluation loss comparison
4. **learning_rate.png** - Learning rate schedule
5. **gradient_norm.png** - Gradient norm over time (TensorBoard seviyeleri için)

## Grid Oluşturma

Tüm seviyelerin combined_loss grafiklerini tek bir grid'de birleştirmek için:

```bash
python combine_all_levels_grid.py
```

Bu komut `all_levels_combined_loss_grid.png` dosyasını oluşturur.

## Gereksinimler

- TensorBoard
- Matplotlib
- NumPy

Python environment: text-generation-webui venv kullanılmalı.

import json
from pathlib import Path
r = json.loads(Path('results/cp05/training_report.json').read_text(encoding='utf-8'))
lines = [f"Experiment: {r['experiment_id']}", f"Device: {r['environment']['device']}", f"Python: {r['environment']['python'].split()[0]}", f"PyTorch: {r['environment']['pytorch']}", f"Config SHA-256: {r['config_sha256']}", "Selection: validation cross-entropy only", ""]
for model, values in r['models'].items():
    lines.append(f"[{model}] best_epoch={values['best_epoch']} best_val_loss={values['best_val_loss']:.6f} train_seconds={values['train_seconds']:.3f}")
    for row in values['history']:
        lines.append(f"epoch={row['epoch']:02d} train_loss={row['train_loss']:.6f} val_loss={row['val_loss']:.6f}")
    lines.append('')
Path('results/cp05/training.log').write_text('\n'.join(lines), encoding='utf-8')

import json
from collections import Counter
from pathlib import Path
import numpy as np

path = Path('results/cp05/evaluation/test_metrics.json')
report = json.loads(path.read_text(encoding='utf-8'))
models = {}
for kind in ('framewise', 'mstcn'):
    rows = [r for r in report['results'] if r['model'] == kind]
    labels = rows[0]['action']['confusion_matrix']['labels']
    confusion = sum((np.asarray(r['action']['confusion_matrix']['rows_true_columns_predicted'], dtype=np.int64) for r in rows), start=np.zeros((len(labels), len(labels)), dtype=np.int64))
    classes = {}
    for i, label in enumerate(labels):
        tp = int(confusion[i, i]); support = int(confusion[i].sum()); predicted = int(confusion[:, i].sum())
        precision = tp / predicted if predicted else 0.0
        recall = tp / support if support else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        classes[label] = {'support': support, 'precision': precision, 'recall': recall, 'f1': f1}
    errors = []
    for i, true_name in enumerate(labels):
        for j, pred_name in enumerate(labels):
            if i != j and confusion[i, j]:
                errors.append((int(confusion[i,j]), true_name, pred_name))
    models[kind] = {'confusion': confusion.tolist(), 'classes': classes, 'top_confusions': sorted(errors, reverse=True)[:12]}
out = {'split': report['split'], 'video_ids': report['results'][::2][0:0], 'models': models}
out['video_ids'] = sorted({r['video_id'] for r in report['results']})
Path('results/cp05/evaluation/per_class_and_confusion.json').write_text(json.dumps(out, indent=2), encoding='utf-8')
lines = ['# CP05 Error Analysis', '', 'Scope: four held-out S2 test executions; frame support is aggregated across these four videos. Pooled precision/recall/F1 and confusion counts are computed from the stored true-row/predicted-column confusion matrices.', '']
for kind, data in models.items():
    lines += [f'## {kind}', '', '| Action | Support (frames) | Precision | Recall | F1 |', '|---|---:|---:|---:|---:|']
    for label, values in data['classes'].items():
        lines.append(f"| {label} | {values['support']} | {values['precision']:.3f} | {values['recall']:.3f} | {values['f1']:.3f} |")
    supported = [(label, v) for label, v in data['classes'].items() if v['support'] > 0 and label != 'NULL']
    lines += ['', 'Top supported actions by pooled F1: ' + ', '.join(f"{a} ({v['f1']:.3f}; n={v['support']})" for a,v in sorted(supported,key=lambda x:x[1]['f1'],reverse=True)[:4]) + '.', 'Lowest supported actions by pooled F1: ' + ', '.join(f"{a} ({v['f1']:.3f}; n={v['support']})" for a,v in sorted(supported,key=lambda x:x[1]['f1'])[:5]) + '.', 'Top frame confusions (true → predicted): ' + ', '.join(f'{a} → {b} ({n})' for n,a,b in data['top_confusions'][:8]) + '.', '']
lines += ['## Interpretation', '', 'Compare with `baseline_comparison.json` for unweighted per-video action/segment metrics. MS-TCN substantially reduces the sequence-order/segmentation errors reflected in Edit and segmental F1, but its test performance is still modest; confusion and rare-action rows should guide the next data/annotation/representation review. No process-semantic conclusion is drawn from TAS-S action labels.']
Path('results/cp05/evaluation/error_analysis.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')

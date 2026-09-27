import json
from pathlib import Path
feature_path = Path('experiments/CP05/feature_readiness.json')
video_path = Path('experiments/CP05/video_readiness.json')
feature = json.loads(feature_path.read_text(encoding='utf-8'))
video = json.loads(video_path.read_text(encoding='utf-8'))
feature['video_qa'] = video['video_qa']
feature['readiness']['videos'] = video['readiness']['videos']
Path('experiments/CP05_data_readiness.json').write_text(json.dumps(feature, indent=2), encoding='utf-8')

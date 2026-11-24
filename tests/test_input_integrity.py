from pathlib import Path
import json


def test_manifest_is_json_and_records_expected_count():
    path=Path(__file__).resolve().parents[1]/'data'/'source_manifest.json'
    data=json.loads(path.read_text(encoding='utf-8'))
    assert 'local_sources' in data
    assert len([item for item in data['local_sources'] if item['filename'].lower().endswith('.mp4')]) == 3

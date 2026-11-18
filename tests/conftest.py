# Module configuration for tests

import sys
import json
from pathlib import Path
import pytest

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

@pytest.fixture
def temp_data_file(tmp_path):
    file_path = tmp_path / "data.json"
    initial_data = {
        "people": ["Anna", "Erik", "Lisa"],
        "taken": [False, True, False],
    }
    file_path.write_text(json.dumps(initial_data, indent="\t"), encoding="utf-8")
    return file_path
import importlib
import json
import sys
from unittest.mock import MagicMock, patch
import pytest

@pytest.fixture
def loaded_config(temp_data_file, monkeypatch):
    sys.modules.pop("config", None)

    mock_tk = MagicMock()
    monkeypatch.setattr("pathlib.Path.with_name", lambda self, name: temp_data_file)
    monkeypatch.setattr("time.sleep", lambda _: None)

    with patch.dict(sys.modules, {"tkinter": mock_tk}):
        import config
        yield config

    sys.modules.pop("config", None)

def test_config_initial_load(loaded_config):
    assert loaded_config.data["people"] == ["Anna", "Erik", "Lisa"]
    assert loaded_config.data["taken"] == [False, True, False]
    assert loaded_config.listbox.insert.call_count == 3

def test_config_add_new_person(loaded_config):
    loaded_config.entry.get.return_value = "  Kalle  "
    loaded_config.add()

    assert "Kalle" in loaded_config.data["people"]
    assert loaded_config.data["people"][-1] == "Kalle"
    assert loaded_config.data["taken"][-1] is False
    loaded_config.entry.delete.assert_called_with(0, loaded_config.tk.END)

def test_config_add_empty_or_whitespace_ignored(loaded_config):
    loaded_config.entry.get.return_value = "    "
    loaded_config.add()

    assert len(loaded_config.data["people"]) == 3
    assert len(loaded_config.data["taken"]) == 3

def test_config_add_duplicate_triggers_prank_save_and_destroy(loaded_config, temp_data_file):
    loaded_config.entry.get.return_value = "Johan"
    loaded_config.add()

    loaded_config.entry.get.return_value = "Anna"  # Duplicate
    with patch("config.sleep"), patch("config.clear") as mock_clear:
        loaded_config.add()
        mock_clear.assert_called_once()
        loaded_config.root.destroy.assert_called_once()

    saved = json.loads(temp_data_file.read_text(encoding="utf-8"))
    assert "Johan" in saved["people"]
    assert saved["people"].count("Anna") == 1

def test_config_remove_selected_person(loaded_config):
    loaded_config.listbox.curselection.return_value = (1,) # Bort med Erik
    loaded_config.remove()

    assert loaded_config.data["people"] == ["Anna", "Lisa"]
    assert loaded_config.data["taken"] == [False, False]
    loaded_config.listbox.delete.assert_called_once_with(1)

def test_config_remove_nothing_selected_does_not_crash(loaded_config):
    loaded_config.listbox.curselection.return_value = ()
    loaded_config.remove()

    assert loaded_config.data["people"] == ["Anna", "Erik", "Lisa"]

def test_config_save_writes_to_disk(loaded_config, temp_data_file):
    loaded_config.data["people"].append("Maja")
    loaded_config.data["taken"].append(False)

    with patch("config.sleep"):
        loaded_config.save()

    saved = json.loads(temp_data_file.read_text(encoding="utf-8"))
    assert saved["people"] == ["Anna", "Erik", "Lisa", "Maja"]
    assert saved["taken"] == [False, True, False, False]

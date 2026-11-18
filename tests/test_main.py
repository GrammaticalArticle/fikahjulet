import json
import sys
from unittest.mock import patch


def test_main_picks_available_winner_and_saves(temp_data_file, monkeypatch, capsys):
    sys.modules.pop("main", None)

    monkeypatch.setattr("pathlib.Path.with_name", lambda self, name: temp_data_file)
    monkeypatch.setattr("builtins.input", lambda _: "")
    monkeypatch.setattr("time.sleep", lambda _: None)

    with patch("random.choice", side_effect=lambda seq: seq[-1]) as mock_choice, \
         patch("random.randint", return_value=12):
        import main

        mock_choice.assert_called_once_with([0, 2])
        assert main.winnerindex == 2

    saved = json.loads(temp_data_file.read_text(encoding="utf-8"))
    assert saved["taken"] == [False, True, True]

    captured = capsys.readouterr()
    assert "Fikahjulet landade på Lisa" in captured.out

    sys.modules.pop("main", None)

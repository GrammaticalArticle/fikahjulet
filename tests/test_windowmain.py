import json
import math
import sys
from unittest.mock import MagicMock, patch
import pytest


@pytest.fixture
def run_windowmain(temp_data_file, monkeypatch):
    """
    Runs windowmain.py headlessly by mocking Tkinter and stepping through
    all root.after(16, animate) frames iteratively in a while loop.
    """
    sys.modules.pop("windowmain", None)

    mock_tk = MagicMock()
    mock_root = MagicMock()
    mock_root.winfo_screenwidth.return_value = 1920
    mock_root.winfo_screenheight.return_value = 1080
    mock_tk.Tk.return_value = mock_root

    def make_toplevel(*args, **kwargs):
        win = MagicMock()
        win.winfo_x.return_value = 1200
        win.winfo_y.return_value = 500
        return win

    mock_tk.Toplevel.side_effect = make_toplevel

    # Queue the next frame instead of recursing 2,700 levels deep
    pending_callbacks = []

    def queue_after(delay, callback):
        pending_callbacks.append(callback)

    def run_mainloop():
        while pending_callbacks:
            cb = pending_callbacks.pop(0)
            cb()

    mock_root.after.side_effect = queue_after
    mock_root.mainloop.side_effect = run_mainloop

    monkeypatch.setattr("pathlib.Path.with_name", lambda self, name: temp_data_file)
    monkeypatch.setattr("builtins.input", lambda _: "")

    # Patch both sys.modules["tkinter"] AND windowdef.tk so zero real windows open
    with patch.dict(sys.modules, {"tkinter": mock_tk}), \
         patch("windowdef.tk", mock_tk), \
         patch("random.choice", side_effect=lambda seq: seq[-1]) as mock_choice, \
         patch("windowdef.load_avatar", return_value=None):
        import windowmain
        yield windowmain, mock_tk, mock_root, mock_choice

    sys.modules.pop("windowmain", None)


def test_windowmain_selects_only_available_winner(run_windowmain):
    wm, _, _, mock_choice = run_windowmain
    mock_choice.assert_called_once_with([0, 2])
    assert wm.winnerindex == 2
    assert wm.winner_name == "Lisa"


def test_windowmain_creates_cards_and_arrow_windows(run_windowmain):
    wm, _, _, _ = run_windowmain
    assert len(wm.cards) == 3
    assert wm.arrow_win is not None


def test_windowmain_rotates_exact_angle_to_winner(run_windowmain):
    wm, _, _, _ = run_windowmain
    final_winner_angle = (wm.total_rotation + (wm.winnerindex * wm.step_angle)) % (2 * math.pi)
    assert final_winner_angle == pytest.approx(0.0, abs=1e-9) or final_winner_angle == pytest.approx(2 * math.pi, abs=1e-9)


def test_windowmain_completes_all_7_phases(run_windowmain):
    wm, _, mock_root, _ = run_windowmain
    expected_total_frames = (
        wm.phase1_frames + wm.phase2_frames + wm.phase3_frames +
        wm.phase4_frames + wm.phase5_frames + wm.phase6_frames +
        wm.phase7_frames
    )
    assert wm.frame == expected_total_frames
    assert mock_root.after.call_count == expected_total_frames


def test_windowmain_traffic_lights_created_and_destroyed(run_windowmain):
    wm, _, _, _ = run_windowmain
    assert wm.traffic_lights == []
    assert wm.red_line_win is not None
    assert wm.end_line_win is not None


def test_windowmain_updates_winner_crown_and_saves_json(run_windowmain, temp_data_file):
    wm, _, _, _ = run_windowmain
    _, winner_frame, winner_name_lbl, winner_sub_lbl = wm.cards[wm.winnerindex]

    winner_frame.configure.assert_any_call(bg="#ca8a04")
    winner_name_lbl.configure.assert_any_call(
        font=("Helvetica", 16, "bold"),
        bg="#ca8a04",
        text="👑 Lisa 👑",
    )
    winner_sub_lbl.configure.assert_any_call(
        font=("Helvetica", 11, "bold"),
        bg="#ca8a04",
        fg="#fef08a",
        text="DUBBELVINNARE!",
    )

    saved = json.loads(temp_data_file.read_text(encoding="utf-8"))
    assert saved["taken"] == [False, True, True]


def test_windowmain_spawns_close_button_at_end(run_windowmain):
    wm, mock_tk, mock_root, _ = run_windowmain
    mock_tk.Button.assert_called_once()
    assert mock_tk.Button.call_args.kwargs["text"] == "Stäng hjul ✕"
    assert mock_tk.Button.call_args.kwargs["command"] == mock_root.destroy

def test_windowmain_renders_avatar_when_present(temp_data_file, monkeypatch):
    sys.modules.pop("windowmain", None)

    mock_tk = MagicMock()
    mock_root = MagicMock()
    mock_root.winfo_screenwidth.return_value = 1920
    mock_root.winfo_screenheight.return_value = 1080
    mock_tk.Tk.return_value = mock_root

    pending_callbacks = []
    mock_root.after.side_effect = lambda delay, cb: pending_callbacks.append(cb)
    mock_root.mainloop.side_effect = lambda: [cb() for cb in iter(lambda: pending_callbacks.pop(0) if pending_callbacks else None, None)]

    monkeypatch.setattr("pathlib.Path.with_name", lambda self, name: temp_data_file)
    monkeypatch.setattr("builtins.input", lambda _: "")

    fake_avatar = MagicMock()
    with patch.dict(sys.modules, {"tkinter": mock_tk}), \
         patch("windowdef.tk", mock_tk), \
         patch("windowdef.load_avatar", return_value=fake_avatar):
        import windowmain
        assert fake_avatar in windowmain.avatar_references

    sys.modules.pop("windowmain", None)

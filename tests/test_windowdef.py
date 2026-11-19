# Testerna var gjorda med hjälp av AI då jag inte orkar göra en massa tester för hand

import json
import math
from unittest.mock import MagicMock, patch
import pytest
from PIL import Image
from windowdef import (
    lerp,
    ease_out_cubic,
    get_line_pos,
    get_circle_pos,
    load_avatar,
    finish_spin,
    close_button,
)

@pytest.mark.parametrize(
    "a, b, t, expected",
    [
        (0, 100, 0.0, 0),
        (0, 100, 1.0, 100),
        (0, 100, 0.5, 50),
        (-50, 50, 0.5, 0),
        (100, 0, 0.25, 75),
    ],
)
def test_lerp(a, b, t, expected):
    assert lerp(a, b, t) == pytest.approx(expected)

def test_ease_out_cubic_boundaries_and_curve():
    assert ease_out_cubic(0.0) == 0.0
    assert ease_out_cubic(1.0) == 1.0
    assert ease_out_cubic(0.2) > 0.2
    assert ease_out_cubic(0.5) == pytest.approx(0.875)

def test_get_line_pos_single_and_multiple():
    x1, y1 = get_line_pos(0, screen_w=1920, screen_h=1080, n=1, win_h=62)
    assert x1 == int(1920 * 0.15)
    assert isinstance(y1, int)

    coords = [get_line_pos(i, 1920, 1080, n=4, win_h=62) for i in range(4)]
    xs = [c[0] for c in coords]
    ys = [c[1] for c in coords]
    assert len(set(xs)) == 1
    assert ys == sorted(ys)
    assert (ys[1] - ys[0]) == pytest.approx(ys[2] - ys[1], abs=1)


@pytest.mark.parametrize(
    "rot, expected_dx, expected_dy",
    [
        (0.0, 100, 0),               # Right (3 o'clock)
        (math.pi / 2, 0, 100),       # Bottom (6 o'clock)
        (math.pi, -100, 0),          # Left (9 o'clock)
        (3 * math.pi / 2, 0, -100),  # Top (12 o'clock)
    ],
)
def test_get_circle_pos_quadrants(rot, expected_dx, expected_dy):
    cx, cy, radius, win_w, win_h = 500, 400, 100, 40, 20
    x, y = get_circle_pos(0, rot=rot, step_angle=0, cx=cx, cy=cy, radius=radius, win_w=win_w, win_h=win_h)
    assert x == int(cx + expected_dx - (win_w / 2))
    assert y == int(cy + expected_dy - (win_h / 2))


def test_load_avatar_missing_returns_none(tmp_path, monkeypatch):
    import windowdef
    monkeypatch.setattr(windowdef, "__file__", str(tmp_path / "windowdef.py"))
    assert load_avatar(1, win_h=62) is None
    assert load_avatar(None, win_h=62) is None

def test_load_avatar_valid_image_preserves_aspect_ratio(tmp_path, monkeypatch):
    import windowdef
    monkeypatch.setattr(windowdef, "__file__", str(tmp_path / "windowdef.py"))

    avatar_dir = tmp_path / "avatar"
    avatar_dir.mkdir()
    img_path = avatar_dir / "avatar1.png"
    Image.new("RGBA", (200, 100), color="red").save(img_path)

    with patch("windowdef.ImageTk.PhotoImage", side_effect=lambda img: img) as mock_photo:
        resized_img = load_avatar(1, win_h=62)
        mock_photo.assert_called_once()
        assert resized_img.size == (100, 50)

def test_load_avatar_corrupt_file_returns_none(tmp_path, monkeypatch):
    import windowdef
    monkeypatch.setattr(windowdef, "__file__", str(tmp_path / "windowdef.py"))

    avatar_dir = tmp_path / "avatar"
    avatar_dir.mkdir()
    (avatar_dir / "avatar1.png").write_text("not a valid png file", encoding="utf-8")

    assert load_avatar(1, win_h=62) is None

def test_finish_spin_updates_winner_and_writes_json(temp_data_file):
    data = json.loads(temp_data_file.read_text(encoding="utf-8"))
    people = data["people"]
    taken = data["taken"]

    cards = [(MagicMock(), MagicMock(), MagicMock(), MagicMock()) for _ in people]

    finish_spin(people, cards, winnerindex=2, taken=taken, data_path=temp_data_file, data=data)

    win, frame_w, name_lbl, sub_lbl = cards[2]
    win.title.assert_called_once_with("! VINNARE !")
    frame_w.configure.assert_called_once_with(bg="#15803d")
    name_lbl.configure.assert_called_once_with(bg="#15803d", fg="#ffffff", text="★ Lisa ★")
    sub_lbl.configure.assert_called_once_with(bg="#15803d", fg="#bbf7d0", text="BJUDER PÅ FIKA!")
    win.lift.assert_called_once()

    cards[0][0].title.assert_not_called()


    updated = json.loads(temp_data_file.read_text(encoding="utf-8"))
    assert updated["taken"] == [False, True, True]

def test_close_button_clears_children_and_creates_button():
    child1, child2 = MagicMock(), MagicMock()
    arrow_frame = MagicMock()
    arrow_frame.winfo_children.return_value = [child1, child2]
    root = MagicMock()

    with patch("windowdef.tk.Button") as mock_btn:
        close_button(arrow_frame, root)
        child1.destroy.assert_called_once()
        child2.destroy.assert_called_once()
        mock_btn.assert_called_once()
        assert mock_btn.call_args.kwargs["command"] == root.destroy
        mock_btn.return_value.pack.assert_called_once_with(expand=True, fill="both")

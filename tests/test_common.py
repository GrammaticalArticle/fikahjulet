# Den här var gjord med hjälp av AI då jag inte
# visste hur jag skulle göra tester utan
# att allting kraschar

from unittest.mock import patch
import pytest
from common import clear, format_json, loadinganimation, waveanimation

def test_animations_are_non_empty():
    assert len(loadinganimation) > 0
    assert len(waveanimation) > 0
    assert all(isinstance(frame, str) for frame in loadinganimation)
    assert all(isinstance(frame, str) for frame in waveanimation)

@patch("os.system")
@patch("os.name", "nt")
def test_clear_windows(mock_system):
    clear()
    mock_system.assert_called_once_with("cls")

@patch("os.system")
@patch("os.name", "posix")
def test_clear_unix(mock_system):
    clear()
    mock_system.assert_called_once_with("clear")

def test_format_json_generates_defaults_when_empty():
    data = {}
    taken, people, out_data = format_json([], [], data)
    assert len(people) == 10
    assert people == [f"Person {i + 1}" for i in range(10)]
    assert taken == [False] * 10
    assert out_data["people"] == people

def test_format_json_generates_defaults_when_none():
    data = {}
    taken, people, out_data = format_json([], None, data)
    assert len(people) == 10
    assert len(taken) == 10
    assert out_data["taken"] == [False] * 10

@pytest.mark.parametrize(
    "people, taken, expected",
    [
        (["A", "B", "C"], [], [False, False, False]),
        (["A", "B", "C"], [True], [True, False, False]),
        (["A", "B", "C"], [False, True], [False, True, False]),
    ],
)
def test_format_json_extends_short_taken(people, taken, expected):
    data = {}
    res_taken, _, out_data = format_json(taken, people, data)
    assert res_taken == expected
    assert out_data["taken"] == expected

@pytest.mark.parametrize(
    "people, taken, expected",
    [
        (["A"], [False, True, True], [False]),
        (["A", "B"], [False, True, True, False], [False, True]),
    ],
)
def test_format_json_trims_long_taken(people, taken, expected):
    data = {}
    res_taken, _, out_data = format_json(taken, people, data)
    assert res_taken == expected
    assert out_data["taken"] == expected

def test_format_json_resets_when_all_true():
    data = {}
    people = ["Anna", "Bo", "Cia", "Dan"]
    taken = [True, True, True, True]
    res_taken, _, out_data = format_json(taken, people, data)
    assert res_taken == [False, False, False, False]
    assert out_data["taken"] == [False, False, False, False]

def test_format_json_single_person_all_true_resets():
    data = {}
    people = ["Solo"]
    taken = [True]
    res_taken, _, _ = format_json(taken, people, data)
    assert res_taken == [False]

def test_format_json_preserves_valid_mixed_state():
    people = ["Anna", "Bo", "Cia"]
    taken = [True, False, True]
    data = {"people": people, "taken": taken}
    res_taken, res_people, out_data = format_json(taken, people, data)
    assert res_people == ["Anna", "Bo", "Cia"]
    assert res_taken == [True, False, True]
    assert out_data is data

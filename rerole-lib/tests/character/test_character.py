import json

from rerole_lib import Sheet
from rerole_lib.utils import Dict

def test_build_effect_index():
    with open("tests/character/test_data.json") as f:
        data = Sheet(json.load(f))

    data.build_effect_index()
    effect_index = data.get("effect_index")

    assert effect_index["strength"] == [
        ["spells", "mighty strength"],
        ["equipment", "belt of stronk"],
    ]

    assert effect_index["dexterity"] == [
        ["equipment", "belt of dex"],
    ]

    assert effect_index["will"] == [
        ["spells", "Sacred Oath", "1"],
        ["feats", "iron will"],
        ["equipment", "cloak of resistance"],
    ]

    assert effect_index["acrobatics"] == [
        ["spells", "general skill buff", "1"],
        ["feats", "skill focus (acrobatics)"],
    ]

def test_calculate():
    with open("tests/character/test_data.json") as f:
        data = Sheet(json.load(f))
    data.calculate()

    assert data.get_in(["skills", "climb", "modifier"]) == 11
    assert data.get_in(["saves", "will", "modifier"]) == 11

def test_antimagic():
    with open("tests/character/test_data.json") as f:
        data = Sheet(json.load(f))

    data.calculate()
    assert data.get_in(["skills", "acrobatics", "modifier"]) == 9

    data["antimagic_field"] = True
    data.calculate()
    assert data.get_in(["skills", "acrobatics", "modifier"]) == 5

    data["antimagic_field"] = False
    data.calculate()
    assert data.get_in(["skills", "acrobatics", "modifier"]) == 9

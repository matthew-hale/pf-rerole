import json

from rerole_lib import character as c, utils

def test_build_effect_index():
    with open("tests/character/test_data.json") as f:
        data = json.load(f)

    effect_index = c.build_effect_index(data)

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
        data = json.load(f)
    c.calculate(data)

    assert utils.get_in(data, ["skills", "climb", "modifier"]) == 11
    assert utils.get_in(data, ["saves", "will", "modifier"]) == 11

def test_antimagic():
    with open("tests/character/test_data.json") as f:
        data = json.load(f)

    c.calculate(data)
    assert utils.get_in(data, ["skills", "acrobatics", "modifier"]) == 9

    data["antimagic_field"] = True
    c.calculate(data)
    assert utils.get_in(data, ["skills", "acrobatics", "modifier"]) == 5

    data["antimagic_field"] = False
    c.calculate(data)
    assert utils.get_in(data, ["skills", "acrobatics", "modifier"]) == 9

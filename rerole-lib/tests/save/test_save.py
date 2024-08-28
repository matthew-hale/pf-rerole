from rerole_lib import save

def test_save_calculation():
    effect_total = 8

    data = {
        "value": 4,
        "ability": "dexterity",
    }

    save.calculate(data, effect_total)
    assert data.get("modifier") == 12

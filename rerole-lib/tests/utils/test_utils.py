from rerole_lib import utils

def test_get_in():
    data = {
        "a": {
            1: {
                "apple": 1,
                "banana": 2,
            },
            2: {
                "chestnut": 3,
            },
            3: {},
        },
        "b": {
            4: {
                "dragonfruit": 4,
            },
            5: {
                "eclair": 5,
            },
        },
        "c": {
        },
    }

    assert utils.get_in(data, ["a", 1, "apple"]) == 1
    assert utils.get_in(data, ["a", 2]) == {"chestnut": 3}
    assert utils.get_in(data, ["a", 3]) == {}
    assert utils.get_in(data, ["a", 3], "default") == {}
    assert utils.get_in(data, ["a", 4]) == None
    assert utils.get_in(data, ["a", 4], "default") == "default"
    assert utils.get_in(data, ["a", 4, "dragonfruit"]) == None
    assert utils.get_in(data, ["a", 4, "dragonfruit"], "default") == "default"
    assert utils.get_in(data, ["c"]) == {}
    assert utils.get_in(data, ["c"], "default") == {}
    assert utils.get_in(data, ["d"]) == None
    assert utils.get_in(data, ["d"], "default") == "default"

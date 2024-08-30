from rerole_lib.utils import Dict

def test_get_in():
    data = Dict({
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
    })

    assert data.get_in(["a", 1, "apple"]) == 1
    assert data.get_in(["a", 2]) == {"chestnut": 3}
    assert data.get_in(["a", 3]) == {}
    assert data.get_in(["a", 3], "default") == {}
    assert data.get_in(["a", 4]) == None
    assert data.get_in(["a", 4], "default") == "default"
    assert data.get_in(["a", 4, "dragonfruit"]) == None
    assert data.get_in(["a", 4, "dragonfruit"], "default") == "default"
    assert data.get_in(["c"]) == {}
    assert data.get_in(["c"], "default") == {}
    assert data.get_in(["d"]) == None
    assert data.get_in(["d"], "default") == "default"

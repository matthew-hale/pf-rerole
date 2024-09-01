from rerole_lib.utils import Dict

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
    "e": {
        "stuff": [
            {
                "apple": 10,
                "banana": 20,
            },
            {
                "lemon": 30,
                "lime": 40,
            },
        ],
    }
})

def test_get_in():

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

    assert data.get_in(["e", "stuff", 0, "apple"]) == 10
    assert data.get_in(["e", "stuff", 0, "banana"]) == 20
    assert data.get_in(["e", "stuff", 0, "lemon"]) == None
    assert data.get_in(["e", "stuff", 0, "lime"]) == None
    assert data.get_in(["e", "stuff", 1, "apple"]) == None
    assert data.get_in(["e", "stuff", 1, "banana"]) == None
    assert data.get_in(["e", "stuff", 1, "lemon"]) == 30
    assert data.get_in(["e", "stuff", 1, "lime"]) == 40
    assert data.get_in(["e", "stuff", 2]) == None
    assert data.get_in(["e", "stuff", 2, "apple"]) == None

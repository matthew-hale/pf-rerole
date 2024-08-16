from functools import reduce

def get_in(data: dict, keys: list):
    """A la Clojure's `get-in`; like .get, but uses a sequence of keys.

    To facilitate the common python idiom for checking the existence of a key (comparing to None), this function returns 'None' instead of '{}' in the event that a key is missing. This allows, e.g., the following to work:

    data = {
        "a": 1,
        "b": {"alpha": 0, "beta": 3.14},
        "c": 4,
    }

    want = get_in(data, ["b", "alpha"])
    if want is None:
        ...
    """
    output = reduce(lambda c, k: c.get(k, {}), keys, data)
    if output == {}:
        output = None
    return output

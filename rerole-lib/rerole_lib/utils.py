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

    Note that the result is the actual object within `data`; if it's mutable, updates to it will also update `data` in place.

    E.g.:

    data = {
        "a": {
            "b": {
                "value": 1
            }
        }
    }

    b = get_in(data, ["a", "b"])
    b["value"] = "banana"
    print(data)
    {
        "a": {
            "b": {
                "value": "banana"
            }
        }
    }
    """
    output = reduce(lambda c, k: c.get(k, {}), keys, data)
    if output == {} or not keys:
        output = None
    return output

def search(data: dict, fn, path=[]) -> list | None:
    """Return a list of key sequences whose values return True when `fn` is applied to them.

    Somewhat like `filter`, except it returns the "locations" of the matching values within the input dictionary.
    """
    if not data:
        return None

    matching_key_sequences = []
    for k, v in data.items():
        current_path = list(path)
        current_path.append(k)

        v_matches_fn = fn(v)
        v_has_children = isinstance(v, dict)

        if v_matches_fn:
            matching_key_sequences.append(current_path)
        if v_has_children:
            results = search(v, fn, current_path)
            if results:
                for x in results:
                    matching_key_sequences.append(x)

    return matching_key_sequences

def add_or_append(data: dict, key, val):
    """Append val to data[key], initializing with data[key] = [] if needed."""
    if key not in data.keys():
        data[key] = []
    data[key].append(val)

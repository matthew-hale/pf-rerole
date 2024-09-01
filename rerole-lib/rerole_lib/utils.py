from functools import reduce

class Dict(dict):
    """Provides some utility methods on standard dictionaries that I find helpful."""
    def get_in(self, key_seq: list, default=None):
        """Wraps `utils.get_in()`"""
        return get_in(self, key_seq, default)

    def search(self, fn, path=[]) -> list | None:
        """Wraps `utils.search`"""
        return search(self, fn)

    def add_or_append(self, key, val):
        """Append val to data[key], initializing with data[key] = [] if needed.

        This basically assumes that data[key] is a list or list-like object, and appends the provided value to it. Just didn't want to keep writing this by hand.
        """
        if key not in self.keys():
            self[key] = []
        self[key].append(val)


def get_in(data, key_seq, default=None):
    """A la Clojure's `get-in`; like .get, but uses a sequence of keys.

    This function mimics Clojure's `get-in` function. Provide it with a sequence of keys and an optional default value, and it will return either the specified nested value, or the default.

    Example:

        data = {
            "a": {
                1: {
                    "apple": "tasty",
                },
            },
            "b": [
                {"bagel": "everything"},
                {"bagel": "asiago"},
                {"bagel": "plain"},
                {"bagel": "sesame seed"},
            ]
        })
        get_in(data, ["a", 1, "apple"])
        # 'tasty'

        get_in(data, ["a", 1])
        # {'apple': 'tasty'}

        get_in(data, ["a", 1, "banana"]) # returns None
        get_in(data, ["a", 2, "banana"]) # returns None
        get_in(data, ["a", 2])           # returns None
        get_in(data, ["b"])              # returns None

        get_in(data, ["a", 1, "banana"], default={})
        # {}

    Note that Python's dict and list types do not implement a common interface for a safe "get" operation. Whereas in Clojure, a call to `get-in` on a list of dicts of lists of dicts would "just work," it would not normally work in Python.

    It does, however, work here, because I made it so:

        get_in(data, ["b", 1, "bagel"])
        # "asiago"

    The default value of `None` for the `default` parameter makes `get_in` behave like Python's own `.get()` method for dictionaries. It would have been more personally useful to set the default to `{}`, but I wanted to stick to the normal language behavior as much as possible.

    One scenario that this function trips up on is when `None` is a possible valid value. I think it should basically never be a valid value, so I don't really care to fix this, but beware:

        data["a"][1]["cucumber"] = None
        get_in(data, ["a", 1, "cucumber"], default="pickles")
        # 'pickles'
    """
    if not data or not key_seq:
        return default

    def getter(data, key):
        if data is None:
            return None
        try:
            keys = data.keys()
        except AttributeError:
            # Might be a list
            pass
        else:
            # Is a dict
            if key not in keys:
                return None
            return data.get(key)

        try:
            return data[key]
        except:
            # Either isn't a list, or the index was out of range
            return None

    output = reduce(getter, key_seq, data)
    if output is None:
        return default
    return output

def search(data, fn, path=[]):
    """Return a list of matching key sequences in `data`, where fn(data.get_in(seq)) is True.

    Somewhat like `filter`, except it returns the "locations" of the matching values within the input dictionary. These "locations" can then be used in `.get_in()` to find the associated values, if desired.

    Example:

        data = {
            "a": 1,
            "b": [
                {
                    "cat": True,
                    "dog": False,
                },
                {
                    "cat": False,
                    "dog": True,
                },
            ],
            "c": {
                "apple": True,
                "banana": False,
                "pear": True,
            },
            "d": True,
            "e": {
                "f": {
                    "coconut": True,
                },
            },
        })

        data.search(lambda x: x is True)
        [
            ['b', 0, 'cat'],
            ['b', 1, 'dog'],
            ['c', 'apple'],
            ['c', 'pear'],
            ['d'],
            ['e', 'f', 'coconut']
        ]
    """
    if not data:
        return None

    matching_key_sequences = []

    try:
        for key, val in data.items():
            current_path = list(path)
            current_path.append(key)

            try:
                _ = [x for x in val]
                val_has_children = True
            except:
                val_has_children = False

            val_has_no_children = not val_has_children
            val_matches = fn(val)

            if val_matches:
                matching_key_sequences.append(current_path)
            if val_has_no_children:
                continue

            results = search(val, fn, current_path)
            if not results:
                continue

            for match in results:
                matching_key_sequences.append(match)
        return matching_key_sequences
    except AttributeError:
        pass # It's a list

    for idx, val in enumerate(data):
        current_path = list(path)
        current_path.append(idx)

        try:
            _ = [x for x in value]
            val_has_children = True
        except:
            val_has_children = False

        val_has_no_children = not val_has_children
        val_matches = fn(val)

        if val_matches:
            matching_key_sequences.append(current_path)
        if val_has_no_children:
            continue
        results = search(value, fn, current_path)
        if not results:
            continue
        for match in results:
            matching_key_sequences.append(match)
    return matching_key_sequences

from functools import reduce

def get_in(data: dict, keys: list, default=None):
    """A la Clojure's `get-in`; like .get, but uses a sequence of keys.

    This function mimics Clojure's `get-in` function. Provide it with a dictionary, a sequence of keys, and an optional default value, and it will return either the specified nested dictionary value, or the default.

    For example:

    >>> data = {
    ...     "a": {
    ...         1: {
    ...             "apple": "tasty",
    ...         },
    ...     },
    ... }
    >>> get_in(data, ["a", 1, "apple"])
    'tasty'
    >>>
    >>> get_in(data, ["a", 1])
    {'apple': 'tasty'}
    >>>
    >>> get_in(data, ["a", 1, "banana"]) # returns None
    >>> get_in(data, ["a", 2, "banana"]) # returns None
    >>> get_in(data, ["a", 2])           # returns None
    >>> get_in(data, ["b"])              # returns None
    >>>
    >>> get_in(data, ["a", 1, "banana"] default={})
    {}
    >>>

    The default value of `None` makes `get_in` behave like Python's own `.get()` method for dictionaries. It would have been more personally useful to set the default to `{}`, but I wanted to stick to the normal language behavior as much as possible.

    One scenario that this function trips up on is when `None` is a possible valid value. I think it should basically never be a valid value, so I don't really care to fix this, but beware:

    >>> data
    {'a': {1: {'apple': 'tasty'}}}
    >>>
    """
    if not keys:
        return default

    def getter(data, key):
        if data is None:
            return None
        if key not in data:
            return None
        return data.get(key)

    output = reduce(getter, keys, data)
    if output is None:
        return default
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

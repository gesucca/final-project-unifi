"""Discretization of countinous attributes in datasets."""


class _DiscRange:
    def __init__(self, minimum, maximum):
        self._label = str(minimum) + '-' + str(maximum)
        self._min = minimum
        self._max = maximum

    def in_range(self, value):
        """Are you happy, damned linter? What could this function possibly do?"""
        return self._min <= value <= self._max

    def get_label(self):
        """As above."""
        return self._label


def _discretize(value, ranges):
    if value == 'n.c.' or value == '<5':
        return value.upper()

    range_found = False

    for rng in ranges:
        if rng.in_range(float(value)):
            value = rng.get_label()
            range_found = True
            break

    if not range_found:
        value = 'OUT_OF_RANGE'

    return value


def discretize(source, dest, keys, ranges, drop):
    """Discretization of countinous attributes in datasets.
    WARNING: keys and ranges must match positionally!"""
    if len(keys) != len(ranges):
        raise Exception('Keys and ranges length are different!')

    for doc in source.find():
        if drop:
            source.delete_one(doc)

        for i in range(len(keys)):
            for k in list(doc.keys()):
                if keys[i] in k:
                    doc[k] = _discretize(doc[k], ranges[i])

        dest.insert_one(doc)

    if drop:
        source.drop()

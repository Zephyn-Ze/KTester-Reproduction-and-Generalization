import collections
import numbers
import re


SizeUnit = collections.namedtuple('SizeUnit', 'divider, symbol, name')
CombinedUnit = collections.namedtuple('CombinedUnit', 'decimal, binary')

disk_size_units = (
    CombinedUnit(SizeUnit(1000**1, 'KB', 'kilobyte'), SizeUnit(1024**1, 'KiB', 'kibibyte')),
    CombinedUnit(SizeUnit(1000**2, 'MB', 'megabyte'), SizeUnit(1024**2, 'MiB', 'mebibyte')),
    CombinedUnit(SizeUnit(1000**3, 'GB', 'gigabyte'), SizeUnit(1024**3, 'GiB', 'gibibyte')),
    CombinedUnit(SizeUnit(1000**4, 'TB', 'terabyte'), SizeUnit(1024**4, 'TiB', 'tebibyte')),
    CombinedUnit(SizeUnit(1000**5, 'PB', 'petabyte'), SizeUnit(1024**5, 'PiB', 'pebibyte')),
    CombinedUnit(SizeUnit(1000**6, 'EB', 'exabyte'), SizeUnit(1024**6, 'EiB', 'exbibyte')),
    CombinedUnit(SizeUnit(1000**7, 'ZB', 'zettabyte'), SizeUnit(1024**7, 'ZiB', 'zebibyte')),
    CombinedUnit(SizeUnit(1000**8, 'YB', 'yottabyte'), SizeUnit(1024**8, 'YiB', 'yobibyte')),
)


def is_string(value):
    return isinstance(value, str)


def format(text, *args, **kw):
    if args:
        text %= args
    if kw:
        text = text.format(**kw)
    return text


def tokenize(text):
    tokenized_input = []
    for token in re.split(r'(\d+(?:\.\d+)?)', text):
        token = token.strip()
        if re.match(r'\d+\.\d+', token):
            tokenized_input.append(float(token))
        elif token.isdigit():
            tokenized_input.append(int(token))
        elif token:
            tokenized_input.append(token)
    return tokenized_input


class InvalidSize(Exception):
    pass


def parse_size(size, binary=False):
    """
    Parse a human readable data size and return the number of bytes.

    :param size: The human readable file size to parse (a string).
    :param binary: :data:`True` to use binary multiples of bytes (base-2) for
                   ambiguous unit symbols and names, :data:`False` to use
                   decimal multiples of bytes (base-10).
    :returns: The corresponding size in bytes (an integer).
    :raises: :exc:`InvalidSize` when the input can't be parsed.

    This function knows how to parse sizes in bytes, kilobytes, megabytes,
    gigabytes, terabytes and petabytes. Some examples:

    >>> from humanfriendly import parse_size
    >>> parse_size('42')
    42
    >>> parse_size('13b')
    13
    >>> parse_size('5 bytes')
    5
    >>> parse_size('1 KB')
    1000
    >>> parse_size('1 kilobyte')
    1000
    >>> parse_size('1 KiB')
    1024
    >>> parse_size('1 KB', binary=True)
    1024
    >>> parse_size('1.5 GB')
    1500000000
    >>> parse_size('1.5 GB', binary=True)
    1610612736
    """
    tokens = tokenize(size)
    if tokens and isinstance(tokens[0], numbers.Number):
        # Get the normalized unit (if any) from the tokenized input.
        normalized_unit = tokens[1].lower() if len(tokens) == 2 and is_string(tokens[1]) else ''
        # If the input contains only a number, it's assumed to be the number of
        # bytes. The second token can also explicitly reference the unit bytes.
        if len(tokens) == 1 or normalized_unit.startswith('b'):
            return int(tokens[0])
        # Otherwise we expect two tokens: A number and a unit.
        if normalized_unit:
            # Convert plural units to singular units, for details:
            # https://github.com/xolox/python-humanfriendly/issues/26
            normalized_unit = normalized_unit.rstrip('s')
            for unit in disk_size_units:
                # First we check for unambiguous symbols (KiB, MiB, GiB, etc)
                # and names (kibibyte, mebibyte, gibibyte, etc) because their
                # handling is always the same.
                if normalized_unit in (unit.binary.symbol.lower(), unit.binary.name.lower()):
                    return int(tokens[0] * unit.binary.divider)
                # Now we will deal with ambiguous prefixes (K, M, G, etc),
                # symbols (KB, MB, GB, etc) and names (kilobyte, megabyte,
                # gigabyte, etc) according to the caller's preference.
                if (normalized_unit in (unit.decimal.symbol.lower(), unit.decimal.name.lower()) or
                        normalized_unit.startswith(unit.decimal.symbol[0].lower())):
                    return int(tokens[0] * (unit.binary.divider if binary else unit.decimal.divider))
    # We failed to parse the size specification.
    msg = "Failed to parse size! (input %r was tokenized as %r)"
    raise InvalidSize(format(msg, size, tokens))

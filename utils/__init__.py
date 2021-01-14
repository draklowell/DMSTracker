from . import version
from fractions import Fraction


def isInt(val):
    try:
        int(val)
        return True
    except ValueError:
        return False


def sizeToString(size):
    power = 2 ** 10
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        n += 1
    return str(size) + " " + power_labels[n] + 'B'


def timeToString(time):
    intervals = {
        "years": 12,
        'months': Fraction(30, 7),
        'weeks': 7,
        'days': 24,
        'hours': 60,
        'minutes': 60,
        'seconds': 1,
    }
    int_powers = list(reversed(intervals.keys()))
    n = 0
    power = intervals[int_powers[n]]
    while time >= power:
        time = round(time/power)
        n += 1
        if n >= len(int_powers):
            break
        power = intervals[int_powers[n]]
    return str(time) + " " + int_powers[n-1]

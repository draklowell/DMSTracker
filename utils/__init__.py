from . import version


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

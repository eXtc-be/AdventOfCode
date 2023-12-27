# tools.py - some tools to be used by other programs

import functools
import time


# evaluates an integer and returns the integer and a string
# the string is empty if the integer d==1, 's' in any other case
def evalPlural(d):
    return d, (d != 1 and 's' or '')


# takes a duration in seconds and converts it to a more readable form
# 1. all fields, no matter if they're zero
# 2. only nonzero fields
# 3. no zero leading fields
def convertSeconds(duration, mode=3):
    days, hours = divmod(duration, 24 * 60 * 60)
    hours, minutes = divmod(hours, 60 * 60)
    minutes, seconds = divmod(minutes, 60)
    milliseconds = 0

    second_format = ''
    if days or hours or minutes or seconds > 10:
        second_format = '%d second%s'
    elif seconds > 2:
        second_format = '%0.1f second%s'
    elif seconds > 1:
        second_format = '%0.2f second%s'
    else:  # seconds < 0
        seconds, milliseconds = round(seconds), round(seconds * 1000)
        second_format = '%d second%s'

    r = ''

    # mode 1: return all fields, no matter what their value
    # e.g. 0 days, 0 hours, 3 minutes and 0 seconds
    if mode == 1:
        r += '%d day%s, ' % evalPlural(days)
        r += '%d hour%s, ' % evalPlural(hours)
        r += '%d minute%s, ' % evalPlural(minutes)
        r += second_format % evalPlural(seconds) + ', '
        if milliseconds:
            r += '%d millisecond%s' % evalPlural(milliseconds)
        else: r = r[:-2]

    # mode 2: don't return any fields with value==0
    # e.g. 3 hours, 2 seconds
    if mode == 2:
        if days: r += '%d day%s, ' % evalPlural(days)
        if hours: r += '%d hour%s, ' % evalPlural(hours)
        if minutes: r += '%d minute%s, ' % evalPlural(minutes)
        if seconds: r += second_format % evalPlural(seconds) + ', '
        if milliseconds:
            r += '%d millisecond%s' % evalPlural(milliseconds)
        else:
            r = r[:-2]

    # mode 3: don't return any leading fields with value==0
    # e.g. 3 minutes and 0 seconds
    if mode == 3:
        if days:
            r += '%d day%s, ' % evalPlural(days)
            r += '%d hour%s, ' % evalPlural(hours)
            r += '%d minute%s and ' % evalPlural(minutes)
            r += second_format % evalPlural(seconds)
        else:
            if hours:
                r += '%d hour%s, ' % evalPlural(hours)
                r += '%d minute%s and ' % evalPlural(minutes)
            else:
                if minutes:
                    r += '%d minute%s and ' % evalPlural(minutes)
                    r += second_format % evalPlural(seconds)
                else:
                    if seconds:
                        r += second_format % evalPlural(seconds)
                    else:
                        r += '%d millisecond%s' % evalPlural(milliseconds)

    return r


def time_it(func):
    """record and print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {convertSeconds(run_time)}")
        return value

    return wrapper


if __name__ == "__main__":
    for test in (
            0.3456789,
            1.3456789,
            2.3456789,
            12.3456789,
            56*60+12.3456789,
            3*3600+56*60+12.3456789,
            (24*2+3)*3600+56*60+12.3456789,
            (24*2+0)*3600+0*60+12.3456789,
    ):
        print(convertSeconds(test, 1))
        print(convertSeconds(test, 2))
        print(convertSeconds(test, 3))
        print('-' * 50)

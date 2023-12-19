# evaluates an integer and returns the integer and a string

# the string is empty if the integer d==1, 's' in any other case
def evalPlural(d):
    return d, (d != 1 and 's' or '')


# takes a duration in seconds and converts it to a more readable form
# 1. all fields, no matter if they're zero
# 2. only nonzero fields
# 3. no zero leading fields
def convertSeconds(duration, mode=3):
    days = duration // (24 * 60 * 60)
    duration %= (24 * 60 * 60)
    hours = duration // (60 * 60)
    duration %= (60 * 60)
    minutes = duration // (60)
    duration %= (60)
    seconds = duration
    r = ''

    # mode 1: return all fields, no matter what their value
    # eg. 0 days, 0 hours, 3 minutes and 0 seconds
    if mode == 1:
        r += '%d day%s, ' % evalPlural(days)
        r += '%d hour%s, ' % evalPlural(hours)
        r += '%d minute%s and ' % evalPlural(minutes)
        r += '%d second%s' % evalPlural(seconds)

    # mode 2: don't return any fields with value==0
    # e.g. 3 hours, 2 seconds
    if mode == 2:
        if days: r += '%d day%s, ' % evalPlural(days)
        if hours: r += '%d hour%s, ' % evalPlural(hours)
        if minutes: r += '%d minute%s, ' % evalPlural(minutes)
        if seconds:
            r += '%d second%s' % evalPlural(seconds)
        else:
            r = r[:-1]

    # mode 3: don't return any leading fields with value==0
    # e.g. 3 minutes and 0 seconds
    if mode == 3:
        if days:
            r += '%d day%s, ' % evalPlural(days)
            r += '%d hour%s, ' % evalPlural(hours)
            r += '%d minute%s and ' % evalPlural(minutes)
            r += '%d second%s' % evalPlural(seconds)
        else:
            if hours:
                r += '%d hour%s, ' % evalPlural(hours)
                r += '%d minute%s and ' % evalPlural(minutes)
                r += '%d second%s' % evalPlural(seconds)
            else:
                if minutes:
                    r += '%d minute%s and ' % evalPlural(minutes)
                    r += '%d second%s' % evalPlural(seconds)
                else:
                    r += '%d second%s' % evalPlural(int(seconds))

    if r == '0 seconds': r = 'less than 1 second'

    return r

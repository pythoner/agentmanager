import datetime


TRUE_STRINGS = ('1', 't', 'true', 'on', 'y', 'yes')
FALSE_STRINGS = ('0', 'f', 'false', 'off', 'n', 'no')


def date2str(date):
    return date.strftime("%Y-%m-%d %H:%M:%S")


def str2date(string):
    return datetime.datetime.strptime(string, "%Y-%m-%d %H:%M:%S")


def bool_from_string(subject, strict=False):
    """Interpret a string as a boolean.

    A case-insensitive match is performed such that strings matching 't',
    'true', 'on', 'y', 'yes', or '1' are considered True and, when
    `strict=False`, anything else is considered False.

    Useful for JSON-decoded stuff and config file parsing.

    If `strict=True`, unrecognized values, including None, will raise a
    ValueError which is useful when parsing values passed in from an API call.
    Strings yielding False are 'f', 'false', 'off', 'n', 'no', or '0'.
    """
    if not isinstance(subject, basestring):
        subject = str(subject)

    lowered = subject.strip().lower()

    if lowered in TRUE_STRINGS:
        return True
    elif lowered in FALSE_STRINGS:
        return False
    elif strict:
        acceptable = ', '.join(
            "'%s'" % s for s in sorted(TRUE_STRINGS + FALSE_STRINGS))
        msg = "Unrecognized value '%(val)s', acceptable values are:"\
              " %(acceptable)s" % {'val': subject, 'acceptable': acceptable}
        raise ValueError(msg)
    else:
        return False


def meet_decimal_digits(fee, number=6):
    if round(fee, number) - fee != 0:
        return False
    else:
        return True

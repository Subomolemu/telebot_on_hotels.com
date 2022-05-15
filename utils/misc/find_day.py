from datetime import datetime

def days(day_in, day_out):
    format = '%Y-%m-%d'
    fmt_day_in = datetime.strptime(day_in, format).date()
    fmt_day_out = datetime.strptime(day_out, format).date()
    find_day = (fmt_day_out - fmt_day_in).days
    return find_day
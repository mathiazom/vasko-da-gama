from dateutil.relativedelta import relativedelta as rd


def readable_delta(seconds):
    if seconds < 60:
        return "less than a minute"
    delta = rd(seconds=seconds)
    readable = ""
    if delta.days > 1:
        readable += f"{delta.days} days, "
    elif delta.days == 1:
        readable += f"{delta.days} day, "
    if delta.hours > 1:
        readable += f"{delta.hours} hours, "
    elif delta.hours == 1:
        readable += f"{delta.hours} hour, "
    if delta.minutes > 1:
        readable += f"{delta.minutes} minutes, "
    elif delta.minutes == 1:
        readable += f"{delta.minutes} minute, "
    readable = readable[:-2]  # remove excess comma and space
    readable = " and".join(readable.rsplit(",", 1))  # replace last comma with ' and'
    return readable
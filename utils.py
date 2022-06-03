import datetime
import os

from dateutil.relativedelta import relativedelta as rd


def next_of_weekday(today, weekday):
    return today + datetime.timedelta((weekday - today.isoweekday()) % 7)


def timestamp_for_message_schedule(message_schedule):
    schedule_date = next_of_weekday(datetime.datetime.today(), message_schedule['weekday'])
    schedule_datetime = schedule_date.replace(**message_schedule['time'])
    return int(schedule_datetime.timestamp())


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


# Create an empty file to mark a successful run
def write_checkpoint_file(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)
    # Simply write to file before immediately closing it
    open(f"{dir}/{str(datetime.date.today().isoformat())}", "w").close()

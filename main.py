import os

import datetime
import time
import csv

from dotenv import load_dotenv

from reminders import reminder_messages
from schedule import is_scheduled, schedule_message
from utils import write_checkpoint_file, next_of_weekday

load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']

CHECKPOINTS_DIR = os.getenv('CHECKPOINTS_DIR', 'checkpoints')

COMMUNAL = "Fellesvask"


def timestamp_for_message_schedule(message_schedule):
    schedule_date = next_of_weekday(datetime.datetime.today(), message_schedule['weekday'])
    schedule_datetime = schedule_date.replace(**message_schedule['time'])
    return int(schedule_datetime.timestamp())


def get_weeks_cleaners():
    current_week = int(datetime.datetime.today().strftime("%V"))
    with open('gamaslist.csv', mode='r') as file:
        for lines in csv.reader(file):
            if int(lines[0]) == current_week:
                if lines[1] == COMMUNAL:
                    return COMMUNAL
                return lines[1], lines[2]
    return None


def schedule_reminders():
    cleaners = get_weeks_cleaners()
    if cleaners is None:
        print("[FAILED] No cleaners found")
        return
    print(f"[INFO] This weeks cleaners: {cleaners}")
    for m in reminder_messages(cleaners):
        timestamp = timestamp_for_message_schedule(m['schedule'])
        if timestamp < time.time():
            print("[WARNING] Scheduled time is in the past, skipping message.")
            continue
        if is_scheduled(timestamp):
            print("[WARNING] Message already scheduled, skipping.")
            write_checkpoint_file(CHECKPOINTS_DIR)
            continue
        schedule_message(m)


if __name__ == '__main__':
    schedule_reminders()

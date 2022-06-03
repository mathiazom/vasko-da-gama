from datetime import datetime
from pytz import timezone
import sys
import time
import csv

import direct
from config import Config
from definitions import APP_ROOT
from reminders import reminder_messages
from schedule import is_scheduled, schedule_message
from utils import write_checkpoint_file, timestamp_for_message_schedule

config = Config.from_config_file(APP_ROOT / "config.yaml")
tz = timezone(config.timezone)


def get_weeks_cleaners():
    current_week = int(datetime.today().strftime("%V"))
    with open(config.cleaning_schedule, mode='r') as file:
        for lines in csv.reader(file):
            if int(lines[0]) == current_week:
                if lines[1] == config.communal_keyword:
                    return config.communal_keyword
                return lines[1], lines[2]
    return None


def get_chores(is_communal):
    if "chores" not in config:
        return None
    chores = []
    if is_communal:
        if "communal" not in config.chores:
            return None
        with open(config.chores.communal, mode='r') as file:
            chores.append(file.read())
    else:
        if "pair" not in config.chores:
            return None
        for chores_file in config.chores.pair:
            with open(chores_file, mode='r') as file:
                chores.append(file.read())
    return chores


def get_reminder(reminder_id):
    cleaners = get_weeks_cleaners()
    if cleaners is None:
        print("[FAILED] No cleaners found")
        return None
    print(f"[INFO] This weeks cleaners: {cleaners}")
    is_communal = cleaners == config.communal_keyword
    return reminder_messages(
        cleaners,
        is_communal,
        get_chores(is_communal)
    )[reminder_id]


def schedule_reminder(reminder_id):
    reminder = get_reminder(reminder_id)
    timestamp = timestamp_for_message_schedule(reminder['schedule'])
    if timestamp < time.time():
        print("[WARNING] Scheduled time is in the past, skipping message.")
        return
    if is_scheduled(config.slack.bot_token, config.slack.channel_id, timestamp):
        print("[WARNING] Message already scheduled, skipping.")
        write_checkpoint_file(config.checkpoints_dir)
        return
    if schedule_message(config.slack.bot_token, config.slack.channel_id, reminder):
        write_checkpoint_file(config.checkpoints_dir)


def post_reminder(reminder_id):
    if direct.post_reminder(
            config.slack.bot_token,
            config.slack.channel_id,
            get_reminder(reminder_id)
    ):
        write_checkpoint_file(config.checkpoints_dir)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        op = sys.argv[1]
        if op == "direct":
            if len(sys.argv) > 2:
                post_reminder(sys.argv[2])
            else:
                print("[FAIL] Operation 'direct' requires a reminder id")
        elif op == "schedule":
            if len(sys.argv) > 2:
                schedule_reminder(sys.argv[2])
            else:
                print("[FAIL] Operation 'schedule' requires a reminder id")
        else:
            print("[FAIL] Operation argument must be either 'direct' or 'schedule'")
    else:
        print("[FAIL] Missing operation argument. Use 'direct' to post reminders now, or 'schedule' to schedule")

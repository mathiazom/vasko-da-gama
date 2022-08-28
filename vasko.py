from datetime import datetime
import sys
import time
import csv
from typing import Optional, List, Dict, Any

from munch import Munch

import direct
from config import Config
from definitions import APP_ROOT
from reminders import reminder_messages
from schedule import is_scheduled, schedule_message
from utils import write_checkpoint_file, timestamp_for_message_schedule

config = Config.from_config_file(APP_ROOT / "config.yaml")


def get_current_week() -> int:
    return int(datetime.today().strftime("%V"))


def get_weeks_cleaners(cleaning_schedule_file, communal_keyword) -> Optional[List[str]]:
    current_week = get_current_week()
    with open(cleaning_schedule_file, mode='r') as file:
        for line in csv.reader(file):
            if int(line[0]) == current_week:
                if line[1] == communal_keyword:
                    return communal_keyword
                return line[1:]
    return None


def get_weeks_special_chore(special_chores_file) -> str:
    current_week = get_current_week()
    with open(special_chores_file, mode='r') as file:
        chores = []
        for line in csv.reader(file):
            chores.append(line)
        return "- " + "\n- ".join(chores[current_week % len(chores)])


def get_chores(chores_config, is_communal) -> Optional[Dict[str, any]]:
    chores = Munch()
    if is_communal:
        if "communal" not in chores_config:
            return None
        with open(chores_config.communal, mode='r') as file:
            chores.communal = file.read()
    else:
        if "pair" not in chores_config:
            return None
        chores.pair = []
        for chores_file in chores_config.pair:
            with open(chores_file, mode='r') as file:
                chores.pair.append(file.read())
        if "special" in chores_config:
            chores.special = get_weeks_special_chore(chores_config.special)
    return chores


def get_reminder(reminder_id) -> Optional[Dict[str, Any]]:
    if config is None:
        print("[FAILED] Config missing when retrieving reminder")
        return None
    if "cleaning_schedule" not in config:
        print("[FAILED] Missing cleaning schedule in config")
        return None
    cleaners = get_weeks_cleaners(config.cleaning_schedule, config.communal_keyword)
    if cleaners is None:
        print("[FAILED] No cleaners found")
        return None
    print(f"[INFO] This weeks cleaners: {cleaners}")
    is_communal = cleaners == config.communal_keyword
    reminders = reminder_messages(
        cleaners,
        is_communal,
        get_chores(config.chores, is_communal) if "chores" in config else None
    )
    if reminder_id not in reminders:
        print(f"[FAILED] No reminder for id '{reminder_id}'")
        return None
    return reminders[reminder_id]


def schedule_reminder(reminder_id) -> None:
    reminder = get_reminder(reminder_id)
    if reminder is None:
        print("[FAILED] No reminder found, aborting.")
        return
    timestamp = timestamp_for_message_schedule(reminder['schedule'])
    if timestamp < time.time():
        print("[WARNING] Scheduled time is in the past, skipping message.")
        return
    if config is None:
        print("[FAILED] Could not schedule reminder, config missing")
        return
    if "slack" not in config:
        print("[FAILED] Could not schedule reminder, Slack config missing")
        return
    if is_scheduled(config.slack.bot_token, config.slack.channel_id, timestamp):
        print("[WARNING] Message already scheduled, skipping.")
        write_checkpoint_file(config.checkpoints_dir)
        return
    if schedule_message(config.slack.bot_token, config.slack.channel_id, reminder):
        write_checkpoint_file(config.checkpoints_dir)


def post_reminder(reminder_id) -> None:
    reminder = get_reminder(reminder_id)
    if reminder is None:
        print("[FAILED] No reminder found, aborting.")
        return
    if config is None:
        print("[FAILED] Could not post reminder, config missing")
        return
    if "slack" not in config:
        print("[FAILED] Could not post reminder, Slack config missing")
        return
    if direct.post_reminder(
            config.slack.bot_token,
            config.slack.channel_id,
            reminder
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

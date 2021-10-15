import os

import requests
import datetime
import time
import csv

from dotenv import load_dotenv

from utils import readable_delta

load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']

COMMUNAL = "Fellesvask"


def next_of_weekday(today, weekday):
    return today + datetime.timedelta((weekday - today.isoweekday()) % 7)


def timestamp_for_message(message_options):
    schedule_date = next_of_weekday(datetime.datetime.today(), message_options['weekday'])
    schedule_datetime = schedule_date.replace(**message_options['time'])
    return int(schedule_datetime.timestamp())


def get_random_fun_fact():
    return requests.get('https://uselessfacts.jsph.pl/random.json?language=en').json()['text']


def get_random_dad_joke():
    return requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'}).json()['joke']


def get_weeks_cleaners():
    current_week = int(datetime.datetime.today().strftime("%V"))
    with open('gamaslist.csv', mode='r') as file:
        for lines in csv.reader(file):
            if int(lines[0]) == current_week:
                if lines[1] == COMMUNAL:
                    return COMMUNAL
                return lines[1], lines[2]
    return None


def is_scheduled(message_options):
    timestamp = timestamp_for_message(message_options)
    res = requests.post(
        "https://slack.com/api/chat.scheduledMessages.list",
        headers={'Authorization': f'Bearer {BOT_TOKEN}'},
        json={
            "channel": CHANNEL_ID,
            "oldest": timestamp,
            "latest": timestamp
        }
    )
    if not (res.ok and res.json()['ok']):
        print(f"[FAILED] Could not check scheduled messages: {res.text}")
        return True  # pretend that message is already schedule to avoid message explosion...
    return len(res.json()['scheduled_messages']) > 0


def schedule_message(message_options):
    print(f"[INFO] Scheduling message:\n{message_options}")
    timestamp = timestamp_for_message(message_options)
    res = requests.post(
        "https://slack.com/api/chat.scheduleMessage",
        headers={'Authorization': f'Bearer {BOT_TOKEN}'},
        json={
            "channel": CHANNEL_ID,
            "text": message_options['text'],
            "post_at": timestamp
        })
    if not (res.ok and res.json()['ok']):
        print(f"[FAILED] Could not schedule message: {res.text}")
        return
    print(f"[INFO] Message scheduled successfully. Will be sent in {readable_delta(timestamp - int(time.time()))}.")


def schedule_reminders():
    cleaners = get_weeks_cleaners()
    print(f"[INFO] This weeks cleaners: {cleaners}")
    if cleaners is None:
        print("[FAILED] No cleaners found")
        return
    messages = [
        {
            'weekday': 5,
            'time': {
                'hour': 13, 'minute': 37, 'second': 0, 'microsecond': 0
            },
            'text': "⏲🧹\n" +
                    (
                        f"Ukens vaskere er <@{cleaners[0]}> og <@{cleaners[1]}>."
                        if cleaners != COMMUNAL else
                        "Denne uken er det fellesvask <!channel>!"
                    ) +
                    "\n\n"
                    f"> {get_random_fun_fact()}"
        },
        {
            'weekday': 7,
            'time': {
                'hour': 12, 'minute': 0, 'second': 0, 'microsecond': 0
            },
            'text': "🧹🧼✨\n" +
                    (
                        f"<@{cleaners[0]}> og <@{cleaners[1]}>, husk at dere er ukens beærede vaskere!"
                        if cleaners != COMMUNAL else
                        "Minner om fellesvask denne uken <!channel>!"
                    ) +
                    "\n\n"
                    f"> {get_random_dad_joke()}"
        }
    ]
    for m in messages:
        if is_scheduled(m):
            print("[WARNING] Message already scheduled, skipping.")
            continue
        schedule_message(m)


if __name__ == '__main__':
    schedule_reminders()

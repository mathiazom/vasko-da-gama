import os

import requests
import datetime
import csv
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ['CHANNEL_ID']

COMMUNAL = "Fellesvask"


def next_of_weekday(today, weekday):
    return today + datetime.timedelta((weekday - today.isoweekday()) % 7)


def datetime_from_schedule(schedule_options):
    return \
        next_of_weekday(datetime.datetime.today(), schedule_options['weekday']) \
            .replace(**schedule_options['time'])


def get_random_fun_fact():
    return requests.get('https://uselessfacts.jsph.pl/random.json?language=en').json()['text']


def get_random_dad_joke():
    return requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'}).json()['joke']


def get_weeks_cleaners():
    current_week = int(datetime.datetime.today().strftime("%V"))
    with open('gamaslist.csv', mode='r') as file:
        for lines in csv.reader(file):
            if lines[1] == COMMUNAL:
                return COMMUNAL
            if int(lines[0]) == current_week:
                return lines[1], lines[2]


def schedule_message(message_options):
    print(requests.post(
        "https://slack.com/api/chat.scheduleMessage",
        headers={'Authorization': f'Bearer {BOT_TOKEN}'},
        json={
            "channel": CHANNEL_ID,
            "text": message_options['text'],
            "post_at": int(datetime_from_schedule(message_options).timestamp())
        }).text)


cleaners = get_weeks_cleaners()
schedule_message({
    'weekday': 5,
    'time': {
        'hour': 13, 'minute': 37, 'second': 0, 'microsecond': 0
    },
    'text': "⏲🧹\n" +
            (
                f"Ukens vaskere er <@{cleaners[0]}> og <@{cleaners[1]}>.\n"
                if cleaners != COMMUNAL else
                "Denne uken er det fellesvask <!channel>!"
            ) +
            "\n\n"
            f"> {get_random_fun_fact()}"
})
schedule_message({
    'weekday': 7,
    'time': {
        'hour': 12, 'minute': 0, 'second': 0, 'microsecond': 0
    },
    'text': "🧹🧼✨\n" +
            (
                f"<@{cleaners[0]}> og <@{cleaners[1]}>, husk at dere er ukens beærede vaskere!\n"
                if cleaners != COMMUNAL else
                "Minner om fellesvask denne uken <!channel>!"
            ) +
            "\n\n"
            f"> {get_random_dad_joke()}"
})

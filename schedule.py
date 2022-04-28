import time

import requests

from main import timestamp_for_message_schedule, BOT_TOKEN, CHANNEL_ID, CHECKPOINTS_DIR
from utils import write_checkpoint_file, readable_delta


def is_scheduled(timestamp):
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
    timestamp = timestamp_for_message_schedule(message_options['schedule'])
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
    write_checkpoint_file(CHECKPOINTS_DIR)

import time

import requests

from utils import readable_delta, timestamp_for_message_schedule


def is_scheduled(token, channel, timestamp):
    res = requests.post(
        "https://slack.com/api/chat.scheduledMessages.list",
        headers={'Authorization': f'Bearer {token}'},
        json={
            "channel": channel,
            "oldest": timestamp,
            "latest": timestamp
        }
    )
    if not (res.ok and res.json()['ok']):
        print(f"[FAILED] Could not check scheduled messages: {res.text}")
        return True  # pretend that message is already schedule to avoid message explosion...
    return len(res.json()['scheduled_messages']) > 0


def schedule_message(token, channel, message_options):
    print(f"[INFO] Scheduling message:\n{message_options}")
    timestamp = timestamp_for_message_schedule(message_options['schedule'])
    res = requests.post(
        "https://slack.com/api/chat.scheduleMessage",
        headers={'Authorization': f'Bearer {token}'},
        json={
            "channel": channel,
            "text": message_options['text'],
            "attachments": message_options['attachments'],
            "post_at": timestamp
        })
    if not (res.ok and res.json()['ok']):
        print(f"[FAILED] Could not schedule message: {res.text}")
        return False
    print(f"[INFO] Message scheduled successfully. Will be sent in {readable_delta(timestamp - int(time.time()))}.")
    return True

from fun import get_random_fun_fact, get_random_dad_joke, get_non_existent_cat, get_real_cat
from main import COMMUNAL


def reminder_messages(cleaners):
    real_cat = get_real_cat()
    return [
        {
            'weekday': 5,
            'time': {
                'hour': 13, 'minute': 37, 'second': 0, 'microsecond': 0
            },
            'text': "⏲🧹\n" +
                    (
                        f"Ukas vaskere er <@{cleaners[0]}> og <@{cleaners[1]}>."
                        if cleaners != COMMUNAL else
                        "Denne uka er det fellesvask <!channel>!"
                    ),
            "attachments": [
                {
                    "fallback": "Ukas ikke-eksisterende katt",
                    "pretext": "Ukas ikke-eksisterende katt:",
                    "color": "#039BE5",
                    "image_url": get_non_existent_cat()
                }
            ]
        },
        {
            'weekday': 7,
            'time': {
                'hour': 12, 'minute': 0, 'second': 0, 'microsecond': 0
            },
            'text': "🧹🧼✨\n" +
                    (
                        f"<@{cleaners[0]}> og <@{cleaners[1]}>, husk at dere er ukas beærede vaskere!"
                        if cleaners != COMMUNAL else
                        "Minner om fellesvask denne uka <!channel>!"
                    ),
            "attachments": [
                {
                    "fallback": "Ukas organiske katt",
                    "pretext": "Ukas organiske katt:",
                    "color": "#2eb886",
                    "image_url": real_cat
                }
            ] if real_cat is not None else None
        }
    ]

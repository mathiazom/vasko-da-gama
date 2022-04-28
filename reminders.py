from fun import get_random_fun_fact, get_random_dad_joke
from main import COMMUNAL


def reminder_messages(cleaners):
    return [
        {
            'schedule': {
                'weekday': 5,
                'time': {
                    'hour': 13, 'minute': 37, 'second': 0, 'microsecond': 0
                }
            },
            'text': "⏲🧹\n" +
                    (
                        f"Ukas vaskere er <@{cleaners[0]}> og <@{cleaners[1]}>."
                        if cleaners != COMMUNAL else
                        "Denne uka er det fellesvask <!channel>!"
                    ) +
                    "\n\n"
                    f"> {get_random_fun_fact()}"
        },
        {
            'schedule': {
                'weekday': 7,
                'time': {
                    'hour': 12, 'minute': 0, 'second': 0, 'microsecond': 0
                }
            },
            'text': "🧹🧼✨\n" +
                    (
                        f"<@{cleaners[0]}> og <@{cleaners[1]}>, husk at dere er ukas beærede vaskere!"
                        if cleaners != COMMUNAL else
                        "Minner om fellesvask denne uka <!channel>!"
                    ) +
                    "\n\n"
                    f"> {get_random_dad_joke()}"
        }
    ]

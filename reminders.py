from fun import get_non_existent_cat, get_real_cat


def reminder_messages(cleaners, is_communal):
    real_cat = get_real_cat()
    return {
        'alpha': {
            'text': "⏲🧹\n" +
                    (
                        f"Ukas vaskere er <@{cleaners[0]}> og <@{cleaners[1]}>."
                        if not is_communal else
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
        'beta': {
            'text': "🧹🧼✨\n" +
                    (
                        f"<@{cleaners[0]}> og <@{cleaners[1]}>, husk at dere er ukas beærede vaskere!"
                        if not is_communal else
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
    }

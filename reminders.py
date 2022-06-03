from typing import Dict, Any, List, Optional

from fun import get_non_existent_cat, get_real_cat


def get_chores_messages(cleaners, is_communal, chores) -> Optional[List[str]]:
    if chores is None:
        return None
    if is_communal:
        return chores
    return [f"<@{cleaners[i]}>\n{chores[i]}" for i in [0, 1]]


def reminder_messages(cleaners, is_communal, chores) -> Dict[str, Any]:
    real_cat = get_real_cat()
    non_existent_cat = get_non_existent_cat()
    chores_messages = get_chores_messages(cleaners, is_communal, chores)
    return {
        'alpha': {
            'text': ":timer_clock::broom:\n" +
                    (
                        f"Ukas vaskere er <@{cleaners[0]}> og <@{cleaners[1]}>"
                        if not is_communal else
                        f"Denne uka er det fellesvask <!channel>!"
                    ) + ("\nOppgaver i :thread:" if chores_messages is not None else ""),
            "attachments": [
                {
                    "fallback": "Ukas ikke-eksisterende katt",
                    "pretext": "Ukas ikke-eksisterende katt:",
                    "color": "#039BE5",
                    "image_url": non_existent_cat
                }
            ] if non_existent_cat is not None else None,
            "chores": chores_messages
        },
        'beta': {
            'text': ":broom::soap::sparkles:\n" +
                    (
                        f"<@{cleaners[0]}> og <@{cleaners[1]}>, husk at dere er ukas beærede vaskere!"
                        if not is_communal else
                        "Minner om fellesvask denne uka <!channel>!"
                    ) + ("\nOppgaver i :thread:" if chores_messages is not None else ""),
            "attachments": [
                {
                    "fallback": "Ukas organiske katt",
                    "pretext": "Ukas organiske katt:",
                    "color": "#2eb886",
                    "image_url": real_cat
                }
            ] if real_cat is not None else None,
            "chores": chores_messages
        }
    }

from typing import Dict, Any, List, Optional

from fun import get_top_image_from_subreddit


def slack_user_list_string(users):
    if users is None or len(users) == 0:
        return None
    if len(users) == 1:
        return f"<@{users[0]}>"
    else:
        return f"{', '.join([f'<@{u}>' for u in users[:-1]])} og <@{users[-1]}>"


def get_chores_messages(cleaners, is_communal, chores) -> Optional[List[str]]:
    if chores is None:
        return None
    if is_communal:
        return chores.communal
    messages = [f"<@{cleaner}>\n{chores.pair[i]}" for i, cleaner in enumerate(cleaners[:2])]
    if "special" in chores:
        messages.append(f"<@{cleaners[2]}>\n{chores.special}")
    return messages


def reminder_messages(cleaners, is_communal, chores) -> Dict[str, Any]:
    alpha = {
        "image_url": get_top_image_from_subreddit("tuckedinkitties"),
        "pretext": "Ukas inntullede kattunge:",
        "fallback": "😺🛏️"
    }
    beta_image = get_top_image_from_subreddit("CatsOnPizza")
    if beta_image is not None:
        beta = {
            "image_url": beta_image,
            "pretext": "Ukas katt på pizza:",
            "fallback": "😺🍕"
        }
    else:
        # Fallback to supermodel
        beta = {
            "image_url": get_top_image_from_subreddit("SupermodelCats"),
            "pretext": "Ukas supermodell:",
            "fallback": "😺💫"
        }
    chores_messages = get_chores_messages(cleaners, is_communal, chores)
    return {
        'alpha': {
            'text': ":timer_clock::broom:\n" +
                    (
                        f"Ukas vaskere er {slack_user_list_string(cleaners)}"
                        if not is_communal else
                        f"Denne uka er det fellesvask <!channel>!"
                    ) + ("\nOppgaver i :thread:" if chores_messages is not None else ""),
            "attachments": [
                {
                    **alpha,
                    "color": "#039BE5"
                }
            ] if alpha["image_url"] is not None else None,
            "chores": chores_messages
        },
        'beta': {
            'text': ":broom::soap::sparkles:\n" +
                    (
                        f"{slack_user_list_string(cleaners)}, husk at dere er ukas beærede vaskere!"
                        if not is_communal else
                        "Minner om fellesvask denne uka <!channel>!"
                    ) + ("\nOppgaver i :thread:" if chores_messages is not None else ""),
            "attachments": [
                {
                    **beta,
                    "color": "#2eb886"
                }
            ] if beta["image_url"] is not None else None,
            "chores": chores_messages
        }
    }

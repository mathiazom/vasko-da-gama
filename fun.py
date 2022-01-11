import secrets

import requests

from main import TRANSFER_SH_URL, CAT_API_KEY


def get_random_fun_fact():
    return requests.get('https://uselessfacts.jsph.pl/random.json?language=en').json()['text']


def get_random_dad_joke():
    return requests.get('https://icanhazdadjoke.com/', headers={'Accept': 'application/json'}).json()['joke']


def upload_to_transfersh(byte_like):
    # Upload to self-hosted transfer.sh instance, and return upload url
    return requests.post(TRANSFER_SH_URL, files={secrets.token_hex(8): byte_like}).text


def get_non_existent_cat():
    image = requests.get("https://thiscatdoesnotexist.com/").content
    return upload_to_transfersh(image)


def get_real_cat():
    try:
        image_url = requests.get(
            url="https://api.thecatapi.com/v1/images/search",
            headers={"x-api-key": CAT_API_KEY}
        ).json()[0]['url']
    except:
        return None
    image = requests.get(image_url).content
    return upload_to_transfersh(image)

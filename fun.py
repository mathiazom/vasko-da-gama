import secrets

import requests

from config import Config
from definitions import APP_ROOT

config = Config.from_config_file(APP_ROOT / "config.yaml")


def upload_to_transfersh(url, byte_like):
    # Upload to self-hosted transfer.sh instance, and return upload url
    return requests.post(url, files={secrets.token_hex(8): byte_like}).text


def get_non_existent_cat():
    image = requests.get("https://thiscatdoesnotexist.com/").content
    return upload_to_transfersh(config.fun.transfersh_url, image)


def get_real_cat():
    try:
        image_url = requests.get(
            url="https://api.thecatapi.com/v1/images/search",
            headers={"x-api-key": config.fun.cat_api_key}
        ).json()[0]['url']
    except:
        return None
    image = requests.get(image_url).content
    return upload_to_transfersh(config.fun.transfersh_url, image)

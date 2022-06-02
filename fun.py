import secrets

import requests

from config import Config
from definitions import APP_ROOT

config = Config.from_config_file(APP_ROOT / "config.yaml")


def upload_to_transfersh(url, byte_like):
    # Upload to self-hosted transfer.sh instance, and return upload url
    res = requests.post(url, files={secrets.token_hex(8): byte_like})
    if not res.ok:
        print(f"[WARNING] Failed to upload file to transfer.sh instance at {url}")
        return None
    return res.text


def get_non_existent_cat():
    res = requests.get("https://thiscatdoesnotexist.com/")
    if not res.ok:
        print("[WARNING] Failed to retrieve non existent cat")
        return None
    return upload_to_transfersh(config.fun.transfersh_url, res.content)


def get_real_cat():
    try:
        image_url = requests.get(
            url="https://api.thecatapi.com/v1/images/search",
            headers={"x-api-key": config.fun.cat_api_key}
        ).json()[0]['url']
    except:
        print("[WARNING] Failed to retrieve real cat")
        return None
    return upload_to_transfersh(
        config.fun.transfersh_url,
        requests.get(image_url).content
    )

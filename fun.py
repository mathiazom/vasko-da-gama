import secrets
from typing import Optional

import requests

from config import Config
from definitions import APP_ROOT

config = Config.from_config_file(APP_ROOT / "config.yaml")


def upload_to_transfersh(url: str, filename: str, byte_like) -> Optional[str]:
    # Upload to self-hosted transfer.sh instance, and return upload url
    res = requests.post(url, files={filename: byte_like})
    if not res.ok:
        print(f"[WARNING] Failed to upload file to transfer.sh instance at {url}")
        return None
    return res.text


def get_non_existent_cat() -> Optional[str]:
    if config is None:
        print("[FAILED] Could not upload non existent cat, config missing.")
        return None
    if "fun" not in config:
        print("[FAILED] Could not upload non existent cat, fun config missing.")
        return None
    res = requests.get("https://thiscatdoesnotexist.com/")
    if not res.ok:
        print("[WARNING] Failed to retrieve non existent cat")
        return None
    return upload_to_transfersh(
        config.fun.transfersh_url,
        f"{secrets.token_hex(4)}.jpg",
        res.content
    )


def get_real_cat() -> Optional[str]:
    if config is None:
        print("[FAILED] Could not upload real cat, config missing.")
        return None
    if "fun" not in config:
        print("[FAILED] Could not upload real cat, fun config missing.")
        return None
    try:
        real_cat_res = requests.get(
            url="https://api.thecatapi.com/v1/images/search",
            headers={"x-api-key": config.fun.cat_api_key}
        )
    except:
        print("[WARNING] Failed to retrieve real cat")
        return None
    real_cat = real_cat_res.json()[0]
    real_cat_url = real_cat['url']
    real_cat_filename = real_cat_url.split("/")[-1]
    return upload_to_transfersh(
        config.fun.transfersh_url,
        real_cat_filename,
        requests.get(real_cat_url).content
    )

import json
import os

SETTINGS_FILE = "data/settings.json"


def load_settings():

    if not os.path.exists(SETTINGS_FILE):

        os.makedirs("data", exist_ok=True)

        default = {
            "last_quotation": 1,
            "business": {
                "name": "",
                "address": "",
                "phone": "",
                "gst": "",
                "logo": ""
            }
        }

        with open(SETTINGS_FILE, "w") as f:
            json.dump(default, f, indent=4)

        return default

    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(settings):

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


def get_next_quotation():

    settings = load_settings()

    number = settings["last_quotation"]

    settings["last_quotation"] += 1

    save_settings(settings)

    return f"QT-{number:04d}"
def get_business():

    settings = load_settings()

    return settings.get(
        "business",
        {
            "name": "",
            "address": "",
            "phone": "",
            "gst": ""
        }
    )


def save_business(name, address, phone, gst, logo):

    settings = load_settings()

    settings["business"] = {
        "name": name,
        "address": address,
        "phone": phone,
        "gst": gst,
        "logo": logo
    }

    save_settings(settings)
def get_logo_path():

    settings = load_settings()

    return settings.get("logo_path", "")


def save_logo_path(path):

    settings = load_settings()

    settings["logo_path"] = path

    save_settings(settings)    
import sys
from pathlib import Path

import yaml


def get_arg(key):
    for i in sys.argv:
        if i.split(":", maxsplit=1)[0] == key:
            return i.split(":", maxsplit=1)[1]
    return None


if get_arg("url") is None:
    raise Exception("'url' argument is missing. Example: 'url:https://www.google.com'")

path = Path(__file__).parent / "setup.yml"
with path.open() as f:  # Loads yaml config file to be referenced elsewhere in env_setup.py
    yml_config = yaml.load(f, Loader=yaml.FullLoader)


class EnvironmentSetup:
    _instance = None
    base_url = get_arg("url")
    login_username = get_arg("username")
    login_password = get_arg("password")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EnvironmentSetup, cls).__new__(cls)

        return cls._instance

    def __init__(self):
        if self.base_url[-1] != "/":
            self.base_url = self.base_url + "/"

    def get_base_url(self):
        return self.base_url


class Browser:
    path_root = None

    def __init__(self, playwright):
        self.playwright = playwright
        self.browser_type = None
        self.context = None

        if get_arg("headless") == "n":
            self.headless = False
        else:
            self.headless = True

        if get_arg("browser").lower() == ("firefox" and "ff"):
            self.browser_type = self.playwright.firefox.launch(headless=self.headless)
        elif get_arg("browser").lower() == ("chrome" and "cr"):
            self.browser_type = self.playwright.chromium.launch(headless=self.headless)
        else:
            self.browser_type = self.playwright.webkit.launch(headless=self.headless)

    def start(self):
        try:
            self.context = self.browser_type.new_context(
                storage_state=f"{Browser.path_root}/state.json",
                viewport={"width": 1920, "height": 1080},
            )
        except FileNotFoundError:
            self.context = self.browser_type.new_context(
                viewport={"width": 1920, "height": 1080},
            )
        self.context.set_default_timeout(5000)
        self.context.set_default_navigation_timeout(30000)
        return self.context

    def stop(self):
        self.context.close()

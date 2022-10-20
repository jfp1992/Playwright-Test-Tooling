""" Allows for more readable logging of key steps during execution """
import logging
import os
import time
from datetime import datetime

from colorama import Fore, Style

from base.env_setup import get_arg


def log_new_date_time():
    """Gets a new date and time
    :return: The date time"""
    current_date_time = datetime.now()
    date_time = current_date_time.strftime("%d_%m_%Y %H_%M_%S")  # Get current date and format date time
    return date_time


class StepCounter:
    date_time = log_new_date_time()
    test_title = "UndefinedTestTitle"
    path_root = None

    def log_result(self, text):
        with open(os.path.join(StepCounter.path_root, f"results_{self.date_time}.txt"), "a") as file:
            file.write(f"{text}\n")

    def reset(self, expected, actual):
        raise Exception(f"{expected}\n\n{actual}")


def xlogging(set_debug_level, text_out, log_as_step="n", sleep_secs=0, frame_stack=1):
    """This allows a specific wait time to be passed when sending a message to the console
    :param log_as_step: default is 'n', use count_step='y' if log should also be counted as a step to be logged to steps file
    :param set_debug_level: 1:DEBUG, 2:INFO, 3:, WARNING, 4:ERROR, 5:CRITICAL
    :param text_out: Message to be printed to the console
    :param sleep_secs: How long to wait before continuing with the program
    :param frame_stack: Set to true if the file calling this function == locators.py
    :return: Void"""

    if set_debug_level == 1:
        debug_level = logging.debug
        log_level = "Debug: "
        color = Fore.WHITE
    elif set_debug_level == 2:
        debug_level = logging.info
        log_level = "Info: "
        color = Fore.LIGHTGREEN_EX
    elif set_debug_level == 3:
        debug_level = logging.warning
        log_level = "Warn: "
        color = Fore.YELLOW
    elif set_debug_level == 4:
        debug_level = logging.error
        log_level = "Error: "
        color = Fore.LIGHTRED_EX
    elif set_debug_level == 5:
        debug_level = logging.critical
        log_level = "CRITICAL: "
        color = Fore.RED
    else:
        debug_level = 2
        log_level = ""
        color = Fore.WHITE

    if log_as_step == "n":
        if sleep_secs != 0:
            if get_arg("colors") == "y":
                debug_level(f"{color}{log_level} {text_out}; wait duration: {sleep_secs} second(s){Style.RESET_ALL}")
            else:
                debug_level(f"{log_level} {text_out}; wait duration: {sleep_secs} second(s)")
        else:
            if get_arg("colors") == "y":
                debug_level(f"{color}{log_level} {text_out}{Style.RESET_ALL}")
            else:
                debug_level(f"{log_level} {text_out}")
        time.sleep(sleep_secs)

    if log_as_step == "y":
        if sleep_secs != 0:
            if get_arg("colors") == "y":
                debug_level(f"{Fore.LIGHTCYAN_EX}{log_level} {text_out}; wait duration: {sleep_secs} second(s){Style.RESET_ALL}")
            else:
                debug_level(f"{log_level} {text_out}; wait duration: {sleep_secs} second(s)")
        else:
            if get_arg("colors") == "y":
                debug_level(f"{Fore.LIGHTCYAN_EX}{log_level} {text_out}{Style.RESET_ALL}")
            else:
                debug_level(f"{log_level} {text_out}")
        time.sleep(sleep_secs)

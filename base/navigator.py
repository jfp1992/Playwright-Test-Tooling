from base.custom_logging import xlogging
from base.env_setup import EnvironmentSetup
from base.lang_code import LangCode
from base.record_time import RecordTime


class Navigator:
    cookie_close = False
    excellent_responses = 0
    good_responses = 0
    ok_responses = 0
    poor_responses = 0
    bad_responses = 0
    critical_responses = 0

    def __init__(self, page, url_ext="", trigger_element=None, module="undefined", load_check_element=None):
        """
        :param url_ext: Used for 'go_to_url' - url to navigate to. If not using go_to_url then it is recommended to set this to ''
        to avoid having to set default params
        Example format: 'member/login'
        :param module: Used for 'navigate_to_url' - String identifier for navigating, for example: clicking save button for bricky
        :param trigger_element: Pass an element to trigger navigation action Example: web_wait(save button).click - Exclude ending parenthesis: ()
        :param load_check_element: Pass an element to check for page load this will be used as the stop time for the time recorder"""
        self.page = page
        self.url_ext = url_ext
        self.module = module
        self.trigger_element = trigger_element
        self.load_check_element = load_check_element
        self.dom_before_load = ""

        if self.load_check_element is None:
            self.load_check_element = lambda: self.page.self.page.locator("#toolbar-item-administration-tray").wait_for(
                state="visible"
            )

    def go_to_url(self):
        url_load = RecordTime(f"going to url {EnvironmentSetup().get_base_url() + LangCode.language_code + self.url_ext}")
        url_load.start()

        self.page.goto(EnvironmentSetup().get_base_url() + LangCode.language_code + self.url_ext)

        self.page.wait_for_load_state(state="networkidle")
        self.page.wait_for_load_state(state="domcontentloaded")

        xlogging(2, url_load.stop()[1], frame_stack=2)
        self.load_timer(url_load)

    def navigate(self):
        if self.module != "undefined" and self.trigger_element is not None:
            navigation = RecordTime(self.module)
            navigation.start()

            self.trigger_element()

            self.page.wait_for_load_state(state="networkidle")
            self.page.wait_for_load_state(state="domcontentloaded")

            xlogging(2, navigation.stop()[1], frame_stack=2)
            self.load_timer(navigation)

        else:
            if self.module == "undefined":
                raise ValueError("No module name to pass to Navigator.navigate")
            if self.trigger_element is None:
                raise ValueError("No trigger_element to pass to Navigator.navigate")
            if self.load_check_element is None:
                raise ValueError("No load_check_element to pass to Navigator.navigate")

    def load_timer(self, timer):
        """Checks time taken for a RecordTime object and categorises time taken then increases the counter for that bracket
        :param timer: RecordTime object, for example: if you have "stop_watch = RecordTime" then 'stop_watch' would be passed
        """
        if timer.stop()[0] <= 2:
            xlogging(2, f"Excellent response time: Page load took {timer.stop()[0]} seconds")
            Navigator.excellent_responses += 1
        elif 2 < timer.stop()[0] <= 5:
            xlogging(2, f"Good response time: Page load took {timer.stop()[0]} seconds")
            Navigator.good_responses = Navigator.good_responses + 1
        elif 5 < timer.stop()[0] <= 10:
            xlogging(2, f"Ok response time: Page load took {timer.stop()[0]} seconds")
            Navigator.ok_responses += 1
        elif 10 < timer.stop()[0] <= 20:
            xlogging(3, f"Poor response time: Page load took {timer.stop()[0]} seconds")
            Navigator.poor_responses += 1
        elif 20 < timer.stop()[0] <= 30:
            xlogging(4, f"Bad response time: Page load took {timer.stop()[0]} seconds")
            Navigator.bad_responses += 1
        elif timer.stop()[0] > 30:
            xlogging(5, f"Critical response time, test may fail: Page load took {timer.stop()[0]} seconds")
            Navigator.critical_responses += 1

    def response_stats(self):
        return (
            f"\nResponse statistics for run:\n"
            f"\t- Excellent: {Navigator.excellent_responses} (0-2s)\n"
            f"\t- Good-----: {Navigator.good_responses} (2-5s)\n"
            f"\t- Ok-------: {Navigator.ok_responses} (5-10s)\n"
            f"\t- Poor-----: {Navigator.poor_responses} (10-20s)\n"
            f"\t- Bad------: {Navigator.bad_responses} (20-30s)\n"
            f"\t- Critical-: {Navigator.critical_responses} (30s+)\n"
        )

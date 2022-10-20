import random
import time
from datetime import datetime

from playwright.sync_api import expect

from base.custom_logging import xlogging
from base.locators import Css
from base.record_time import RecordTime


class Tools:
    def __init__(self, page, context):
        self.page = page
        self.context = context

    def hover_element(self, hover_xpath, element_to_appear_xpath, index=0):
        """Hovers reliably on an element until the target element appears
        :param index: nth element to hover, 0 = first element
        :param hover_xpath: Hover target xpath
        :param element_to_appear_xpath: Elements xpath to appear when hovering
        :param refresh_on_failure: If unable to find the element_to_appear the page will be refresh and hover will be retried"""
        element_to_hover = self.page.locator(hover_xpath)

        element_to_appear = self.page.locator(element_to_appear_xpath)

        self.page.wait_for_load_state(state="networkidle")

        xlogging(2, f"Hovering '{hover_xpath}'", "y")
        element_to_hover.nth(index).hover()

        element_to_appear.first.wait_for(state="visible")

    def drag_and_drop(self, drag_from_element, drag_to_element, hold_delay=0, release_delay=0):
        drag_from_element.hover()
        self.page.mouse.down()
        drag_from_element.hover()
        time.sleep(hold_delay)

        drag_to_element.hover()
        time.sleep(release_delay)
        drag_to_element.hover()
        self.page.mouse.up()

    def get_elements(self, locator):
        combo_values = self.page.locator(locator)
        count = combo_values.count()

        elements = []

        for i in range(count):
            elements.append(self.page.locator(locator).nth(i))

        return elements

    def go_forward(self):
        current_url = self.page.url
        xlogging(2, f"Going forward a page", "y", frame_stack=2)
        self.page.go_forward()
        if current_url == self.page.url:
            xlogging(3, f"User remains on the same page after attempting to navigate forward", "y")

    def go_back(self):
        current_url = self.page.url
        xlogging(2, f"Going back a page", "y", frame_stack=2)
        self.page.go_back()
        if current_url == self.page.url:
            xlogging(3, f"User remains on the same page after attempting to navigate back", "y")

    def refresh(self):
        xlogging(2, f"Reloading page", "y")
        self.page.reload()

    def clear_cookies(self, context):
        xlogging(2, f"Clearing cookies", "y", frame_stack=2)
        context.delete_all_cookies()

    def new_date_time(self):
        current_date_time = datetime.now()
        date_time = "AUTO: " + current_date_time.strftime("%d/%m/%Y %H_%M_%S")  # Get current date and format date time
        return date_time

    def random_hex_color(self, selector_value):
        """Generates random hex value for colors example: '#ffffff', '#1D4ADD'
        :param selector_value: A string to pass into an xpath query to send keys to an input tag with a attribute of 'data-drupal-selector'
        :return: void"""
        import random

        r = lambda: random.randint(0, 255)
        color = "#{:02x}{:02x}{:02x}".format(r(), r(), r())
        self.page.locator(Css("input", "data-drupal-selector", selector_value).contains()).fill(color)

    def random_int(self, num1, num2):
        try:
            return random.randint(num1, num2)
        except ValueError:
            raise Exception("Bad value passed into num1 or num2 for random_int function")

    def random_float(self, num1, num2):
        return random.uniform(num1, num2)

    def wait_for_jquery_to_finish(self, timeout=30):
        timeout = timeout * 1000
        jquery_timer = RecordTime("jQuery")
        jquery_timer.start()
        self.page.wait_for_function(str(self.page.evaluate("jQuery.active == 0")).lower(), timeout=timeout)
        xlogging(2, jquery_timer.stop()[1], "y", frame_stack=2)

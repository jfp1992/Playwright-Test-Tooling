import os

import traceback

from base.custom_logging import StepCounter
from base.env_setup import Browser, get_arg
from base.runner import TestRunner


class TestBase:
    test_count = 10
    start_context = True

    context = None
    page = None

    def __init__(self):
        if TestBase.start_context:
            playwright = TestRunner.playwright
            TestBase.context = Browser(playwright, StepCounter.test_title).start()
            TestBase.page = TestBase.context.new_page()
            TestBase.start_context = False

        self.page = TestBase.page
        self.context = TestBase.context

    def setup(self):
        """Placeholder: Not all tests require a setup"""
        pass

    def test(self):
        raise NotImplementedError

    def teardown(self):
        """Placeholder: Not all tests require a teardown"""
        pass

    def run(self) -> None:
        try:
            self.page.goto("about:blank")
            self.context.tracing.start(title=StepCounter.test_title, sources=True, screenshots=True, snapshots=True)
        except:
            self.page = self.context.new_page()
            self.context.tracing.start(title=StepCounter.test_title, sources=True, screenshots=True, snapshots=True)
            self.page.goto("about:blank")
        try:
            self.setup()
            self.test()
            self.teardown()
        except Exception as e:
            traceback_formatted = traceback.format_exc()
            if get_arg("headless") == "n":
                traceback.print_exc()
                self.page.pause()
            self.page.evaluate(f"console.error(String.raw`{traceback_formatted}`)")
            self.context.tracing.stop(path=os.path.join(StepCounter.path_root, "traces", f"trace_{StepCounter.test_title}.zip"))
            if TestBase.test_count % 10 == 0:
                self.context.close()
                TestBase.start_context = True
            TestBase.test_count += 1
            self.page.close()
            raise e
        TestBase.page = TestBase.context.new_page()
        self.context.tracing.stop(path=os.path.join(StepCounter.path_root, "traces", f"ignore.zip"))
        if TestBase.test_count % 10 == 0:
            self.context.close()
            TestBase.start_context = True
        TestBase.test_count += 1
        self.page.close()

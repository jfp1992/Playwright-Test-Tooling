""" Executes all tests found within a glob search list passed by main.py
"""
import glob
import os
import platform
import traceback

from base.custom_logging import StepCounter, xlogging
from base.record_time import RecordTime


class TestRunner:
    playwright = None

    def __init__(self, test_fuzzy_paths, path_root, playwright):
        """Sets up the lists of tests to be iterated through for execution
        :param test_fuzzy_paths: List of paths (can be fuzzy)"""
        TestRunner.playwright = playwright
        self.path_breakdown = "Undefined test title or simplified path"

        self.tests = []
        self.test_fuzzy_paths = test_fuzzy_paths
        self.path_root = path_root

        xlogging(2, f"For each fuzzy path:")
        for test_fuzzy_path in test_fuzzy_paths:
            xlogging(2, test_fuzzy_path)
        xlogging(2, f"Getting the glob list and setting the self.test list with itself concatenated with the glob list")

        for test_path in test_fuzzy_paths:
            self.tests = self.tests + glob.glob(os.path.join(self.path_root, "test_suites") + "/" + test_path)

        self.tests.sort()

        for test_path in self.tests:
            xlogging(2, test_path)

        self.tests_passed = 0
        self.tests_failed = 0

        self.pic_path_temp = os.path.join(self.path_root, "temp").replace("/base", "").replace("\\base", "")
        self.vid_path = os.path.join(self.path_root, "video").replace("/base", "").replace("\\base", "")

        xlogging(2, f"Found {len(self.tests)} tests", "y")

    def image_cleanup(self):
        """Gets the list of png images in the images folder and removes them."""
        files = glob.glob(f"{self.pic_path_temp}/*.png")
        for f in files:
            os.remove(f)

    def get_test_title(self, path):
        prtsc_filename = path
        self.path_breakdown = []

        prtsc_filename = prtsc_filename.replace(".py", "")

        if platform.system() == "Windows":
            for file_path_section in prtsc_filename.split("\\"):
                self.path_breakdown.append(file_path_section)
        else:
            for file_path_section in prtsc_filename.split("/"):
                self.path_breakdown.append(file_path_section)

    @staticmethod
    def exec_file(filepath, globals=None, locals=None):
        """Executes the filepath passed"""
        if globals is None:
            globals = {}
        globals.update(
            {
                "__file__": filepath,
                "__name__": "__main__",
            }
        )
        with open(filepath, "rb") as file:
            exec(compile(file.read(), filepath, "exec"), globals, locals)

    def run(self):
        """Iterates through the combined list of tests found and runs each one.
        By default the pass_state is False unless file execution is successful then this flag is set to True"""
        all_tests = RecordTime("\nAll tests")
        all_tests.start()
        for test in self.tests:
            self.image_cleanup()
            self.get_test_title(test)

            StepCounter.test_title = f"{self.path_breakdown[-2]}_{self.path_breakdown[-1]}"
            current_test = RecordTime(f"{self.path_breakdown[-2]}_{self.path_breakdown[-1]}")

            current_test.start()
            pass_state = False
            record = False
            if not pass_state:
                try:
                    if not record:
                        StepCounter.record_step_images = False
                    else:
                        StepCounter.record_step_images = True
                    xlogging(2, f"running test {test}")
                    self.exec_file(test)

                    pass_state = True

                    self.tests_passed += 1

                    xlogging(2, f"Total passed: {self.tests_passed} out of {len(self.tests)} tests")

                    self.image_cleanup()
                    continue

                except Exception:
                    traceback.print_exc()
                    xlogging(2, f"FAILURE: {self.path_breakdown[-2]}_{self.path_breakdown[-1]}")

            if not pass_state:
                self.tests_failed += 1

        xlogging(2, f"Total passed: {self.tests_passed} out of {len(self.tests)} tests")
        xlogging(2, f"Total failed: {self.tests_failed} out of {len(self.tests)} tests")

        if self.tests_failed != 0:
            xlogging(4, f"Run failed with {self.tests_failed} out of {len(self.tests)} tests failing")
            # xlogging(2, Navigator.response_stats()) TODO: refactor this - maybe do it better?
            return ["fail", f"Run failed with {self.tests_failed} out of {len(self.tests)} tests failing"]
        else:
            xlogging(2, f"Run finished with {self.tests_passed} out of {len(self.tests)} tests passing")
            # xlogging(2, Navigator.response_stats()) TODO: refactor this - maybe do it better?
            return ["pass", f"Run finished with {self.tests_passed} out of {len(self.tests)} tests passing"]

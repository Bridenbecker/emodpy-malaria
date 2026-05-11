import os
import sys
import time
import unittest
from pathlib import Path

from emodpy.emod_task import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))
import manifest
import helpers


class BaseSimTest(unittest.TestCase):

    def setUp(self) -> None:
        self.original_working_dir = os.getcwd()
        self.case_name = self._testMethodName
        print(f"\n{self.case_name}")
        helpers.create_failed_tests_folder()
        self.test_folder = os.path.join(manifest.failed_tests, self.case_name)
        if os.path.exists(self.test_folder):
            helpers.delete_existing_folder(self.test_folder)
        os.mkdir(self.test_folder)
        os.chdir(self.test_folder)

    def tearDown(self) -> None:
        helpers.close_idmtools_logger(logger.parent)
        if os.name == "nt":
            time.sleep(1)
        os.chdir(self.original_working_dir)

        test_failed = False
        try:
            if hasattr(self._outcome, 'errors'):
                test_failed = any(error[1] for error in self._outcome.errors)
            elif hasattr(self._outcome, 'result'):
                result = self._outcome.result
                if hasattr(result, 'errors') and hasattr(result, 'failures'):
                    test_failed = len(result.errors) > 0 or len(result.failures) > 0
        except (AttributeError, TypeError):
            test_failed = False

        helpers.delete_existing_folder(self.test_folder, must_be_empty=test_failed)

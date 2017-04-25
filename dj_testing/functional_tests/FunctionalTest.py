import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException

DEFAULT_WAIT = 5


class FunctionalTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(DEFAULT_WAIT)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()

    def wait_for(self, function_with_assertion, timeout=DEFAULT_WAIT):
        start_time = time.time()
        while (time.time() - start_time) < timeout:
            try:
                return function_with_assertion()
            except(AssertionError, WebDriverException, NoSuchElementException):
                time.sleep(0.1)
        return function_with_assertion()

    def get_item_input_box(self):
        return self.browser.find_element_by_id('input-search')

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def check_for_row_in_list_table(self, row_text, table_id):
        table = self.browser.find_element_by_id(table_id)
        rows = table.find_element_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
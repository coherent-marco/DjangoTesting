from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import TestCase

# Create your tests here.
from selenium import webdriver


DEFAULT_WAIT = 5


class ProductSearchTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(DEFAULT_WAIT)

    def tearDown(self):
        self.browser.refresh()
        self.browser.quit()
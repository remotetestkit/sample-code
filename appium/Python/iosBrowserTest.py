import os
import sys
import unittest

from time import sleep
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.options.common import AppiumOptions
import warnings

# get userName, password from Environment variable
RTK_USERNAME = os.environ.get('RTK_USERNAME')
RTK_PASSWORD = os.environ.get('RTK_PASSWORD')
if not RTK_USERNAME or not RTK_PASSWORD:
    print("Environment variable error")
    sys.exit()


class OpenUrlTest(unittest.TestCase):
    def setUp(self):
        caps = {
            'userName': RTK_USERNAME,
            'password': RTK_PASSWORD,
            'logLevel': 'info',
            'platformName': 'iOS',
            'deviceName': 'iPhone',
            'platformVersion': '18',
            'browserName': 'Safari',
            'automationName': 'XCUITest'
        }
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        options = AppiumOptions()
        for k in caps:
            options.set_capability(k, caps[k])
        self.driver = webdriver.Remote(
            "https://gwjp.appkitbox.com/wd/hub", options=options
        )
        print(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_google_search(self):
        # Open URL
        url = "https://www.google.com/"
        print("Open URL: " + url)
        self.driver.get(url)
        element = self.driver.find_element(By.CSS_SELECTOR, 'textarea')
        sleep(5)
        self.driver.save_screenshot('capture_01.png')

        # Input keys
        word = "Remote testKit"
        print("Input Keys: " + word)
        element.send_keys(word)
        element.submit
        sleep(5)
        self.driver.save_screenshot('capture_02.png')

        # Get value
        value = self.driver.find_element(By.CSS_SELECTOR, 'textarea').get_attribute('value')
        print("Text field value=" + value)
        self.assertEqual(value, "Remote testKit")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(OpenUrlTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

import os
import sys
import unittest

from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
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
            'deviceName': 'Nexus 5',
            'platformName': 'Android',
            'browserName': 'Chrome',
            'appiumVersion': '1.22.3',
            'chromeOptions': {'w3c': False}
        }
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        self.driver = webdriver.Remote('https://gwjp.appkitbox.com/wd/hub', caps)
        print(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_google_search(self):
        print(self.driver.capabilities['snapshotUrl'])
        # Open URL
        url = "https://www.google.com/"
        print("Open URL: " + url)
        self.driver.get(url)
        element = self.driver.find_element(By.NAME, 'q')
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
        value = self.driver.find_element(By.NAME, 'q').get_attribute('value')
        print("Text field value=" + value)
        self.assertEqual(value, "Remote testKit")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(OpenUrlTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

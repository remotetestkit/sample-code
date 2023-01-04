import os
import sys
import unittest

from time import sleep
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
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
            'deviceName': 'iPhone 7.*',
            'platformVersion': '12',
            'bundleId': 'com.apple.calculator'
        }
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        self.driver = webdriver.Remote('https://gwjp.appkitbox.com/wd/hub', caps)
        print(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_calculator(self):
        print(self.driver.capabilities['snapshotUrl'])

        driver = self.driver
        self.driver.save_screenshot('capture_01.png')

        el1 = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "1")
        el1.click()
        self.driver.save_screenshot('capture_02.png')

        is_lang_english = True
        try:
            el2 = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "multiply")
            el2.click()
        except Exception:
            is_lang_english = False
            el2 = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "乗算")
            el2.click()
        self.driver.save_screenshot('capture_03.png')

        el3 = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "3")
        el3.click()
        self.driver.save_screenshot('capture_04.png')

        el2.click()
        self.driver.save_screenshot('capture_05.png')

        el3.click()
        self.driver.save_screenshot('capture_06.png')

        if is_lang_english:
            el4 = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "equals")
            el4.click()
            self.driver.save_screenshot('capture_07.png')

            el5 = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "Result")
            value = el5.get_attribute('value')

            print("Text field value=" + value)
            self.assertEqual(value, "9")

            el6 = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "clear")
            el6.click()
            self.driver.save_screenshot('capture_08.png')
        else:
            el4 = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "計算実行")
            el4.click()
            self.driver.save_screenshot('capture_07.png')

            el5 = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "結果")
            value = el5.get_attribute('value')

            print("Text field value=" + value)
            self.assertEqual(value, "9")

            el6 = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "消去")
            el6.click()
            self.driver.save_screenshot('capture_07.png')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(OpenUrlTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

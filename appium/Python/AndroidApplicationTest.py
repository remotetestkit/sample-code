import os
import sys
import unittest

from time import sleep
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

# get userName, password from Environment variable
RTK_USERNAME = os.environ.get('RTK_USERNAME')
RTK_PASSWORD = os.environ.get('RTK_PASSWORD')
if not RTK_USERNAME or not RTK_PASSWORD:
    print("Environment variable error")
    sys.exit()


class ContactsAndroidTests(unittest.TestCase):
    def setUp(self):
        caps = {
            'userName': RTK_USERNAME,
            'password': RTK_PASSWORD,
            'deviceName': 'Nexus 5',
            'platformName': 'Android',
            'unicodeKeyboard': 'true',
            'resetKeyboard': 'true',
            'appiumVersion': '1.15.1',
            # set application from RemoteTestKit storage
            # 'app': 'RTKdemo.apk',
            # set application from HTTP Url
            'app': 'https://github.com/remotetestkit/sample-code/raw/master/appium/apk/RTKdemo.apk',
            'appPackage': 'com.example.remotetestkit.demo',
            'appActivity': 'MainActivity'
        }
        self.driver = webdriver.Remote('https://gwjp.appkitbox.com/wd/hub', caps)
        print(self.driver)

    def tearDown(self):
        self.driver.quit()

    def test_add_contacts(self):
        print(self.driver.capabilities['snapshotUrl'])
        self.driver.save_screenshot('capture_01.png')

        # get text fields and set text in it
        textfields = self.driver.find_elements(By.CLASS_NAME, "android.widget.EditText")
        textfields[0].send_keys("RTK")
        textfields[1].send_keys("Remote TestKing")
        self.driver.save_screenshot('capture_02.png')

        # click Save button
        element = self.driver.find_element(By.ID, "com.example.remotetestkit.demo:id/Save")
        element.click()

        # set text from Login display
        result = self.driver.find_element(By.ID, 'com.example.remotetestkit.demo:id/title4')
        print("Login Result : " + result.text)
        self.assertEqual('Password Error', result.text)
        self.driver.save_screenshot('capture_03.png')

        # press return key
        self.driver.press_keycode(4)

        # delete and set text to text fields
        textfields[1].clear()
        textfields[1].send_keys('Remote TestKit')
        self.driver.save_screenshot('capture_04.png')

        # click Save button
        element.click()

        # get text from Login display
        result = self.driver.find_element(By.ID, 'com.example.remotetestkit.demo:id/title2')
        print("Login Result : " + result.text)
        self.assertEqual('Logged in', result.text)
        self.driver.save_screenshot('capture_05.png')


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(ContactsAndroidTests)
    unittest.TextTestRunner(verbosity=2).run(suite)

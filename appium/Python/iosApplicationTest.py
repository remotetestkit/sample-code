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
            'platformVersion': '14',
            "app": "https://github.com/remotetestkit/sample-code/raw/master/appium/apk/RTKappium.ipa",
            "bundleId": "com.example.remotetestkit.demo",
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

    def test_application(self):
        self.driver.save_screenshot("app_cap001.png")

        # 「ID」と「間違ったパスワード」をテキストフィールドに入力
        textfields = self.driver.find_elements(By.XPATH, "//XCUIElementTypeTextField")
        textfields[0].send_keys("RTK")
        textfields[1].send_keys("Remote TestKing")
        sleep(3)
        self.driver.save_screenshot("app_cap002.png")

        # Saveボタン押下
        savebutton = self.driver.find_element(By.XPATH, "//XCUIElementTypeButton[@name='Save']")
        savebutton.click()
        sleep(3)

        # 表示されたメッセージを取得
        self.driver.save_screenshot("app_cap003.png")
        result = self.driver.find_elements(By.XPATH, "//XCUIElementTypeStaticText")[-1]
        print("Login Result : " + result.text)
        self.assertEqual("Password Error", result.text)

        # 戻るボタンを押してトップ画面に戻る
        backbutton = self.driver.find_element(By.XPATH, "//XCUIElementTypeButton[@name='Back']")
        backbutton.click()
        sleep(3)

        # 「正しいパスワード」を入力
        textfields[1].clear()
        textfields[1].send_keys("Remote TestKit")
        sleep(3)

        self.driver.save_screenshot("app_cap004.png")

        # Saveボタン押下
        savebutton = self.driver.find_element(By.XPATH, "//XCUIElementTypeButton[@name='Save']")
        savebutton.click()
        sleep(3)

        # 表示されたメッセージを取得
        result = self.driver.find_elements(By.XPATH, "//XCUIElementTypeStaticText")[-1]
        try:
            result.text
        except AttributeError:
            self.driver.save_screenshot("app_cap005_error.png")

        self.driver.save_screenshot("app_cap005.png")
        print("Login Result : " + result.text)
        self.assertEqual("Logged in", result.text)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(OpenUrlTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

import os
import sys
import unittest

from time import sleep
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.options.common import AppiumOptions

import warnings

# get userName, password from Environment variable
RTK_USERNAME = os.environ.get("RTK_USERNAME")
RTK_PASSWORD = os.environ.get("RTK_PASSWORD")
if not RTK_USERNAME or not RTK_PASSWORD:
    print("Environment variable error")
    sys.exit()


class WebviewAppTest(unittest.TestCase):
    def setUp(self):
        caps = {
            "userName": RTK_USERNAME,
            "password": RTK_PASSWORD,
            "deviceName": "iPhone 12",
            "platformName": "iOS",
            "appiumVersion": "2.1.3",
            "automationName": "XCUITest",
            "newCommandTimeout": "180",
            "app": "https://github.com/remotetestkit/sample-code/raw/master/appium/apk/RTKappium_webview.ipa",
            "bundleId": "com.example.remotetestkit.webviewdemo",
            "webviewConnectTimeout": 5000,
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
        if self.driver:
            self.driver.quit()

    def switchContext(self, name):
        ctxs = self.driver.contexts
        print(ctxs)
        for ctx in ctxs:
            if ctx.find(name) != -1:
                print("found context name : " + ctx)
                self.driver.switch_to.context(ctx)
                return
        print("The specified context was not found.")
        sys.exit()

    def test_webview(self):
        self.driver.save_screenshot("capture_01.png")

        # URL入力
        nEdittext = self.driver.find_element(By.XPATH, "//XCUIElementTypeTextField")
        nEdittext.clear()
        nEdittext.send_keys("https://nr--test.web.app/webviewapp/")
        self.driver.save_screenshot("capture_02.png")

        # ログインボタン押下
        nLoginButton = self.driver.find_element(
            By.XPATH, "//XCUIElementTypeButton[@name='Login']"
        )
        nLoginButton.click()
        sleep(5)
        self.driver.save_screenshot("capture_03.png")

        # コンテキストをWebviewへ切り替え
        self.switchContext("WEBVIEW")

        # Webのログイン画面
        wInputs = self.driver.find_elements(By.CSS_SELECTOR, "input")
        wInputs[0].send_keys("RTK")
        wInputs[1].send_keys("Remote Testking")
        self.driver.save_screenshot("capture_04.png")
        wSubmitButton = self.driver.find_element(By.CSS_SELECTOR, "button")
        wSubmitButton.click()
        sleep(3)

        # Webの結果画面
        self.driver.save_screenshot("capture_05.png")
        wH2 = self.driver.find_element(By.CSS_SELECTOR, "h2")
        resultText = wH2.text
        print("Text field value=" + resultText)

        # 前の画面に戻る
        wBackText = self.driver.find_element(By.CSS_SELECTOR, "a")
        wBackText.click()
        sleep(3)

        # 正しいパスワードを入力
        wInputs = self.driver.find_elements(By.CSS_SELECTOR, "input")
        wInputs[1].clear()
        wInputs[1].send_keys("Remote TestKit")
        self.driver.save_screenshot("capture_06.png")
        wSubmitButton = self.driver.find_element(By.CSS_SELECTOR, "button")
        wSubmitButton.click()
        sleep(3)

        # Webの結果画面
        self.driver.save_screenshot("capture_07.png")
        wH2 = self.driver.find_element(By.CSS_SELECTOR, "h2")
        resultText = wH2.text
        print("Text field value=" + resultText)

        # コンテキストをネイティブアプリに切り替え
        self.switchContext("NATIVE_APP")

        # Webviewを閉じる
        nCloseButton = self.driver.find_element(
            By.XPATH, "//XCUIElementTypeButton[@name='Back']"
        )
        nCloseButton.click()
        sleep(3)
        self.driver.save_screenshot("capture_08.png")


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(WebviewAppTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

import os
import sys
import unittest
from time import sleep
from appium import webdriver
from selenium.webdriver.common.by import By
from appium.options.common import AppiumOptions

# ------------------------------------------------------------------------------------------
# The original selenium.webdriver.remote.remote_connection is not implemented to access
# the endpoint via proxy. So We wrote a monkey patch for the proxy.
import certifi
import urllib3
from selenium.webdriver.remote.remote_connection import RemoteConnection

RemoteConnection.__org__init__ = RemoteConnection.__init__


def patch_init(self, remote_server_addr, keep_alive=False, ignore_proxy=False):
    print("\nMonkey patch version: selenium.webdriver.remote.remote_connection")
    RemoteConnection.__org__init__(self, remote_server_addr, keep_alive=keep_alive, ignore_proxy=ignore_proxy)

    if keep_alive:
        # Define proxy. Default value is squid port.
        PROXY_URL = "http://localhost:3128"
        self._conn = urllib3.ProxyManager(proxy_url=PROXY_URL, timeout=self._timeout)

        # If basic authentication is required, uncomment the following and define it.
        # headers = urllib3.util.make_headers(proxy_basic_auth="userid:password")
        # self._conn = urllib3.ProxyManager(
        #     proxy_url=PROXY_URL, proxy_headers=headers, cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())


RemoteConnection.__init__ = patch_init
# ------------------------------------------------------------------------------------------

# Specify userName, password to Environment variable
RTK_ACCESSTOKEN = os.environ.get('RTK_ACCESSTOKEN')

if not RTK_ACCESSTOKEN:
    print("Environment variable error")
    sys.exit()


class OpenUrlTest(unittest.TestCase):
    def setUp(self):
        caps = {
            'accessToken': RTK_ACCESSTOKEN,
            'deviceName': 'Nexus 5',
            'platformName': 'Android',
            'browserName': 'Chrome',
            'chromeOptions': {'w3c': False}
        }
        # Specify the endpoint
        options = AppiumOptions()
        for k in caps:
            options.set_capability(k, caps[k])
        self.driver = webdriver.Remote(
            "https://gwjp.appkitbox.com/wd/hub", options=options
        )
        print(f"command_executor={self.driver.command_executor}")
        print(f"proxy={self.driver.command_executor._conn.proxy}")

    def tearDown(self):
        self.driver.quit()

    def test_google_search(self):
        # print(self.driver.capabilities['snapshotUrl'])
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

require 'rubygems'
require 'test/unit'
require 'selenium-webdriver'
require 'appium_lib'

# get userName, password from Environment variable
RTK_USERNAME = ENV['RTK_USERNAME']
RTK_PASSWORD = ENV['RTK_PASSWORD']
unless RTK_USERNAME && RTK_PASSWORD then
    puts "Environment variable error"
    exit(0)
end


class OpenUrlTest < Test::Unit::TestCase
    def setup
        opts = {
            caps: {
                userName: RTK_USERNAME,
                password: RTK_PASSWORD,
                deviceName: 'Nexus 5',
                platformName: 'Android',
                browserName: 'Chrome',
                appiumVersion: '1.22.3',
                automationName: 'UiAutomator2'
            },
            appium_lib: {
                server_url: 'https://gwjp.appkitbox.com/wd/hub',
                wait: 60
            }
        }
        @driver = Appium::Driver.new(opts).start_driver
    end

    def teardown
        @driver.quit()
    end

    def test_google_search
        puts @driver.capabilities['snapshotUrl']
        # Open URL
        url = "https://www.google.com/"
        puts "Open URL: " + url
        @driver.get(url)
        element = @driver.find_element(:css, 'input[name="q"]')
        @driver.save_screenshot('capture_01.png')

        # Input keys
        word = "Remote testKit"
        puts "Input Keys: " + word
        element.send_keys(word)
        element.submit
        sleep(5)
        @driver.save_screenshot('capture_02.png')

        # Get value
        value = @driver.find_element(:css, 'input[name="q"]').value
        puts "Text field value=" + value
        assert_equal true, value == "Remote testKit"
    end
end

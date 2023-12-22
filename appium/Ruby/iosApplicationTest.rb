# gem install selenium-webdriver
# gem install appium_lib
# export RTK_USERNAME=xxxx
# export RTK_PASSWORD=xxxx

require 'rubygems'
require 'test/unit'
require 'selenium-webdriver'
require 'appium_lib'

# get userName, password from Environment variable
RTK_USERNAME = ENV['RTK_USERNAME']
RTK_PASSWORD = ENV['RTK_PASSWORD']
unless RTK_USERNAME && RTK_PASSWORD
  puts 'Environment variable error'
  exit(0)
end

class ContactsIOsTests < Test::Unit::TestCase
  def setup
    opts = {
      caps: {
        # get userName, password from Environment variable
        userName: RTK_USERNAME,
        password: RTK_PASSWORD,
        deviceName: 'iPhone 8.*',
        platformName: 'iOS',
        automationName: 'XCUITest',
        # lang is japanese
        # platformVersion: '13',
        # lang is english
        platformVersion: '14.0.1',
        app: 'RTKappium.ipa',
        bundleId: 'com.example.remotetestkit.demo'
      },
      appium_lib: {
        server_url: 'https://gwjp.appkitbox.com/wd/hub',
        wait: 60
      }
    }
    @driver = Appium::Driver.new(opts).start_driver
  end

  def teardown
    @driver.quit
  end

  def test_application
    puts @driver.capabilities['snapshotUrl']
    @driver.save_screenshot('capture_01.png')

    # get text fields and set text in it
    textfields = @driver.find_elements(:xpath, '//XCUIElementTypeTextField')
    textfields[0].send_keys('RTK')
    textfields[1].send_keys('Remote TestKing')
    @driver.save_screenshot('capture_02.png')

    # click Save button
    element = @driver.find_element(:xpath,'//XCUIElementTypeButton[@name="Save"]')
    element.click()
    sleep(5)

    # set text from Login display
    result = @driver.find_elements(:xpath,'//XCUIElementTypeStaticText')[-1]
    puts 'Login Result : ' + result.text
    assert_equal('Password Error', result.text)
    @driver.save_screenshot('capture_03.png')

    # press return key
    backbutton = @driver.find_element(:xpath,'//XCUIElementTypeButton[@name="Back"]')
    backbutton.click()
    sleep(5)

    # delete and set text to text fields
    textfields[1].clear()
    textfields[1].send_keys('Remote TestKit')
    @driver.save_screenshot('capture_04.png')

    # click Save button
    element.click()
    sleep(5)

    # get text from Login display
    result = @driver.find_elements(:xpath,'//XCUIElementTypeStaticText')[-1]
    puts 'Login Result : ' + result.text
    assert_equal('Logged in', result.text)
    @driver.save_screenshot('capture_05.png')
  end
end
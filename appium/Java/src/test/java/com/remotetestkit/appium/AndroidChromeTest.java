package com.remotetestkit.appium;

import static org.junit.Assert.assertEquals;

import java.io.File;
import java.net.URL;

import org.apache.commons.io.FileUtils;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.remote.DesiredCapabilities;

import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.AndroidElement;
import io.appium.java_client.android.AndroidKeyCode;
import io.appium.java_client.remote.AndroidMobileCapabilityType;
import io.appium.java_client.remote.MobileCapabilityType;

import org.openqa.selenium.OutputType;

public class AndroidChromeTest {

	private static AndroidDriver<AndroidElement> driver;

	@BeforeAll
	static void initAll() throws Exception {
		DesiredCapabilities capabilities = new DesiredCapabilities();

		// get userName, password from Environment variable
		capabilities.setCapability("userName", System.getenv("userName"));
		capabilities.setCapability("password", System.getenv("password"));
		capabilities.setCapability(MobileCapabilityType.PLATFORM_NAME, "Android");
		capabilities.setCapability(MobileCapabilityType.DEVICE_NAME, "Nexus 5");
		capabilities.setCapability(AndroidMobileCapabilityType.BROWSER_NAME, "Chrome");
		capabilities.setCapability(MobileCapabilityType.APPIUM_VERSION, "1.15.1");

		driver = new AndroidDriver<>(new URL("https://gwjp.appkitbox.com/wd/hub"), capabilities);
	}

	@AfterAll
	static void tearDownAll() {
		driver.quit();
	}

	@Test
	void search() throws Exception {
		System.out.println("snapshotUrl: " + driver.getCapabilities().getCapability("snapshotUrl"));

		// Open URL
		String url = "https://www.google.com/";
		System.out.println("Open URL: " + url);
		driver.get(url);
		AndroidElement element = driver.findElementByName("q");
		Thread.sleep(5000);
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_01.png"));

		// Input keys
		String word = "Remote TestKit";
		System.out.println("Input Keys: " + word);
		element.sendKeys(word);
		element.submit();
		Thread.sleep(5000);
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_02.png"));

		// Get value
		String value = driver.findElementByName("q").getAttribute("value");
		System.out.println("Text field value=" + value);
		assertEquals(value, "Remote TestKit");

		driver.pressKeyCode(AndroidKeyCode.KEYCODE_APP_SWITCH);
		driver.pressKeyCode(AndroidKeyCode.KEYCODE_HOME);
	}
}

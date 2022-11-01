package com.remotetestkit.appium;

import java.io.File;
import java.net.URL;

import io.appium.java_client.android.nativekey.AndroidKey;
import io.appium.java_client.android.nativekey.KeyEvent;
import org.apache.commons.io.FileUtils;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;

import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.remote.AndroidMobileCapabilityType;
import io.appium.java_client.remote.MobileCapabilityType;

import org.openqa.selenium.OutputType;
import org.openqa.selenium.Keys;

public class AndroidChromeTest {

	private static AndroidDriver driver;

	@BeforeAll
	static void initAll() throws Exception {
		DesiredCapabilities capabilities = new DesiredCapabilities();

		// get userName, password from Environment variable
		capabilities.setCapability("userName", System.getenv("userName"));
		capabilities.setCapability("password", System.getenv("password"));
		capabilities.setCapability(MobileCapabilityType.PLATFORM_NAME, "Android");
		capabilities.setCapability(MobileCapabilityType.DEVICE_NAME, "Nexus 5");
		capabilities.setCapability(AndroidMobileCapabilityType.BROWSER_NAME, "Chrome");
		capabilities.setCapability("appiumVersion", "1.22.3");

		driver = new AndroidDriver(new URL("https://gwjp.appkitbox.com/wd/hub"), capabilities);
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
		WebElement element = driver.findElement(By.name("q"));
		Thread.sleep(5000);
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_B01.png"));

		// Input keys
		String word = "Remote TestKit";
		System.out.println("Input Keys: " + word);
		element.sendKeys(word);
		element.sendKeys(Keys.chord(Keys.ENTER));
		Thread.sleep(5000);
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_B02.png"));

		// Get value
		String value = driver.findElement(By.name("q")).getAttribute("value");
		System.out.println("Text field value=" + value);
		Assertions.assertEquals(value, "Remote TestKit");

		driver.pressKey(new KeyEvent(AndroidKey.APP_SWITCH));
		driver.pressKey(new KeyEvent(AndroidKey.HOME));
	}
}

// Please add apk file(/appium/apk/RTKdemo.apk) to "Remote testKit web(https://webapp.appkitbox.com) -> Rapid Tester -> Mobile App(Add)" before this test

package com.remotetestkit.appium;

import static org.junit.Assert.assertEquals;

import java.io.File;
import java.net.URL;
import java.util.List;

import org.apache.commons.io.FileUtils;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.remote.DesiredCapabilities;

import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.android.AndroidElement;
import io.appium.java_client.remote.AndroidMobileCapabilityType;
import io.appium.java_client.remote.MobileCapabilityType;

public class AndroidApplicationTest {

	private static AndroidDriver<AndroidElement> driver;

	@BeforeAll
	static void initAll() throws Exception {
		DesiredCapabilities capabilities = new DesiredCapabilities();

		// get userName, password from Environment variable
		capabilities.setCapability("userName", System.getenv("userName"));
		capabilities.setCapability("password", System.getenv("password"));
		capabilities.setCapability(MobileCapabilityType.PLATFORM_NAME, "Android");
		capabilities.setCapability(MobileCapabilityType.DEVICE_NAME, "Nexus 5");
		capabilities.setCapability("unicodeKeyboard", true);
		capabilities.setCapability("resetKeyboard", true);
		capabilities.setCapability(MobileCapabilityType.NEW_COMMAND_TIMEOUT, Integer.toString(180));
		// set application from RemoteTestKit storage
		// capabilities.setCapability(MobileCapabilityType.APP, "RTKdemo.apk");
		// set application from HTTP Url
		capabilities.setCapability(MobileCapabilityType.APP, "https://github.com/remotetestkit/sample-code/raw/master/appium/apk/RTKdemo.apk");
		capabilities.setCapability(AndroidMobileCapabilityType.APP_PACKAGE, "com.example.remotetestkit.demo");
		capabilities.setCapability(AndroidMobileCapabilityType.APP_ACTIVITY, "MainActivity");

		driver = new AndroidDriver<>(new URL("https://gwjp.appkitbox.com/wd/hub"), capabilities);

	}

	@AfterAll
	static void tearDownAll() {
		driver.quit();
	}

	@Test
	void loginTest() throws Exception {
		System.out.println("snapshotUrl: " + driver.getCapabilities().getCapability("snapshotUrl"));
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_01.png"));

		// get text fields and set text in it
		List<AndroidElement> textfields = driver.findElementsByClassName("android.widget.EditText");
		textfields.get(0).sendKeys("RTK");
		textfields.get(1).sendKeys("Remote TestKing");
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_02.png"));

		// click Save button
		AndroidElement element = driver.findElementById("com.example.remotetestkit.demo:id/Save");
		element.click();

		// set text from Login display
		AndroidElement result = driver.findElementById("com.example.remotetestkit.demo:id/title4");
		System.out.println("Login Result : " + result.getText().toString());
		assertEquals("Password Error", result.getText().toString());
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_03.png"));

		// press return key
		driver.pressKeyCode(4);

		// delete and set text to text fields
		textfields.get(1).clear();
		textfields.get(1).sendKeys("Remote TestKit");
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_04.png"));

		// click Save button
		element.click();

		// get text from Login display
		result = driver.findElementById("com.example.remotetestkit.demo:id/title2");
		System.out.println("Login Result : " + result.getText().toString());
		assertEquals("Logged in", result.getText().toString());
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_05.png"));

		Thread.sleep(5000);
	}
}

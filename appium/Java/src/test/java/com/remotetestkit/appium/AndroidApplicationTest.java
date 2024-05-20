// Please add apk file(/appium/apk/RTKdemo.apk) to "Remote testKit web(https://webapp.appkitbox.com) -> Rapid Tester -> Mobile App(Add)" before this test

package com.remotetestkit.appium;

import java.io.File;
import java.net.URL;
import java.util.List;

import io.appium.java_client.android.nativekey.AndroidKey;
import io.appium.java_client.android.nativekey.KeyEvent;
import org.apache.commons.io.FileUtils;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.remote.DesiredCapabilities;

import io.appium.java_client.android.AndroidDriver;
import io.appium.java_client.remote.AndroidMobileCapabilityType;
import io.appium.java_client.remote.MobileCapabilityType;

public class AndroidApplicationTest {

	private static AndroidDriver driver;

	@BeforeAll
	static void initAll() throws Exception {
		DesiredCapabilities capabilities = new DesiredCapabilities();

		// get userName, password from Environment variable
		capabilities.setCapability("userName", System.getenv("userName"));
		capabilities.setCapability("password", System.getenv("password"));
		capabilities.setCapability(MobileCapabilityType.PLATFORM_NAME, "Android");
		capabilities.setCapability(MobileCapabilityType.DEVICE_NAME, "Pixel");
		capabilities.setCapability(MobileCapabilityType.PLATFORM_VERSION, "12");
		capabilities.setCapability("unicodeKeyboard", true);
		capabilities.setCapability("resetKeyboard", true);
		capabilities.setCapability(MobileCapabilityType.NEW_COMMAND_TIMEOUT, Integer.toString(180));
		capabilities.setCapability("appiumVersion", "1.22.3");
		// set application from RemoteTestKit storage
		// capabilities.setCapability(MobileCapabilityType.APP, "RTKdemo.apk");
		// set application from HTTP Url
		capabilities.setCapability(MobileCapabilityType.APP, "https://github.com/remotetestkit/sample-code/raw/master/appium/apk/RTKdemo.apk");
		capabilities.setCapability(AndroidMobileCapabilityType.APP_PACKAGE, "com.example.remotetestkit.demo");
		capabilities.setCapability(AndroidMobileCapabilityType.APP_ACTIVITY, "MainActivity");

		driver = new AndroidDriver(new URL("https://gwjp.appkitbox.com/wd/hub"), capabilities);

	}

	@AfterAll
	static void tearDownAll() {
		driver.quit();
	}

	@Test
	void loginTest() throws Exception {
		System.out.println("snapshotUrl: " + driver.getCapabilities().getCapability("snapshotUrl"));
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_A01.png"));

		// get text fields and set text in it
		List<WebElement> textFields = driver.findElements(By.className("android.widget.EditText"));
		textFields.get(0).sendKeys("RTK");
		textFields.get(1).sendKeys("Remote TestKing");
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_A02.png"));

		// click Save button
		WebElement element = driver.findElement(By.id("com.example.remotetestkit.demo:id/Save"));
		element.click();

		// set text from Login display
		WebElement result = driver.findElement(By.id("com.example.remotetestkit.demo:id/title4"));
		System.out.println("Login Result : " + result.getText());
		Assertions.assertEquals("Password Error", result.getText());
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_A03.png"));

		// press return key
		driver.pressKey(new KeyEvent(AndroidKey.BACK));

		// delete and set text to text fields
		textFields.get(1).clear();
		textFields.get(1).sendKeys("Remote TestKit");
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_A04.png"));

		// click Save button
		element.click();

		// get text from Login display
		result = driver.findElement(By.id("com.example.remotetestkit.demo:id/title2"));
		System.out.println("Login Result : " + result.getText());
		Assertions.assertEquals("Logged in", result.getText());
		FileUtils.copyFile(driver.getScreenshotAs(OutputType.FILE), new File("capture_A05.png"));

		Thread.sleep(5000);
	}
}

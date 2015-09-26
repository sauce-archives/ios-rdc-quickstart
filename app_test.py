from sauce_helpers import (on_platforms,
                           sauce_storage_upload,
                           SauceIosRealDeviceAppTest)

IOS_REAL_DEVICES = [
    # You could have many different iOS devices in here,
    # and test the same app on all of them.
    # In September 2015, the only device available in beta
    # is the iPhone 6, but more devices are on their way!
    # Note: the app *has* to be uploaded to Sauce Storage first.
    {
        "deviceName": "iPhone 6 Device",
        "platformName": "iOS",
        "platformVersion": "8.4",
        "app": sauce_storage_upload("./SampleApp.zip")
    }
]


@on_platforms(IOS_REAL_DEVICES)
class AppTest(SauceIosRealDeviceAppTest):
    def test_app(self):
        # Find the "Second" button, and click it
        self.driver.find_element_by_name('Second').click()
        # Wait for a second
        self.driver.implicitly_wait(1)
        # Check that we now see the Second View. If we didn't,
        # this would throw an exception
        self.driver.find_element_by_name('Second View')

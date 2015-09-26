from sauce_helpers import (on_platforms,
                           sauce_storage_upload,
                           SauceIosRealDeviceAppTest)

IOS_REAL_DEVICES = [{
    "deviceName": "iPhone 6 Device",
    "platformName": "iOS",
    "platformVersion": "8.4"
}]

APP_STORAGE_URL = sauce_storage_upload('./SampleApp.zip')


@on_platforms(IOS_REAL_DEVICES)
class AppTest(SauceIosRealDeviceAppTest):
    app = APP_STORAGE_URL

    def test_app(self):
        self.driver.find_element_by_name('Second').click()
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_name('Second View')


# @on_platforms(IOS_REAL_DEVICES)
# class WebTest(SauceIosRealDeviceWebTest):

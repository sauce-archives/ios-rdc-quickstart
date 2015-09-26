from sauce_helpers import (on_platforms,
                           SauceTest)

PLATFORMS = [
    {
        "browserName": "Safari",
        "deviceName": "iPhone 6 Device",
        "platformName": "iOS",
        "platformVersion": "8.4"
    },
    {
        "browserName": "Safari",
        "deviceName": "iPhone 6",  # Simulator. Because it doesn't say "Device"
        "platformName": "iOS",
        "platformVersion": "8.4"
    }
]


@on_platforms(PLATFORMS)
class WebTest(SauceTest):
    def test_website(self):
        # Navigate to the page and interact with the elements on the guinea-pig page using id.
        self.driver.get('http://saucelabs.com/test/guinea-pig')
        div = self.driver.find_element_by_id('i_am_an_id')
        # check the text retrieved matches expected value
        self.assertEqual('I am a div', div.text)

        # populate the comments field by id
        self.driver.find_element_by_id('comments').send_keys('My comment')

import new
import os
from saucestorage import SauceStorageClient
from selenium import webdriver
import sys
import unittest

USERNAME = os.environ.get('SAUCE_USERNAME')
ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')
API_ENDPOINT = 'ondemand.saucelabs.com:80'
HOST = 'saucelabs.com'

STORAGE_API = SauceStorageClient(USERNAME, ACCESS_KEY)


def sauce_storage_upload(filename):
    result = STORAGE_API.put(filename)
    return result['url']


# A Python decorator that allows you to specify that a certain
# test needs to be run on various platforms.
def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)
    return decorator


class SauceTest(unittest.TestCase):
    def setUp(self):
        # set a name for the test
        self.desired_capabilities['name'] = self.id()

        # initialize test driver
        sauce_url = "http://%s:%s@%s/wd/hub"
        command_executor = sauce_url % (USERNAME, ACCESS_KEY, API_ENDPOINT)
        self.driver = webdriver.Remote(
            desired_capabilities=self.desired_capabilities,
            command_executor=command_executor
        )

    def tearDown(self):
        msg = "Link to your job: https://%s/jobs/%s"
        print msg % (HOST, self.driver.session_id)
        self.driver.quit()

# This creates a test with appropriate driver for an iOS app
# The test *must* have an "app" property defined, with the path
# to the app on the filesystem.
class SauceIosRealDeviceAppTest(SauceTest):
    def setUp(self):
        # When using the iOS Real Device Cloud, we must use an app that
        # is already uploaded to the Sauce Storage API. This is indicated
        # by a URL that starts with 'sauce-storage:'
        if not 'app' in self.desired_capabilities
            raise Exception("Test must have 'app' property, a 'sauce-storage:' URL")
        app = self.desired_capabilities['app']
        if not app.startswith('sauce-storage:'):
            msg = ("Invalid app: '{}'. For Sauce Labs iOS Real Device tests, "
                   "app must be a 'sauce-storage:' URL")
            raise Exception(msg.format(app))

        super(SauceIosRealDeviceAppTest, self).setUp()

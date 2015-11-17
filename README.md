# Quick Start to the Sauce Labs iOS Real Device Cloud

We're proud to present the new Sauce Labs Real Device Cloud. Now, you
can test your apps and websites on actual iOS devices like the iPhone 6. 

We can do it because we've hooked real iOS devices up to the cloud, and made them
run your tests just like iOS simulators... almost.

To get you started, we've put together some sample tests, with a sample app, that you can try -- right now --
with your own Sauce Labs account.

## Running the example tests

Sauce Labs works with Selenium libraries in any language, but the examples here
are (for now) just in Python. So you'll need to be familiar with running scripts 
on the command line, and have Python 2.x or better installed.

To get these scripts to work, first you'll need a couple of environment variables. 

### Environment variables

`SAUCE_USERNAME` should be the 
username you use to log into [https://saucelabs.com/](http://saucelabs.com/). 

`SAUCE_ACCESS_KEY` should be the "access key" that Sauce assigned to you. To find it, first log into
your account on the Sauce Labs website.
* If you're using the new interface (it looks blue), click on your user account in the bottom left-hand
  corner. This should pop open a menu. Click on **User Settings**. This opens your User Settings page. 
  Scroll down to find your Access Key.
* In the old interface (it looks more red and yellow), the Access Key is in the grey column on the 
  left hand side.


#### Linux or Mac OS X users

Type these commands:

```bash
export SAUCE_USERNAME=your_username
export SAUCE_ACCESS_KEY=your_access_key
```

You might want to add these lines to your shell's startup profile, which for most people
is in their home directory under `.bash_profile`.

#### Windows users

Type these commands:

```
set SAUCE_USERNAME=your_username
set SAUCE_ACCESS_KEY=your_access_key
```

You might want to add this to your default environment variables.

### Install test libraries

If you use Sauce already, you almost certainly have this stuff, but in case you are 
on a fresh machine: in the shell, enter the directory where you installed these files.
And then, install dependencies with `pip install -r requirements.txt`.

### How to run the tests

Log into your account on Sauce Labs. It's not necessary, but it's just interesting to watch the tests
progress.

In a shell, enter the directory containing the test files. To run the tests, just type `nosetests -vv`. 

`nosetests` will find anything that looks like a test and run it. It may take a while before you
see anything, but soon you'll see tests running, in your shell and in the web interface for your account!



## How to write your own tests

Hopefully that worked (if it didn't, see the contact info below) and you're interested in writing your own
tests now. Let's have a look at these example tests for clues about how to write your own.

### Web tests

To start, let's look at `test_web.py`, and see what's happening. 

`test_web` peforms a simple test of a web page, on two different platforms; an iPhone 6 simulator, and 
an iPhone 6. The `@on_platforms` decorator is just a handy way of running the same test on various platforms.

As you can see, the `capabilities` for a real device are very similar to those for a simulator. 
The only difference is that instead of saying `"deviceName": "iPhone 6"`, you use `"deviceName": "iPhone 6 Device"`.

And that's just about it. There isn't much that's different for a web test between platforms.

The one thing to watch out for is that we haven't yet released [Sauce Connect](https://docs.saucelabs.com/reference/sauce-connect/) for iOS 
Real Devices. But it's on the way! Check with Sauce Labs for updates.

### App tests

Pop open the file `test_app.py` and have a look!

This performs a really simple test on a simple app. The app has two views, and the test just clicks on 
one button and checks if the view has changed.

You specify a real device in your capabilities just like the web test - `"deviceName": "iPhone 6 Device"`. 

You put the app in `"app"`, but there are a few things to watch out for:

#### Building

Up till now you've probably only been uploading simulator apps to Sauce Labs. But if you run your app on a real iOS device, it 
has to be compiled and archived specially for one.

We can't go into a full discussion of how to compile iOS apps, but here are some tips to get you started:

* You can make a `.app` directory or an `.ipa`. (See the **Uploading** section).
* If you are using Apple's development IDE, XCode, you will have to create a "scheme" which archives the application to a file. Then
  use that as your app file. Here's where to start in Apple's documentation: 
  * [XCode Overview: Run Your App](https://developer.apple.com/library/ios/documentation/ToolsLanguages/Conceptual/Xcode_Overview/RunYourApp.html)_ 
  * [XCode Help: Archiving Your Application](https://developer.apple.com/library/ios/recipes/xcode_help-scheme_editor/Articles/SchemeArchive.html) 
* If you are building with the command-line tool, `xcodebuild`, the arguments should include:

  `-arch armv7 -sdk iphoneos`

  This StackOverflow post, 
  [xcodebuild simulator or device?](http://stackoverflow.com/questions/5010062/xcodebuild-simulator-or-device) may also help.


#### Uploading

Sauce Labs can accept your app in two formats.

  * As an IPA archive, whose filename must end in `.ipa`; or
  * A zipped `.app` directory, whose filename must end in `.zip`.

The big difference from simulator tests is that you have to upload a real device iOS app to 
[Sauce Storage](https://support.saucelabs.com/customer/portal/articles/2018312-uploading-apps-to-sauce-storage) first.

Sauce Storage is a convenient place to temporarily store files that your tests will need. Rather than waste time and bandwidth
transferring the file over to us for every test, you can just upload it to us once, in a secure, private area.

For most tests, Sauce Storage is optional, but for the iOS Real Device Cloud, it is required. However, we've made it 
easy with the helpers in this package. All you have to do in the capabilities is to specify the app as 
`"app": sauce_storage_upload("your_app.zip")` and you're done.

If you want to upload the app yourself ahead of time, the `saucestorage` helper library, included here, could be of use. Or, 
see the [Sauce Storage API documentation](https://docs.saucelabs.com/reference/rest-api/#temporary-storage). Just make sure, once
you've uploaded the app, that you use a `sauce-storage:` URL. So the test capabilities would have a line like `"app": "sauce-storage:your_app.zip"`.


#### Provisioning

And here's a thing *not* to watch out for. You may already be aware that iOS apps in development don't work on just any iPhone or iPad.
In Apple parlance, the apps need to be signed and provisioned for a set of devices. So you may be wondering how we can install
your apps on our devices and test them. But you don't need to worry; we've taken care of that! Just upload the app and it will work.

If you can run it on an iOS real device, so can we. 

## Where to find out more

We're still producing supporting materials for the iOS Real Device Cloud, so if you have any questions contact [Chiarng Lin](mailto:chiarng@saucelabs.com) 
or [Neil Manvar](mailto:neil@saucelabs.com).

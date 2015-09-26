# Quick Start to the Sauce Labs iOS Real Device Cloud

We're proud to present to your our new Real Device Cloud. Now, you
can test your apps and websites on actual iOS devices like the iPhone 6. 

We can do it because we've hooked them up to the cloud, and made them
work just like the tests you used to work on simulators... almost.

So here are a few things you need to know first:

## Getting started

You'll need to be familiar with running scripts on the command line, and have
Python 2.x or better installed.

First you'll need a couple of environment variables. 

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

## Install test libraries

If you use Sauce already, you almost certainly have this stuff, but in case you are 
on a fresh machine: in the shell, enter the directory where you installed these files.
And then, install dependencies with `pip install -r requirements.txt`.

## How to run the tests

Log into your account on Sauce Labs. It's not necessary, but it's just interesting to watch the tests
progress.

In a shell, enter the directory containing the test files. To run the tests, just type `nosetests -vv`. 

`nosetests` will find anything that looks like a test and run it. It may take a while before you
see anything, but soon you'll see tests running, in your shell and in the web interface for your account!


## How to write your own tests

### Web tests

To start, let's look at `test_web.py`, and see what's happening. 

`test_web` peforms a simple test of a web page, on two different platforms; an iPhone 6 simulator, and 
an iPhone 6. The `@on_platforms` decorator is just a handy way of running the same test on various platforms.

As you can see, the `capabilities` for a real device are very similar to those for a simulator. 
The only difference is that instead of saying `"deviceName": "iPhone 6"`, you use `"deviceName": "iPhone 6 Device"`.

And that's just about it. There isn't much that's different for a web test between platforms.

The one thing to watch out for is that, as of September 2015, we haven't yet released [Sauce Connect](https://docs.saucelabs.com/reference/sauce-connect/) for iOS 
Real Devices. But it's on the way! Check with Sauce Labs for updates.

### App tests

Pop open the file `test_app.py` and have a look!

This performs a really simple test on a simple app. The app has two views, and the test just clicks on 
one button and checks if the view has changed.

You specify a real device in your capabilities just like the web test - `"deviceName": "iPhone 6 Device"`. 

You put the app in `"app"`, but there are two things to watch out for:

#### Building

The app has to be compiled for an iOS real device.** Up till now you've probably only been uploading simulator apps to Sauce Labs. If
you upload a simulator app, you'll get a confusing error message. (We're working on that!)

We can't go into a full discussion of how to compile iOS apps, but here are some tips to get you started:

* If you are using Apple's development IDE, XCode, you will have to create a "scheme" which archives the application to a file. Then
  use that as your app file. Here's where to start in Apple's documentation: 
  * [XCode Overview: Run Your App](https://developer.apple.com/library/ios/documentation/ToolsLanguages/Conceptual/Xcode_Overview/RunYourApp.html)_ 
  * [XCode Help: Archiving Your Application](https://developer.apple.com/library/ios/recipes/xcode_help-scheme_editor/Articles/SchemeArchive.html) 
* If you are building with the command-line tool, `xcodebuild`, the arguments should include `-arch armv7 -sdk iphoneos`. This StackOverflow post, 
  [xcodebuild simulator or device?](http://stackoverflow.com/questions/5010062/xcodebuild-simulator-or-device) may also help.

#### Uploading

This is the biggest difference from simulator tests. You have to upload a real device iOS app to 
[Sauce Storage](https://support.saucelabs.com/customer/portal/articles/2018312-uploading-apps-to-sauce-storage) first.

Sauce Storage is a convenient place to store files that your tests will need. Rather than waste time and bandwidth
transferring the file over to us for every test, you can just upload it to a secure, private area that only your tests can access.

For other kinds of tests, Sauce Storage is optional, but for the iOS Real Device Cloud, it is required. However, we've made it 
extra easy with the helpers in this package. All you have to do in the capabilities is to specify the app as 
`sauce_storage_upload("your_app.zip")` and you're done.

#### Provisioning

And here's a thing *not* to watch out for. You may already be aware that iOS apps in development don't work on just any iPhone or iPad.
In Apple parlance, the apps need to be signed and provisioned for a set of devices. So you may be wondering how we can install
your apps on our devices and test them. But you don't need to worry; we've taken care of that! Just upload the app and it will work. 

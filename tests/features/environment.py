import os

from behave import given, when, then

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import UnexpectedAlertPresentException


def before_all(context):
    """ Setup Selenium WebDriver """
    # set to true to test in the Vagrant
    run_headless = os.getenv('CONTINUOUS_INTEGRATION', '') > ''

    if not run_headless:
        print("Using Firefox driver")
        context.driver = webdriver.Firefox()
        url = "http://localhost:8080"
    else:
        print("Using SauceLabs driver")

        # ----------------------------------------------------------------
        # This is the only code you need to edit in your existing scripts.
        # The command_executor tells the test to run on Sauce, while the
        # desired_capabilties parameter tells us which browsers and OS to
        # spin up.
        # ----------------------------------------------------------------
        desired_cap = {
            'platform': "Mac OS X 10.9",
            'browserName': "firefox",
            'version': "40",
            'tunnel-identifier': os.environ['TRAVIS_JOB_NUMBER']
        }
        sauce_url = "http://{0}:{1}@ondemand.saucelabs.com/wd/hub".format(
            os.environ['SAUCE_USERNAME'],os.environ['SAUCE_ACCESS_KEY'])

        context.driver = webdriver.Remote(
            command_executor=sauce_url,
            desired_capabilities=desired_cap)
        # ----------------------------------------------------------------

        url = "http://localhost"

    print("Using url: {}".format(url))
    context.base_url = url
    context.driver.set_window_size(1024, 800)
    context.driver.implicitly_wait(3)
    context.accept_next_alert = True

    context.select = Select

    context.wait = wait
    context.Keys = Keys
    context.NoSuchElementException = NoSuchElementException


def wait(driver, xpath):
    wait_ = WebDriverWait(driver, 10)
    ele = wait_.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    ele.click()
    return ele


def after_all(context):
    """ Close WebDriver once we're done """
    context.driver.quit()


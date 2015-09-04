# -*- coding: utf-8 -*-

# To run:
#   python tests/test_redcap_hooks.py

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import UnexpectedAlertPresentException


import unittest, time, re
import os


class TestRedcapHooks(unittest.TestCase):
    def setUp(self):

        # set to true to test in the Vagrant
        run_headless = os.getenv('CONTINUOUS_INTEGRATION', '') > ''

        if not run_headless:
            print("Using Firefox driver")
            self.driver = webdriver.Firefox()
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
                'platform': "Mac OS X 10.10",
                'browserName': "firefox",
                'version': "40",
                'tunnel-identifier': "125.1",
                'build': os.environ['TRAVIS_BUILD_NUMBER']
            }
            sauce_url = "http://{0}:{1}@ondemand.saucelabs.com:80/wd/hub".format(
                os.environ['SAUCE_USERNAME'],os.environ['SAUCE_ACCESS_KEY'])

            self.driver = webdriver.Remote(
                command_executor=sauce_url,
                desired_capabilities=desired_cap)
            # ----------------------------------------------------------------

            url = "http://localhost:8080"

        print("Using url: {}".format(url))
        self.base_url = url
        self.driver.set_window_size(1024, 800)
        self.driver.implicitly_wait(3)
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_redcap_hooks(self):
        driver = self.driver
        try:
            driver.get(self.base_url + "/redcap/index.php")
            driver.find_element_by_css_selector("font").click()
            driver.find_element_by_id("app_title").clear()
            driver.find_element_by_id("app_title").send_keys("This is the Project Title")
            Select(driver.find_element_by_id("purpose")).select_by_visible_text("Practice / Just for fun")
            driver.find_element_by_css_selector("input[type=\"button\"]").click()
            time.sleep(0.2)

            # Version 6.5.3 needs to un-check the "Auto-numbering for records" option
            driver.find_element_by_xpath("""//button[@onclick="saveProjectSetting($(this),'auto_inc_set','1','0',1,'setupChklist-modules');"]""").click()

            print("Click 'Online Designer'")
            time.sleep(1)
            driver.find_element_by_xpath("//div[@id='setupChklist-design']/table/tbody/tr/td[2]/div[2]/div/button").click()
            driver.find_element_by_id("formlabel-my_first_instrument").click()
            driver.find_element_by_id("btn-last").click()
            Select(driver.find_element_by_id("field_type")).select_by_visible_text("Text Box (Short Text)")
            driver.find_element_by_id("field_label").clear()
            driver.find_element_by_id("field_label").send_keys("How many times did the event occur?")
            driver.find_element_by_id("field_name").click()
            driver.find_element_by_id("field_name").clear()
            driver.find_element_by_id("field_name").send_keys("occurrences")
            Select(driver.find_element_by_id("val_type")).select_by_visible_text("Integer")
            driver.find_element_by_id("val_min").clear()
            driver.find_element_by_id("val_min").send_keys("0")
            driver.find_element_by_id("val_max").clear()
            driver.find_element_by_id("val_max").send_keys("50")
            driver.find_element_by_id("field_note").clear()
            driver.find_element_by_id("field_note").send_keys("0-50 (<span class=valid>-1</span> if unknown)")
            driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
            time.sleep(0.3)

            print("Adding subject 1...")
            wait = WebDriverWait(driver, 10)
            xpath = "//a[contains(text(),'Add / Edit Records')]"
            ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            ele.click()

            xpath = "//input[@id='inputString']"
            ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            ele.clear()
            ele.send_keys(1)
            ele.send_keys(Keys.ENTER)
            time.sleep(0.5)

            print("Enter data for subject 1")
            driver.find_element_by_name("occurrences").clear()
            driver.find_element_by_name("occurrences").send_keys("-1")

            print("Set my_first_instrument_complete")
            Select(driver.find_element_by_name("my_first_instrument_complete")).select_by_visible_text("Complete")
            driver.find_element_by_name("submit-btn-cancel").click()
            driver.find_element_by_link_text("Project Home").click()
            driver.find_element_by_link_text("My Projects").click()
            driver.find_element_by_link_text("Control Center").click()
            driver.find_element_by_link_text("General Configuration").click()

            try:
                os.remove('hooks/redcap_data_entry_form')
            except Exception as exc:
                print("Moving on {}".format(exc))

            print("Create symlink for the hook we are activating: ")
            print("ln -s library/redcap_data_entry_form hooks/redcap_data_entry_form")
            os.symlink('library/redcap_data_entry_form', 'hooks/redcap_data_entry_form')
            driver.find_element_by_name("hook_functions_file").clear()
            driver.find_element_by_name("hook_functions_file").send_keys("/redcap_data/hooks/redcap_hooks.php")
            time.sleep(0.2)
            driver.find_element_by_css_selector("input[type=\"submit\"]").click()
            print("Hook enabled...")

            print("Adding data to subject 1... This time the hook should be active")
            driver.find_element_by_link_text("My Projects").click()
            driver.find_element_by_link_text("This is the Project Title").click()
            wait = WebDriverWait(driver, 10)
            xpath = "//a[contains(text(),'Add / Edit Records')]"
            ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            ele.click()

            xpath = "//input[@id='inputString']"
            ele = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            ele.clear()
            ele.send_keys(1)
            ele.send_keys(Keys.ENTER)
            time.sleep(0.5)

            print("Enter data for subject 1")
            driver.find_element_by_name("occurrences").clear()
            driver.find_element_by_name("occurrences").send_keys("-1")
            Select(driver.find_element_by_name("my_first_instrument_complete")).select_by_visible_text("Complete")
            driver.find_element_by_css_selector("option[value=\"2\"]").click()
            driver.find_element_by_name("submit-btn-saverecord").click()
            time.sleep(0.2)

            print("Verify that the data was saved with the hook enabled")
            Select(driver.find_element_by_id("record_select2")).select_by_visible_text("1")
            try:
                self.assertEqual("-1", driver.find_element_by_name("occurrences").get_attribute("value"))
            except AssertionError as e:
                self.verificationErrors.append(str(e))

            print("Delete the record we created...")
            driver.find_element_by_name("submit-btn-delete").click()
            driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
            driver.find_element_by_link_text("My Projects").click()

            print("Delete the project we created...")
            driver.find_element_by_link_text("This is the Project Title").click()
            driver.find_element_by_css_selector("li > a").click()
            driver.find_element_by_link_text("Other Functionality").click()
            driver.find_element_by_xpath("//input[@value='Delete the project']").click()
            driver.find_element_by_id("delete_project_confirm").clear()
            driver.find_element_by_id("delete_project_confirm").send_keys("DELETE")
            driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
            driver.find_element_by_xpath("(//button[@type='button'])[4]").click()
            driver.find_element_by_xpath("(//button[@type='button'])[3]").click()
            driver.find_element_by_link_text("My Projects").click()

            print("Remove the soft link for the hook")
            os.remove('hooks/redcap_data_entry_form')
        except:
            print("Saving sreenshot to file: screenshot-test_redcap_hooks.png")
            driver.get_screenshot_as_file('screenshot-test_redcap_hooks.png')
            raise

        print("Done. Yay!")

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True

    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True

    def tearDown(self):
        # This is where you tell Sauce Labs to stop running tests on your behalf.
        # It's important so that you aren't billed after your test finishes.
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()

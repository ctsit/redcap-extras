import os
import shutil
import time

from behave import given, when, then


# base directory containing the "hooks/" folder
HOOKS_ROOT=os.getenv('TRAVIS_BUILD_DIR', '/redcap_data')


@given('the "Complex Validation" hook has been installed')
def given_the_hook_has_been_installed(context):
    driver = context.driver

    driver.get(context.base_url + "/redcap/index.php")
    driver.find_element_by_link_text("My Projects").click()
    driver.find_element_by_link_text("Control Center").click()
    driver.find_element_by_link_text("General Configuration").click()
    driver.find_element_by_name("hook_functions_file").clear()
    driver.find_element_by_name("hook_functions_file")\
          .send_keys(HOOKS_ROOT + '/hooks/redcap_hooks.php')
    print(HOOKS_ROOT + '/hooks/redcap_hooks.php')
    time.sleep(0.2)
    driver.find_element_by_css_selector('input[type="submit"]').click()

    context.hook = AutomaticHookCleanup()
    print("Hook enabled.")


@given('a project exists with a "Demographics" form')
def given_form(context):
    driver = context.driver
    driver.get(context.base_url + "/redcap/index.php")
    driver.find_element_by_css_selector("font").click()
    driver.find_element_by_id("app_title").clear()
    driver.find_element_by_id("app_title").send_keys("This is the Project Title")
    context.select(driver.find_element_by_id("purpose")).select_by_visible_text("Practice / Just for fun")
    driver.find_element_by_css_selector("input[type=\"button\"]").click()
    time.sleep(0.2)
    # Version 6.5.3 needs to un-check the "Auto-numbering for records" option
    driver.find_element_by_xpath("""//button[@onclick="saveProjectSetting($(this),'auto_inc_set','1','0',1,'setupChklist-modules');"]""").click()
    time.sleep(1)


@given('the "Demographics" form has a "Birth Month" field with a range of 1-12')
def given_field(context):
    # Demonstrating that we don't actually have to do anything if it's easier
    # to just implement in one step. In this case, we'll create the field in
    # the next one and just use "My First Instrument" as the "Demographics"
    # form.
    pass


@given('the notes for that field read "{notes}"')
def given_field_notes(context, notes):
    driver = context.driver
    driver.find_element_by_xpath("//div[@id='setupChklist-design']/table/tbody/tr/td[2]/div[2]/div/button").click()
    driver.find_element_by_id("formlabel-my_first_instrument").click()
    driver.find_element_by_id("btn-last").click()
    context.select(driver.find_element_by_id("field_type")).select_by_visible_text("Text Box (Short Text)")
    driver.find_element_by_id("field_label").clear()
    driver.find_element_by_id("field_label").send_keys("Birth Month")
    driver.find_element_by_id("field_name").click()
    driver.find_element_by_id("field_name").clear()
    driver.find_element_by_id("field_name").send_keys("birth_month")
    context.select(driver.find_element_by_id("val_type")).select_by_visible_text("Integer")
    driver.find_element_by_id("val_min").clear()
    driver.find_element_by_id("val_min").send_keys("1")
    driver.find_element_by_id("val_max").clear()
    driver.find_element_by_id("val_max").send_keys("12")
    driver.find_element_by_id("field_note").clear()
    driver.find_element_by_id("field_note").send_keys(notes)
    driver.find_element_by_xpath("(//button[@type='button'])[2]").click()
    time.sleep(0.3)


@given('I\'m filling out the "Birth Month" field of the "Demographics" form')
def given_field_focus(context):
    driver = context.driver

    print("Adding subject 1...")
    context.wait(driver, xpath="//a[contains(text(),'Add / Edit Records')]")

    ele = context.wait(driver, xpath="//input[@id='inputString']")
    ele.clear()
    ele.send_keys(1)
    ele.send_keys(context.Keys.ENTER)
    time.sleep(0.5)


@when('I enter "99" for "Unknown"')
def when_i_enter_value_for_field(context):
    driver = context.driver
    print("Enter data for subject 1")
    driver.find_element_by_name("birth_month").clear()
    driver.find_element_by_name("birth_month").send_keys("99")
    context.select(driver.find_element_by_name("my_first_instrument_complete")).select_by_visible_text("Complete")
    driver.find_element_by_css_selector("option[value=\"2\"]").click()
    time.sleep(0.2)


@then('I should not see the normal "Out of Range" alert.')
def then_i_should_not_see_alert(context):
    try:
        context.driver.find_element_by_css_selector("div.ui-dialog")
        assert False, "Sadly, the alert is present."
    except context.NoSuchElementException:
        return True


class AutomaticHookCleanup(object):
    """ Enables the hook upon creation and disables it when destroyed """

    def __init__(self):
        try:
            os.mkdir('hooks/redcap_data_entry_form')
        except OSError:
            print('"hooks/redcap_data_entry_form" already exists')

        print('Copying hook file: ')
        print('hooks/library/redcap_data_entry_form/complex_validation.php ->'
              ' hooks/redcap_data_entry_form/')
        shutil.copy('hooks/library/redcap_data_entry_form/complex_validation.php',
                    'hooks/redcap_data_entry_form/')

    def __del__(self):
        os.remove('hooks/redcap_data_entry_form/complex_validation.php')
        print('Hook removed.')


# -*- coding: utf-8 -*-
from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re


class CourseBreadcrumbs(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        # self.driver.implicitly_wait(30)
        self.base_url = "http://localhost:8000/admin"
        self.verificationErrors = []
        self.accept_next_alert = True

    def test_course_breadcrumbs(self):
        """
        Test that the breadcrumbs shown when looking at a detail form are correct.
        A Course name should be shown rather than a Course Object.
        """
        driver = self.driver
        driver.get("http://localhost:8000/admin")
        driver.find_element_by_id("id_username").click()
        driver.find_element_by_id("id_username").clear()
        driver.find_element_by_id("id_username").send_keys("admin")
        driver.find_element_by_id("id_password").clear()
        driver.find_element_by_id("id_password").send_keys("password")
        driver.find_element_by_xpath(
            "(.//*[normalize-space(text()) and normalize-space(.)='Password:'])[1]/following::input[3]").click()
        driver.find_element_by_link_text("Courses").click()
        driver.find_element_by_link_text("Office 365 Access - Advanced").click()
        self.assertEqual(u"Home › Coursemanager › Courses › Office 365 Access - Advanced",
                         driver.find_element_by_xpath("(//*[@id=\"container\"]/div[2])").text)
        driver.find_element_by_xpath("//*[@id=\"user-tools\"]/a[3]").click()

    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
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
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()

#-*- coding:utf-8 -*-
import time
from selenium import webdriver
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from Log.Comlog import Log
log = Log()
class BasePaeg(object):
    """
    继承类面，并且封装
    """
    def __init__(self,driver):
        self.driver =driver

    def quit_browser(self):
        self.driver.quit()
        log.info(u"定义页面退出")

    def wait(self,three):#显示等待
         self.driver.implicitly_wait(three)

    def find_element(self,selector):
        element = ''
        if '=>' not in selector:
            return self.driver.find_element_by_id(selector)
        selector_by = selector.split('=>')[0]
        selector_value = selector.split('=>')[1]

        if selector_by == "i" or selector_by == 'id':
            try:
                element = self.driver.find_element_by_id(selector_value)
                log.info("Had find the element \' %s \' successful "
                            "by %s via value: %s " % (element.text, selector_by, selector_value))
            except NoSuchElementException as e:
                log.error("NoSuchElementException: %s" % e)
        elif selector_by == "n" or selector_by == 'name':
            element = self.driver.find_element_by_name(selector_value)
        elif selector_by == "c" or selector_by == 'class_name':
            element = self.driver.find_element_by_class_name(selector_value)
        elif selector_by == "l" or selector_by == 'link_text':
            element = self.driver.find_element_by_link_text(selector_value)
        elif selector_by == "p" or selector_by == 'partial_link_text':
            element = self.driver.find_element_by_partial_link_text(selector_value)
        elif selector_by == "t" or selector_by == 'tag_name':
            element = self.driver.find_element_by_tag_name(selector_value)
        elif selector_by == "x" or selector_by == 'xpath':
            try:
                element = self.driver.find_element_by_xpath(selector_value)
                log.info("Had find the element \' %s \' successful "
                            "by %s via value: %s " % (element.text, selector_by, selector_value))
            except NoSuchElementException as e:
                log.error("NoSuchElementException: %s" % e)
        elif selector_by == "s" or selector_by == 'selector_selector':
            element = self.driver.find_element_by_css_selector(selector_value)
        else:
            raise NameError("Please enter a valid type of targeting elements.")

        return element

    def click(self,selector):
        el = self.find_element(selector)
        try:
            el.click()
        except NameError as e:
            log.error("Failed to click the element with %s" % e)

    def type(self,selector,text):
        el = self.find_element(selector)
        el.clear()
        try:
            el.send_keys(text)
            log.info("Had type \'%s\ in inputbox" % text)
            # el.send_keys(password)
            # log.info("Had type \'%s\ in inputbox" %password)
        except NameError as e:
            log.error("Failed to type in input box with %s" % e)

    def clear(self,selector,text):
        el = self.find_element(selector)
        try:
            el.clear(text)
            log.info("The %s is clear now" %text)
        except NameError as e:
            log.error("Fail to clear the message %s" %text)






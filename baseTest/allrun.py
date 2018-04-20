#-*- coding:utf-8 -*-
import HTMLTestRunnerCN
import unittest
import time
from selenium import webdriver
from common.SSData import random_str
from common.SSData import random_phone_number
from Log.Comlog import Log
from common.SSEmail import Email
from config import Readerconfig

log = Log()

class Test_Kad(unittest.TestCase):
    def setUp(self):
        log.info("---测试开始----")
        base_url = Readerconfig.Dat
        self.driver = webdriver.Chrome()
        self.driver.get(base_url)
    def test_Login(self):
        log.info("----开始测试登录----")
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/a[1]").click()
        log.info("输入账号")
        self.driver.find_element_by_id("UserName").send_keys(Readerconfig.User)
        log.info("输入密码")
        self.driver.find_element_by_id("UserPassword").send_keys(Readerconfig.Pw)
        self.driver.find_element_by_id("LoginButton").click()
        time.sleep(5)
        log.info("---kad账号登录成功----")
    def test_Regist(self):
        log.info("---开始注册测试----")
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/a[2]").click()
        log.info("输入注册账号")
        self.driver.find_element_by_id("txtMobile").send_keys(random_phone_number())
        log.info("输入注册密码")
        self.driver.find_element_by_id("txtPwd").send_keys(random_str())
        self.driver.find_element_by_id("txtImgCode").send_keys("4531")
        self.driver.find_element_by_id("txtMobileCode").send_keys("123456")
        self.driver.find_element_by_id("toLogin").click()
        time.sleep(5)
        if "欢迎注册康爱多账号" == 0:
            log.info("成功登入注册页面，注册成功")
        else:
            print "注册失败"

    def test_search(self):
        log.info("---开始搜索测试----")
        self.driver.find_element_by_id("pageText").clear()
        self.driver.find_element_by_id("pageText").send_keys(u"感冒药")
        self.driver.find_element_by_id("BtnSearchProdut").click()
        time.sleep(3)
        log.info("搜索成功")
    def tearDown(self):
        log.info("---测试结束---")
        self.driver.quit()

if __name__ == '__main__':
    Suite = unittest.TestSuite()
    Suite.addTest(Test_Kad('test_Login'))
    Suite.addTest(Test_Kad('test_Regist'))
    Suite.addTest(Test_Kad('test_search'))
    reportname = Readerconfig.RP +  "//report.html"
    f = file(reportname,'wb')
    runner = HTMLTestRunnerCN.HTMLTestReportCN(
        stream=f,title="Test report",description='Report_Description',verbosity=2
    )
    runner.run(Suite)
    log.info("生成测试报告")
    e = Email(title='360KAD web测试报告',
              message='这是本次自动化的报告，请领导查收！',
              receiver=Readerconfig.RE,
              server=Readerconfig.MH,
              sender=Readerconfig.SE,
              password=Readerconfig.MP,
              path=reportname
              )
    e.send()


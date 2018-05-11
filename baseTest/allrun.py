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
from selenium.webdriver.common.action_chains import ActionChains
from common.ImgScreen import Save
from common.page.public_page import Login,Resit,Search
log = Log()
class Test_Kad(unittest.TestCase):
    def setUp(self):
        log.info("---测试开始----")
        base_url = Readerconfig.Dat
        self.driver = webdriver.Chrome()
        self.driver.get(base_url)
        self.assertEqual(u"【康爱多网上药店】-药品网购,网上买药就上排名前列并提供医药网资讯的康爱多药品网",self.driver.title)
    def test_Login(self):
        log.info("----开始测试登录----")
        loginpage = Login(self.driver)
        loginpage.type_loginLogin()
        time.sleep(5)
        loginpage.type_loginUser(Readerconfig.User)
        loginpage.type_loginPw(Readerconfig.Pw)
        log.info("---可以输入账号了呀")
        time.sleep(5)
        log.info("---赶紧输入密码吧")
        loginpage.type_loginRLogin()
        time.sleep(5)
        log.info("---kad账号登录成功了，小伙伴要开始买东西了吗----")
    def test_Regist(self):
        registpage = Resit(self.driver)
        log.info("---开始注册测试----")
        registpage.type_regist()
        log.info("你可以输入注册账号了")
        registpage.type_moblie(random_phone_number())
        log.info("再输入注册密码试试看")
        registpage.type_pwd(random_str())
        registpage.type_imgacode("4531")
        registpage.type_mobilecode("123456")
        registpage.type_tl()
        self.driver.implicitly_wait(5000)
        self.assertEqual(u"用户注册",self.driver.title)

    def test_search(self):
        log.info("---开始搜索测试----")
        searchprut = Search(self.driver)
        log.info("-----输入搜索关键词-----")
        self.driver.implicitly_wait(5000)
        searchprut.type_textpage(u"感冒药")
        searchprut.type_btnsearch()
        self.driver.implicitly_wait(5000)
        self.assertEqual(u"感冒药_商品搜索_康爱多网上药店",self.driver.title)
        log.info("搜索成功")
        time.sleep(2)


    def test_Bugcat(self):
        self.test_search()
        time.sleep(5)
        ActionChains(self.driver).move_to_element(self.driver.find_element_by_id("Img33923")).perform()
        time.sleep(10)
        self.driver.find_element_by_id("Img33923").click()
        time.sleep(3)
        log.info("---感冒要开始加入购物车了哦---")
        time.sleep(2)
        #切换到新的标签窗口去了
        now_handle = self.driver.current_window_handle
        all_handle = self.driver.window_handles
        for handle in all_handle:
            if handle != now_handle:
                self.driver.switch_to.window(handle)
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="num_rvalue"]').click()
        time.sleep(10)
        self.driver.find_element_by_id("bybuy").click()
        time.sleep(10)
        self.assertEqual(self.driver.find_element_by_xpath('//*[@id="ul1"]/li/p/a').text,u"同仁堂 羚翘解毒丸 9g*10丸")
        log.info("----商品已经加入购物车了，赶紧付款吧----")
    def tearDown(self):
        log.info("---测试结束---")
        self.driver.quit()


if __name__ == '__main__':
    Suite = unittest.TestSuite()
    Suite.addTest(Test_Kad('test_Login'))
    Suite.addTest(Test_Kad('test_Regist'))
    Suite.addTest(Test_Kad('test_search'))
    Suite.addTest(Test_Kad('test_Bugcat'))
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


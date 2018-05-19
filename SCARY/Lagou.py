#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf8')
headers= {
    'User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}
url = "https://www.lagou.com/jobs/list_%E6%96%B0%E5%AA%92%E4%BD%93%E8%BF%90%E8%90%A5?px=default&city=%E5%85%A8%E5%9B%BD#filterBox"
driver = webdriver.Chrome()
driver.get('https://www.lagou.com/jobs/list_%E6%96%B0%E5%AA%92%E4%BD%93%E8%BF%90%E8%90%A5?px=default&city=%E5%85%A8%E5%9B%BD#filterBox')
driver.find_element_by_xpath('//*[@id="s_position_list"]/div[2]/div/span[6]').click()

while True:

    r = requests.get(url, headers=headers)  # 连接
    content = r.text  # 获取内容，自动转码unicode
    soup = BeautifulSoup(content, "html.parser")
    items = soup.findAll('div',attrs ={'class':'sojob-item-main clearfix'})
    items2 = soup.findAll('div',attrs={'class':'company-info nohover'})
    for item in items:
        JobName = item.div.h3.get_text()
        CCname =item.div.p.span.get_text()
        #ComName = item.div.p.a.get_text()

    for item in items2:
        ComName2 = item.find('a').get('title')
        CComname = item.find('span').get_text()

        print u"公司名称：%s" %ComName2
        print u"公司经营类型：%s"%CComname
        print u"职位薪酬：%s" %CCname
        print u"招聘职位：%s" %JobName.strip()
        print u'当前页数数据已经爬完'
        with open("LIEPIN.txt", 'a') as f:
            f.write(ComName2+ CComname+ CCname + JobName+ '\n')
            f.close()










#-*- coding:utf-8 -*-
import requests
import os
from bs4 import BeautifulSoup
import os
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
pageindx = 0
headers= {
    'User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}
# while True:
for pageindx in range(0,91):
    if pageindx>90:
        break
    else:
        pageindx +=1
        url = "https://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%85%A8%E5%9B%BD&kw=%E6%96%B0%E5%AA%92%E4%BD%93%E8%BF%90%E8%90%A5&sm=0&p=" + str(pageindx)
        r = requests.get(url, headers=headers)  # 连接
        content = r.text  # 获取内容，自动转码unicode
        soup = BeautifulSoup(content, "html.parser")
        items = soup.findAll('td',attrs={'class':'zwmc'})
        items2 = soup.findAll('td',attrs={'class':'gsmc'})
        items3 = soup.findAll('li',attrs={'class':'newlist_deatil_two'})
        # items2 = soup.findAll('div',attrs={'class':'company-info nohover'})
        for item in items:
            JobName = item.find('a').get_text()
            # CCname =item.div.p.span.get_text()
        for item in items2:
            ComName2 =item.find('a').get_text(strip=True)
            # CCname =item.find('zwyx')
        # for item in items3:
        #     CComname = item.find(text =re.compile('<span>.+?</span>'))
        # for item in items2:
        #     ComName2 = item.find('a').get('title')
        #     CComname = item.find('span').get_text()

            # print u"目前读取的页数为：%s" %pageindx
            print u"公司名称：%s" %ComName2
            # print u"公司经营类型：%s"%CComname
            # print u"职位薪酬：%s" %CCname
            print u"招聘职位：%s" %JobName
            with open("ZHILIAN.txt", 'a') as f:
                f.write(str(u"公司名称：%s" %ComName2) + '\n'+ str(u"招聘职位：%s" %JobName)+ '\n')
                f.close()










#-*- coding:utf-8 -*-
import requests
import os
from bs4 import BeautifulSoup
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
pageindx = -4
headers= {
    'User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}
# while True:
for pageindx in range(98):
    if pageindx>3956:
        break
    else:
        pageindx +=40
        url = "https://search.zbj.com/p/k"+ str(pageindx) +".html?kw=%E6%96%B0%E5%AA%92%E4%BD%93%E8%BF%90%E8%90%A5"
        r = requests.get(url, headers=headers)  # 连接
        content = r.text  # 获取内容，自动转码unicode
        soup = BeautifulSoup(content, "html.parser")
        items = soup.findAll('div',attrs ={'class':'base-info-wrap'})
        items2 = soup.findAll('span',attrs ={'class':'ico ico-user-single'})
        for item in items:
            ComName = item.find('h4').get_text()


            # print u"目前读取的页数为：%s" %pageindx
            print u"公司名称：%s" %ComName
            # print u"公司经营类型：%s"%CComname
            # print u"职位薪酬：%s" %CCname
            # print u"招聘职位：%s" %JobName
            # with open("LIEPIN.txt", 'a') as f:
            #     f.write(ComName2+ CComname+ CCname + JobName+ '\n')
            #     f.close()











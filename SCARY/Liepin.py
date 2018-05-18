# -*- coding:utf-8 -*-
import requests
import os
from bs4 import BeautifulSoup
import json
import xlrd
class LieP:
    def __init__(self):
        self.pageindex = 0
        self.headers= {
            'User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
        }
        self.stories = []
        self.enable = False
    def getpage(self,pageindex):
        url = ['https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key=%E6%96%B0%E5%AA%92%E4%BD%93%E8%BF%90%E8%90%A5&&headckid=null&d_pageSize=40&siTag=qkuPMtyyPWyGJLVm3Ykn1A~fA9rXquZc5IkJpXC-Ycixw&d_headId=9227b18f23bcc1185b13d8352df15b72&d_ckId=9227b18f23bcc1185b13d8352df15b72&d_sfrom=search_unknown&d_curPage=2&curPage={}'.format(str(i) for i in range(0,101))]
        r = requests.get(url, headers=self.headers)  # 连接
        content = r.text  # 获取内容，自动转码unicode
        soup = BeautifulSoup(content, "html.parser")
        items = soup.findAll('div',attrs ={'class':'company-info nohover'})
        for item in items:
            BASE = item.find('a').get('title')
            print u"公司名称：%s" %BASE

    # def getindex(self,pageindex):
    #     for i in range(0,100):
    #         pageindex =i
    #         pageindex +=1
    #

    # def save_excel( tag_name, file_name):  # 将抓取到的招聘信息存储到excel当中
    #     book = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\%s.xls' % file_name)  # 默认存储在桌面上
    #     tmp = book.add_worksheet()
    #     row_num = len()
    #     for i in range(1, row_num):
    #         if i == 1:
    #             tag_pos = 'A%s' % i
    #             tmp.write_row(tag_pos, tag_name)
    #         else:
    #             con_pos = 'A%s' % i
    #             content = fin_result[i - 1]  # -1是因为被表格的表头所占








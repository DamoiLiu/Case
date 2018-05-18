# #-*- coding:utf-8 -*-
# import urllib2
# import requests
# import urllib
# import re
# from bs4 import BeautifulSoup
#
# # while True:
# #     page = 0
# #     if page <101:
# #         page =page + 1
# #         print page
# #
# # url =  "https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key=%E6%96%B0%E5%AA%92%E4%BD%93%E8%BF%90%E8%90%A5&&headckid=null&d_pageSize=40&siTag=qkuPMtyyPWyGJLVm3Ykn1A~fA9rXquZc5IkJpXC-Ycixw&d_headId=9227b18f23bcc1185b13d8352df15b72&d_ckId=9227b18f23bcc1185b13d8352df15b72&d_sfrom=search_unknown&d_curPage=2&curPage=" + str(page)
# # header = {
# #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
# # }
# # try:
# #     request = urllib2.Request(url)
# #     reponse = urllib2.urlopen(request)
# #     print reponse.read()
# # except urllib2.URLError,e:
# #     if hasattr(e,'code'):
# #         print e.code
# #     if hasattr(e,'reason'):
# #         print e.reason
# # -*- coding:utf-8 -*-
# import urllib
# import urllib2
# import re
# import thread
# import time
#
#
# """
# 爬取猎聘网站的'新媒体运营'搜索关键字的总数
# """
# class QSBK:
#     # 初始化方法，定义一些变量
#     def __init__(self):
#         self.pageIndex = 0#初始化分页
#         # 初始化headers
#         self.headers = {
#             'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
#         }
#         # 存放公司名称的变量，每一个元素是每一页的总量
#         self.stories = []
#         # 存放程序是否继续运行的变量
#         self.enable = False
#
#     # 传入某一页的索引获得页面代码
#     def getPage(self, pageIndex):
#         url = 'https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key=%E6%96%B0%E5%AA%92%E4%BD%93%E8%BF%90%E8%90%A5&&headckid=null&d_pageSize=40&siTag=qkuPMtyyPWyGJLVm3Ykn1A~fA9rXquZc5IkJpXC-Ycixw&d_headId=9227b18f23bcc1185b13d8352df15b72&d_ckId=9227b18f23bcc1185b13d8352df15b72&d_sfrom=search_unknown&d_curPage=2&curPage=' + str(pageIndex)
#         # 构建请求的request
#         request = urllib2.Request(url, headers=self.headers)
#         # 利用urlopen获取页面代码
#         response = urllib2.urlopen(request)
#         soup = BeautifulSoup(response,"html.parser")
#         # 将页面转化为UTF-8编码
#         pageCode = response.read().decode('utf-8')
#         return pageCode
#
#     # 传入某一页代码，返回本页不带图片的段子列表
#     def getPageItems(self, pageIndex):
#         pageCode = self.getPage(pageIndex)
#         if not pageCode:
#             print "页面加载失败...."
#             return None
#         # 用来存储每页的段子们
#         pageStories = []
#         # 遍历正则表达式匹配的信息
#         for item in items:
#             # 是否含有图片
#             haveImg = re.search("img", item[3])
#             # 如果不含有图片，把它加入list中
#             if not haveImg:
#                 # item[0]是一个段子的发布者，item[1]是发布时间,item[2]是内容，item[4]是点赞数
#                 pageStories.append([item[0].strip(), item[1].strip(), item[2].strip(), item[4].strip()])
#         return pageStories
#
#     # 加载并提取页面的内容，加入到列表中
#     def loadPage(self):
#         # 如果当前未看的页数少于2页，则加载新一页
#         if self.enable == True:
#             if len(self.stories) < 2:
#                 # 获取新一页
#                 pageStories = self.getPageItems(self.pageIndex)
#                 # 将该页的段子存放到全局list中
#                 if pageStories:
#                     self.stories.append(pageStories)
#                     # 获取完之后页码索引加一，表示下次读取下一页
#                     self.pageIndex += 1
#
#     # 调用该方法，每次敲回车打印输出一个段子
#     def getOneStory(self, pageStories, page):
#         # 遍历一页的段子
#         for story in pageStories:
#             # 等待用户输入
#             input = raw_input()
#             # 每当输入回车一次，判断一下是否要加载新页面
#             self.loadPage()
#             # 如果输入Q则程序结束
#             if input == "Q":
#                 self.enable = False
#                 return
#             print u"第%d页\t发布人:%s\t发布时间:%s\n%s\n赞:%s\n" % (page, story[0], story[1], story[2], story[3])
#
#     # 开始方法
#     def start(self):
#         print u"正在读取糗事百科,按回车查看新段子，Q退出"
#         # 使变量为True，程序可以正常运行
#         self.enable = True
#         # 先加载一页内容
#         self.loadPage()
#         # 局部变量，控制当前读到了第几页
#         nowPage = 0
#         while self.enable:
#             if len(self.stories) > 0:
#                 # 从全局list中获取一页的段子
#                 pageStories = self.stories[0]
#                 # 当前读到的页数加一
#                 nowPage += 1
#                 # 将全局list中第一个元素删除，因为已经取出
#                 del self.stories[0]
#                 # 输出该页的段子
#                 self.getOneStory(pageStories, nowPage)
#
#
# spider = QSBK()
# spider.start()

import requests
import os
from bs4 import BeautifulSoup
import os
import sys
reload(sys)
sys.setdefaultencoding('utf8')
pageindx = 0
headers= {
    'User-Agent' :'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
}
while True:
    for pageindx in range(0,101):
        if pageindx>101:
            break
        else:
            pageindx +=1
            url = "https://www.liepin.com/zhaopin/?sfrom=click-pc_homepage-centre_searchbox-search_new&d_sfrom=search_fp&key=%E6%96%B0%E5%AA%92%E4%BD%93%E8%BF%90%E8%90%A5&&headckid=null&d_pageSize=40&siTag=qkuPMtyyPWyGJLVm3Ykn1A~fA9rXquZc5IkJpXC-Ycixw&d_headId=9227b18f23bcc1185b13d8352df15b72&d_ckId=9227b18f23bcc1185b13d8352df15b72&d_sfrom=search_unknown&d_curPage=2&curPage=" + str(pageindx)
            r = requests.get(url, headers=headers)  # 连接
            content = r.text  # 获取内容，自动转码unicode
            soup = BeautifulSoup(content, "html.parser")
            items = soup.findAll('div',attrs ={'class':'sojob-item-main clearfix'})
            for item in items:
                JobName = item.div.h3.get_text()
                CCname =item.div.p.span.get_text()
                ComName = item.selector.xpath()
                print u"目前读取的页数为：%s" %pageindx
                print u"公司名称：%s" %ComName
                print u"公司经营类型：%s" %CCname
                print u"招聘职位：%s" %JobName.strip()
                # with open("LIEPIN.txt", 'a') as f:
                #     f.write(ComName + '\n')
                #     f.close()










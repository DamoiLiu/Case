# -*- coding:utf-8 -*-
import sys
import urllib2
import os
from bs4 import BeautifulSoup
import requests
import re
import urllib
import time
"""
爬虫需求：
1.爬下来这些图片保存在一个文件夹里面
2.爬下每张图片的标题，以及图片的分类
"""


class CnblogsUtils(object):
    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36",
            "Connection":"keep - alive",
            "Content - Type": "text / html;charset = UTF - 8",
        }
    def GetPage(self,url=None):  # 抓取页面信息
        Res = urllib2.Request(url, headers=self.headers)
        mypage = urllib2.urlopen(Res)
        soup = BeautifulSoup(mypage.read(),'html.parser',from_encoding='utf-8')
        return soup

    def PageIdx(self,url=None,pageNo=None):  # 爬去每个分页的图片
        soup = self.GetPage(url+pageNo)
        itemImg = soup.findAll('div', attrs={"class": "div_img_with_title"})
        Img =CnblogsUtils()
        print ("----This is",pageNo,"page----")
        for i,Imginfo in enumerate(itemImg):
            Img.num = i
            Img.url = Imginfo.find("img").get("src")

            print (Img.url)
    def saveImg(self,url=None):
        filename = "D:\ImgText"
        if os.path.exists(filename):
            print ("The file is already exists")
        else:
            os.mkdir(filename)
        filesavepath = urllib.urlretrieve(self.PageIdx(),filename)
        print filesavepath

if __name__ == '__main__':
    url= "http://sudasuta.com/page/"
    PP =CnblogsUtils()
    for i in range(1,487):
        PP.PageIdx(url,str(i+1))
        time.sleep(3)
    print PP.saveImg()



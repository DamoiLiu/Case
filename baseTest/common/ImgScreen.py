#-*- coding:utf-8 -*-
from PIL import  Image
from selenium import webdriver
from config.Readerconfig import Dat
import os
from Log.Comlog import Log
log = Log()
def Save_img():
    Img_path = os.getcwd() + "/Image_File"
    if not os.path.exists(Img_path):
        log.info("你所寻找的文件夹不存在，正在创建文件当中....文件创建成功")
        os.mkdir(Img_path)
    else:
        log.info("文件夹已经存在")
    browser = webdriver.Chrome()
    browser.set_window_size(1200, 900)
    browser.get(Dat)
    try:
        browser.save_screenshot(Img_path + "//Webpage.png")
        browser.close()
        log.info("正在截图...截图成功保存")
    except:
        log.exception("截图失败，请检查文件夹以及webpage")


def crop_img(self):
    img = Image.open()
    Raco = (100, 200, 300, 400)
    CorpImg = img.crop(Raco)
    CorpImg.save("")



if __name__ == '__main__':
    print Save_img()




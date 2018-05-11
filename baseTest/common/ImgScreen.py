#-*- coding:utf-8 -*-
from PIL import  Image
from selenium import webdriver
from config.Readerconfig import Dat
from common.page.base_page import BasePaeg
import os
from Log.Comlog import Log
log = Log()
import time
class Save:
    def __init__(self,driver):
        self.driver = driver
    def save_screen_shot(self):
        Dtime = time.strftime('%Y%m%d',time.localtime(time.time()))
        Img_path = os.getcwd() + "\Image_File_%s" %Dtime
        if not os.path.exists(Img_path):
            log.info("你所寻找的文件夹不存在，正在创建文件当中....文件创建成功")
            os.mkdir(Img_path)
        else:
            log.info("文件夹已经存在")
        save_name = Img_path + ".png"
        self.driver.get_screenshot_as_file(save_name)
        time.sleep(3)
        self.save_screen_shot()





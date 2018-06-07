#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import  uiautomator
from uiautomator import Device
import os
import time


#基类，渠道脚本的公共方法
class baseChannel:
    def __init__( self):
        self.pkgName=None
        self.loginSuccess=None
        self.jf_loginSuccess = None
        self.oderSuccess = None
        self.device=None
        self.sizeX=None
        self.sizeY = None
        self.displayRotation = None
        self.nrow=None

    def setParam(self,pkgName,nrow,device):
        self.pkgName = pkgName
        self.device = device
        self.nrow = nrow

    #x,y为使用调试模式获取的坐标位置，phoneX,phoneY为当前调试手机去除虚拟按键后的宽、高(注意横屏和竖屏）
    def clickPoint(self,x,y,phoneX,phoneY):
        if self.sizeX==None or self.sizeY==None or self.displayRotation==None:
            phoneInfo= self.device.info
            print phoneInfo
            self.displayRotation=phoneInfo['displayRotation']
            self.sizeX=phoneInfo['displayWidth']
            self.sizeY=phoneInfo['displayHeight']
            # 根据手机调试模式获取的像素点坐标计算真实的点击位置，需要减去屏幕下方虚拟按键的位置。
        if phoneY>phoneX and self.displayRotation == 1:  # 横屏
            print u'屏幕分辨率输入错误，横屏状态x为宽，y为高'
        clickX = int(self.sizeX * x / phoneX)
        clickY = int(self.sizeY * y / phoneY)
        self.device.click(clickX, clickY)
        return self

    #必须使用Utf7Ime输入法才能调用该方法
    def clickPointInput(self,text):
        cmd='adb shell am broadcast -a ADB_INPUT_CODE --ei code 67 --ei repeat 20'
        p = os.popen(cmd)
        time.sleep(1)
        cmdInput=r"adb shell am broadcast -a ADB_INPUT_TEXT --es msg "  +text
        p = os.popen(cmdInput)

    #截图方法
    def printscreen(self,pngName):
        try:
            self.device.screenshot("./oderRecord/"+pngName+".png")
        except:
            print u'uiautomator截屏失效'
            cmd1 = 'adb shell screencap -p /data/local/tmp/'+ pngName +'.png'
            cmd2 = 'adb pull /data/local/tmp/'+ pngName +'.png ./oderRecord/'
            cmd3 = 'adb shell rm /data/local/tmp/'+ pngName +'.png'
            os.popen(cmd1)
            os.popen(cmd2)
            os.popen(cmd3)

    #获取屏幕参数
    def GetDisplay(self):
        if self.displayRotation==None:
            phoneInfo= self.device.info
            self.displayRotation=phoneInfo['displayRotation']


    # 登陆脚本
    def Login(self):
        pass

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self, canRun=False):
        pass

    # 支付脚本
    def PayOder(self, canRun=False):
       pass

    # 执行脚本，step用于单个步骤调试，方便定位错误
    def Run(self, step=0):
        if step == 0:
            self.Login()
            self.GetDisplay()
            self.Jf_login()
            self.PayOder()
        elif step == 1:  # 登陆
            self.Login()
        elif step == 2:  # 计费登陆
            self.Jf_login(True)
        elif step == 3:  # 支付
            self.PayOder(True)

# bilibili渠道
class bilibili(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(5)
                    if not self.device(resourceId=self.pkgName + ":id/bsgamesdk_login_main").exists:
                        self.device(text="Login").click()
                        time.sleep(1)
                        self.device(text="确定").click()
                        time.sleep(5)

                    print u'开始输入账号密码'
                    self.device(resourceId=self.pkgName + ":id/bsgamesdk_edit_username_login").click()
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/bsgamesdk_edit_username_login").set_text('13430352187')
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/bsgamesdk_edit_password_login").set_text('78451245')
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/bsgamesdk_buttonLogin").click()
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    # 支付脚本
    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="UpLoadUserInfo").click()
                    time.sleep(1)
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:
                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

# coolpad渠道
class coolpad(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(1)
                    self.device(text="Login").click()
                    time.sleep(1)
                    self.device(text="确定").click()
                    time.sleep(5)

                    print u'开始输入账号密码'
                    self.device(text="请输入手机号/邮箱").click()
                    time.sleep(1)
                    self.device(text="请输入手机号/邮箱").set_text('15820100116')
                    time.sleep(1)
                    self.clickPoint(1066, 915, 1920, 1080).clickPointInput('3312939')
                    # self.device(resourceId=self.pkgName + ":id/bsgamesdk_edit_password_login").set_text('78451245')
                    time.sleep(1)
                    self.device(scrollable=True).scroll.vert.forward()
                    time.sleep(1)
                    self.device(text="登   录").click()
                    time.sleep(8)  # 酷派有个自动登陆授权页面需要等待

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    self.device(scrollable=True).scroll.vert.forward()  # 横屏需要两次才能到底
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()  # 同样需要两次
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    self.device(scrollable=True).scroll.vert.forward()  # 横屏需要两次
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()  # 横屏需要两次
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    # 支付脚本
    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    # self.device(text="UpLoadUserInfo").click()
                    # time.sleep(1)
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    self.device.press.back()
                    # if self.device(text=r"交易尚未完成，确定放弃？").exists:
                    #    self.device(text="确定").click()
                    #    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:
                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

#银汉游戏
class yinhan(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    #登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(1)
                    if not self.device(text="请填写手机号/账号").exists:
                        self.device(text="Login").click()
                        time.sleep(1)
                        self.device(text="确定").click()
                        time.sleep(5)

                    print u'开始输入账号密码'
                    self.device(text="请填写手机号/账号").click()
                    time.sleep(1)
                    self.device(text="请填写手机号/账号").set_text('15820100116')
                    time.sleep(1)
                    self.clickPoint(1020,415,1920,1080).clickPointInput('3312939')
                    #self.device(resourceId=self.pkgName + ":id/bsgamesdk_edit_password_login").set_text('78451245')
                    time.sleep(1)
                    self.device(text="登        录").click()
                    time.sleep(2)#酷派有个自动登陆授权页面需要等待

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    self.device(scrollable=True).scroll.vert.forward()#横屏需要两次才能到底
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()#同样需要两次
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess=True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    self.device(scrollable=True).scroll.vert.forward()#横屏需要两次
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()#横屏需要两次
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess=True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess=False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess=False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    #支付脚本
    def PayOder(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.jf_loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    #self.device(text="UpLoadUserInfo").click()
                    #time.sleep(1)
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    self.clickPoint(1730,80,1794,1080)
                    #if self.device(text=r"交易尚未完成，确定放弃？").exists:
                    #    self.device(text="确定").click()
                    #    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:
                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

#豌豆荚
class wandoujia(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    #登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(5)
                    if not self.device(resourceId= "com.wandoujia.mariosdk.plugin.apk:id/account_login").exists:
                        self.device(text="Login").click()
                        time.sleep(1)
                        self.device(text="确定").click()
                        time.sleep(5)

                    print u'开始输入账号密码'
                    self.device(resourceId= "com.wandoujia.mariosdk.plugin.apk:id/account_login").click()
                    time.sleep(1)
                    print self.pkgName + ":id/account_username"
                    self.device(resourceId="com.wandoujia.mariosdk.plugin.apk:id/account_username").set_text('15820100116')
                    time.sleep(1)
                    self.device(resourceId= "com.wandoujia.mariosdk.plugin.apk:id/account_password").set_text('3312939')
                    time.sleep(1)
                    self.device(resourceId= "com.wandoujia.mariosdk.plugin.apk:id/account_login").click()
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess=True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"允许").click(text=r"允许")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess=True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess=False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess=False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    #支付脚本
    def PayOder(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.jf_loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    self.device(resourceId="com.wandoujia.mariosdk.plugin.apk:id/close").click()
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:
                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

#优酷渠道
class youku(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    #登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(5)
                    if not self.device(resourceId=self.pkgName + ":id/btn_other_login").exists:
                        self.device(text="Login").click()
                        time.sleep(1)
                        self.device(text="确定").click()
                        time.sleep(5)

                    print u'开始输入账号密码'
                    self.device(resourceId=self.pkgName + ":id/btn_other_login").click()
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/yk_witherr_edit").set_text('13430352187')
                    time.sleep(1)
                    self.clickPoint(700,900,1080,1920).clickPointInput('j0h14n')
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/btn_login").click()
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess=True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess=True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess=False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess=False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    #支付脚本
    def PayOder(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.jf_loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ':id/yk_pay_icon_back').click()
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:
                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

#网易渠道
class netease(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    #登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(3)
                    if not self.device(resourceId=self.pkgName + ":id/netease_mpay__login_channel_icon").exists:
                        self.device(text="Login").click()
                        time.sleep(1)
                        self.device(text="确定").click()
                        time.sleep(5)

                    print u'开始输入账号密码'
                    #self.device( resourceId=self.pkgName + ":id/netease_mpay__login_channel_icon").click()
                    self.clickPoint(336,1150,1080,1920)
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/netease_mpay__login_urs").set_text('lwk9009@163.com')
                    time.sleep(2)
                    print "111111111"
                    self.device(resourceId=self.pkgName + ":id/netease_mpay__login_login").click()
                    self.clickPoint(710,1291,1080,1920)
                    time.sleep(2)
                    self.device(resourceId=self.pkgName + ":id/netease_mpay__login_password").set_text('19932312300')
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/netease_mpay__login_login").click()
                    time.sleep(1)
                    self.device(resourceId = self.pkgName + ":id/netease_mpay__alert_positive").click()
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/netease_mpay__alert_positive").click()
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/netease_mpay__alert_positive").click()

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    #self.device(scrollable=True).scroll.vert.forward()
                    self.device(scrollable=True).scroll.vert.forward()#横屏3次
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    #self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()#横屏3次
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess=True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(resourceId=self.pkgName + ":id/netease_mpay__alert_positive").click(text=r"确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    time.sleep(1)
                    self.device(resourceId = self.pkgName + ":id/netease_mpay__alert_positive").click()
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/netease_mpay__alert_positive").click()
                    time.sleep(1)
                    self.device(scrollable=True).scroll.vert.forward()
                    #self.device(scrollable=True).scroll.vert.forward()
                    self.device(scrollable=True).scroll.vert.forward()  # 横屏两次
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    #self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess=True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess=False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess=False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    #支付脚本
    def PayOder(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.jf_loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:
                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

#vivo渠道
class vivo(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    #登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(1)
                    if not self.device(resourceId=self.pkgName + ":id/register_onekey_layout").exists:
                        self.device(text="Login").click()
                        time.sleep(1)
                        self.device(text="确定").click()
                        time.sleep(2)
                    if not self.device(resourceId=self.pkgName + ':id/vivo_upgrade_cancel').exists:
                        print u'开始输入账号密码'
                        self.clickPoint(670, 840, 1080, 1920).clickPointInput('15820100116')
                        time.sleep(1)
                        self.clickPoint(600, 1000, 1080, 1920).clickPointInput('3312939')
                        time.sleep(1)
                        self.clickPoint(555, 1200, 1080, 1920)
                        time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()

                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess=True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()

                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']

                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess=True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess=False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess=False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    #支付脚本
    def PayOder(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.jf_loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    self.device.press.back()
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:
                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

class xunlei(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(5)

                    print u'开始输入账号密码'
                    #self.device(resourceId=self.pkgName + ":id/edit_text_user_name").click()
                    #time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/edit_text_user_name").set_text('lwk9003')
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/edit_text_user_pwd").set_text('3312939')
                    time.sleep(1)
                    #self.clickPoint(510,500,1080,1920).clickPointInput('3312939')
                    #time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/layout_login").click()
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

            # 只用来验证计费是否登陆成功，不做其它操作

    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    # 支付脚本
    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    self.device.press.back()
                    if self.device(text=r"交易尚未完成，确定放弃？").exists:
                        self.device(text="确定").click()
                        time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:

                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确认")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

class kugou_sdk(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(5)
                    print u'开始输入账号密码'
                    #self.device(resourceId=self.pkgName + ":id/edit_text_user_name").click()
                    #time.sleep(1)



                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

            # 只用来验证计费是否登陆成功，不做其它操作

    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

            # 支付脚本

    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    self.device.press.back()
                    if self.device(text=r"交易尚未完成，确定放弃？").exists:
                        self.device(text="确定").click()
                        time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:

                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确认")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

class huawei(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    time.sleep(2)
                    #=========================测试操作开始======================
                   # if not self.device(resourceId="com.wandoujia.mariosdk.plugin.apk:id/account_login").exists:
                   #     self.device(text="Login").click()
                    #    time.sleep(1)
                    #    self.device(text="确定").click()
                    #    time.sleep(2)
                    print "登录测试开始"
                    self.device(text="手机号/邮件地址").click()
                    time.sleep(1)
                    #print 11111
                    self.device(text="手机号/邮件地址").set_text("15820100116")
                    time.sleep(1)
                    self.clickPoint(535,1120,1080,1920).clickPointInput("3312939")
                    #time.sleep(1)
                    #self.device(resouceID=self.pkgName + ":id/input_password").set_text("3312939")
                    #time.sleep(1)
                    #self.device(resourceID=self.pkgName +":id/btn_login").click()

                    time.sleep(5)
                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)

        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

            # 只用来验证计费是否登陆成功，不做其它操作

    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

            # 支付脚本

    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="UpLoadUserInfo").click()
                    time.sleep(1)
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:

                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"是否要放弃本次支付？").click(text=r"确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

class pptv(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    #登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(5)
                    #if not self.device(resourceId=self.pkgName + ":id/bsgamesdk_login_main").exists:
                     #   self.device(text="Login").click()
                      #  time.sleep(1)
                       # self.device(text="确定").click()
                        #time.sleep(5)
                    #print 2222222



                    print u'开始输入账号密码'
                    self.clickPoint(795,1838,1080,1920)
                    self.device(text="PP账号/手机账号").click()
                    time.sleep(1)
                    self.device(text="PP账号/手机账号").set_text('lwk9008')
                    time.sleep(1)
                    self.clickPoint(650,800,1080,1920).clickPointInput('3312939')
                    #self.device(resourceId=self.pkgName + ":id/pptvvas_edt").set_text('3312939')
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/pptvvas_login").click()
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess=True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess=True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess=False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess=False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    #支付脚本
    def PayOder(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.jf_loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="UpLoadUserInfo").click()
                    time.sleep(1)
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:

                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确认")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

class muzhiwan(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    #登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(5)
                    #if not self.device(resourceId=self.pkgName + ":id/bsgamesdk_login_main").exists:
                     #   self.device(text="Login").click()
                     #   time.sleep(1)
                     #   self.device(text="确定").click()
                     #   time.sleep(5)

                    print u'开始输入账号密码'
                    #self.clickPoint(455,455,1080,1920).clear()
                    self.clickPoint(486, 846, 1080, 1920).clickPointInput('15820100116')
                    time.sleep(1)
                    self.clickPoint(480,980,1080,1920).clickPointInput('3312939')
                    self.device(text="立即登录").click()
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess=True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess=True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess=False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess=False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    #支付脚本
    def PayOder(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.jf_loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:

                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，是否确认退出？").click(text=r"确认退出")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

#联想渠道
class lenovo_open(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)


    #登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    time.sleep(5)
                    if not self.device(resourceId=self.pkgName + ":id/bsgamesdk_login_main").exists:
                        self.device(text="Login").click()
                        time.sleep(1)
                        self.device(text="确定").click()
                        time.sleep(3)

                    print u'开始输入账号密码'
                    self.device(resourceId=self.pkgName + ":id/at_account").click()
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/at_account").set_text('15820100116')
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/et_password").set_text('3312939')
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/b_login").click()
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess=True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess=True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess=False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess=False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    #支付脚本
    def PayOder(self,canRun=False):
        #检查是否可以执行脚本
        if canRun==False:
            canRun=self.jf_loginSuccess
        if canRun==False or canRun==None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:

                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"确定放弃本次支付？").click(text="确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

#益玩渠道
class iaround(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="稍后更新").click()
                    time.sleep(5)

                    print u'开始输入账号密码'
                    self.device(text="登录成功").click()
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

            # 只用来验证计费是否登陆成功，不做其它操作

    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

            # 支付脚本

    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="UpLoadUserInfo").click()
                    time.sleep(1)
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:

                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"确定放弃本次支付？").click(text="确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False


#海马玩渠道
class droid4x(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    time.sleep(5)

                    print u'开始输入账号密码'
                    self.clickPoint(940,260,1920,1080)
                    time.sleep(1)
                    self.clickPoint(780,169,1920,1080).clickPointInput("15820100116")
                    time.sleep(1)
                    self.clickPoint(952,415,1920,1080).clickPointInput("3312939")
                    time.sleep(1)
                    self.clickPoint(750,690,1920,1080)
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

            # 只用来验证计费是否登陆成功，不做其它操作

    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    # 支付脚本
    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:

                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"确定放弃本次支付？").click(text="确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

#百度渠道
class baidu(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始输入账号密码'
                    time.sleep(5)
                    if not self.device(resourceId=self.pkgName + ":id/bsgamesdk_login_main").exists:
                        self.device(text="Login").click()
                        time.sleep(1)
                        self.device(text="确定").click()
                        time.sleep(3)
                    #self.clickPoint(520, 655, 1080.1920)
                    #self.clickPoint(520,655,1080.1920).clickPointInput("15820100116")
                    self.device(resourceId=self.pkgName + ":id/edtAccount").set_text('15820100116')
                    time.sleep(1)
                    #self.device(resourceId=self.pkgName + ":id/edtAccount").set_text('LWK3312939')
                    self.clickPoint(548,730,1080,1920).clickPointInput("LWK3312939")
                    time.sleep(1)
                    self.device(resourceId=self.pkgName + ":id/btnLogin").click()
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

            # 支付脚本

    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="UpLoadUserInfo").click()
                    time.sleep(1)
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:

                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"确定放弃本次支付？").click(text="确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

#4399渠道
class _4399com(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    time.sleep(5)

                    print u'开始输入账号密码'
                    self.clickPoint(450, 300, 1080, 1920).clickPointInput('lwk9003')
                    time.sleep(1)
                    self.clickPoint(450, 460, 1080, 1920).clickPointInput('3312939')
                    time.sleep(1)
                    self.clickPoint(500,650,1080,1920)
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

            # 只用来验证计费是否登陆成功，不做其它操作

    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    # 支付脚本
    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:
                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"确定放弃本次支付？").click(text="确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

class _49you(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    time.sleep(5)
                    if not self.device(resourceId=self.pkgName + ":id/bsgamesdk_login_main").exists:
                        self.device(text="Login").click()
                        time.sleep(1)
                        self.device(text="确定").click()
                        time.sleep(3)

                    print u'开始输入账号密码'
                    #self.device(resourceId=self.pkgName + ":id/at_account").click()
                    #time.sleep(1)
                    #self.device(resourceId=self.pkgName + ":id/at_account").set_text('15820100116')
                    #time.sleep(1)
                    #self.device(resourceId=self.pkgName + ":id/et_password").set_text('3312939')
                    #time.sleep(1)
                    self.device(text="快速登陆").click()
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

            # 只用来验证计费是否登陆成功，不做其它操作

    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    # 支付脚本
    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="UpLoadUserInfo").click()
                    time.sleep(1)
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:
                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"确定放弃本次支付？").click(text="确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

# 360渠道
class _360_ass(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(3)
                    if not self.device(text="360帐号登录").exists:
                        self.device(text="Login").click()
                        time.sleep(1)
                        self.device(text="确定").click()
                        time.sleep(5)

                    print u'开始输入账号密码'
                    self.device(text= "用户名/手机号/邮箱").set_text('lwk9003')
                    time.sleep(1)
                    self.clickPoint(650, 850, 1080,1920).clickPointInput("3312939")
                    time.sleep(1)
                    self.device(text= "立即登录").click()
                    time.sleep(2)
                    self.device.press.back()
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    time.sleep(1)
                    self.device(text="JF login").click()
                    time.sleep(1)
                    self.device(scrollable=True).scroll.vert.forward()
                    time.sleep(1)
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    time.sleep(1)
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    # 支付脚本
    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:
                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

# uc渠道
class uc_platform(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(8)
                    self.device(text="Login").click()
                    time.sleep(1)
                    self.device(text="确定").click()
                    time.sleep(1)

                    print u'开始输入账号密码'
                    self.clickPoint(160, 1285, 1080, 1920)
                    time.sleep(2)
                    if self.device(resourceId="cn.uc.gamesdk.account:id/layout_platformswitcher_shunk").exists:
                        self.device(resourceId="cn.uc.gamesdk.account:id/layout_platformswitcher_shunk").click()
                    time.sleep(2)
                    self.clickPoint(160,1285,1080,1920)
                    time.sleep(1)
                    #self.device(resourceId=self.pkgName + ":id/et_login_account").set_text('15820100116')
                    self.clickPoint(573,816,1080,1920).clickPointInput('966414499')
                    time.sleep(1)
                    self.clickPoint(550, 965, 1080, 1920).clickPointInput('3312939')
                    #self.device(resourceId=self.pkgName + ":id/et_login_smscode").set_text('3312939')
                    time.sleep(1)
                    self.clickPoint(540, 1150, 1080, 1920)
                    time.sleep(1)

                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    # 支付脚本
    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================

                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:
                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False

# 新浪渠道
class sina_sdk(baseChannel):
    def __init__(self):
        baseChannel.__init__(self)

    # 登陆脚本
    def Login(self):
        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()

                    # ======================测试操作开始===========================
                    time.sleep(8)
                    self.device(text="logout").click()
                    time.sleep(1)
                    self.device(text="Login").click()
                    time.sleep(1)
                    self.device(text="确定").click()
                    time.sleep(1)

                    print u'开始输入账号密码'
                    self.clickPoint(310, 1280, 1080, 1920)
                    time.sleep(3)


                    print u'验证登陆结果'
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    time.sleep(1)
                    # ======================测试操作结束===========================

                    if logText.find(r'LOGIN_SUCCESS') != -1:
                        self.loginSuccess = True
                        print u'登陆成功'
                    else:
                        print u'登陆失败'
                        self.loginSuccess = False
                    break
                except:
                    if trycount >= 3:
                        print u'登陆异常'
                        self.loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("1").when(text=r"输入登陆渠道，只有一个登陆渠道，可以直接确定").click(text=r"确定")
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
                    self.device(text="logout").click()
        except:
            print u'登陆脚本异常'
            self.loginSuccess = False

    # 只用来验证计费是否登陆成功，不做其它操作
    def Jf_login(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================
                    print u'开始计费登陆'
                    self.device(text="JF login").click()
                    self.device(scrollable=True).scroll.vert.forward()
                    logText = self.device(resourceId=self.pkgName + ":id/SdkMsg").info['text']
                    self.device(scrollable=True).scroll.vert.backward()
                    # ======================测试操作结束===========================

                    if logText.find(r'JF_LOGIN_SUCCESS') != -1:
                        print u'计费登陆成功'
                        self.jf_loginSuccess = True
                    else:
                        print u'计费登陆失败'
                        self.jf_loginSuccess = False

                    break
                except:
                    if trycount >= 3:
                        print u'支付登陆异常'
                        self.jf_loginSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'计费登陆脚本异常'
            self.jf_loginSuccess = False

    # 支付脚本
    def PayOder(self, canRun=False):
        # 检查是否可以执行脚本
        if canRun == False:
            canRun = self.jf_loginSuccess
        if canRun == False or canRun == None:
            return

        trycount = 0
        try:
            while True:
                try:
                    trycount += 1
                    self.device.watchers.remove()
                    # ======================测试操作开始===========================

                    self.device(text="Order").click()
                    time.sleep(5)
                    self.printscreen(self.pkgName)
                    time.sleep(1)
                    # ======================测试操作结束===========================
                    print u'支付打开成功'
                    self.oderSuccess = True
                    break

                except:
                    if trycount >= 3:
                        print u'支付异常'
                        self.oderSuccess = False
                        break
                    self.device.press.back()
                    time.sleep(1)
                    self.device.press.back()
                    self.device.watcher("2").when(text=r"退出游戏？").click(text=r"取消")
                    self.device.watcher("3").when(text=r"交易尚未完成，确定放弃？").click(text=r"确定")
                    self.device.watchers.run()
                    self.device(scrollable=True).scroll.vert.backward()
        except:
            print u'支付脚本异常'
            self.oderSuccess = False




if __name__ == '__main__':
    pass
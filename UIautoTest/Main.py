#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import Queue
from xlutils.copy import copy
import os
import xlrd
import re
import time
from uiautomator import Device
import shutil
import channel

XLS_DIR = r'./'
XLS_FILENAME = r'test_plan.xls'
XlS_OUT=r'test_out.xls'


class startTestPlan:
    def __init__(self):
        self.testList=Queue.Queue()
        self._workQueue = Queue.Queue()
        self.device=None
        self.result=Queue.Queue()
        self.sizeX=None
        self.sizeY=None
        self.displayRotation = None
        self.clearPicture()

    #使用前先清除文件夹中的截图
    def clearPicture(self):
        if not os.path.exists(os.getcwd() + "/oderRecord"):
            os.makedirs(os.getcwd() + "/oderRecord")
            return
        else:
            try:
                shutil.rmtree(os.getcwd() + "/oderRecord")
                os.makedirs(os.getcwd() + "/oderRecord")
            except:
                print u'截图清除失败！'

    #安装测试脚本使用的输入法
    def installInputMethod(self):
        apkPath=r'./android_unicode_ime-debug.apk'
        if not os.path.exists(apkPath):
            print u'InstallMethod apk not exist!'
            return
        cmd=r'adb install '+apkPath
        p=os.popen(cmd)
        aaa=p.read()
        print aaa
        cmd = r'adb shell ime enable android.unicode.ime/.Utf7ImeService'
        p = os.popen(cmd)
        print p.read()
        cmd = r'adb shell ime set android.unicode.ime/.Utf7ImeService'
        p = os.popen(cmd)
        print p.read()

    #卸载测试脚本使用的输入法
    def uninstallIputMethod(self):
        cmd = r'adb shell ime disable android.unicode.ime/.Utf7ImeService'
        p = os.popen(cmd)
        apkPath = r'./android_unicode_ime-debug.apk'
        cmd = r'aapt.exe dump badging ' + apkPath
        p = os.popen(cmd)
        cmdText = p.read()
        pkgName = re.findall(r"package: name='(.*?)'", cmdText)
        cmd = r'adb uninstall ' + pkgName[0]
        p = os.popen(cmd)

    #存储测试结果
    def _getResult(self,canLogin,canJFlogin,canOder,displayRotation,nrow):
        data=[canLogin,canJFlogin,canOder,displayRotation,nrow]
        self.result.put(data)

    def readExcel( self,dir_path, xls_name):
        filename = dir_path + xls_name
        if os.path.exists(filename):
            data = xlrd.open_workbook(filename)
            table = data.sheets()[0]
            nrows = table.nrows#行数
            for i in range(nrows):#按行读取表格
                if i == 0: continue#第一行不读取
                channelName=None
                channeldate = {}.fromkeys(['nrow', 'channelName'])
                channeldate['nrow'] = i
                for (j, key_value) in enumerate(table.row_values(i)):
                    #print "the %s :%s" % (j, key_value)
                    if j == 1 and len(key_value) is not 0:channeldate['channelName'] = key_value
                    if j == 2 and len(key_value) is not 0:
                        if key_value.lower().find("t")!=-1 and channeldate['channelName']!=None:
                            self.testList.put(channeldate)
            #print self._testList

    # 获取测试结果队列，并写入Excel表格
    def writeExcel(self, dir_path, xls_name, xls_out, data):
        if data.empty():
            return
        filename = dir_path + xls_name
        fileOut = dir_path + xls_out
        if not os.path.exists(filename):
            print u'测试文件不存在'
            return
        r_xls = xlrd.open_workbook(filename)
        w_xls = copy(r_xls)
        sheet_write = w_xls.get_sheet(0)
        try:
            if not data.empty():
                while not data.empty():
                    result = data.get_nowait()
                    row = int(result[4])
                    sheet_write.write(row, 3, result[0])  # 写入登陆测试结果
                    sheet_write.write(row, 4, result[1])  # 写入计费登陆测试结果
                    sheet_write.write(row, 5, result[2])  # 写入支付页面测试结果
                    sheet_write.write(row, 6, result[3])  # 写入应用横竖状态
                w_xls.save(fileOut)
        except:
            print u'第%s行，结果写入失败' % row

    #获取安装包信息
    def getApkInfo(self,name):
        apkName=''
        filePath=os.getcwd() + "/apk"
        if not os.path.exists(filePath):
            os.makedirs(filePath)
        dirs = os.listdir(filePath)
        if len(dirs) < 1:
            print u"文件夹为空\n"
            return
        for apk in dirs:
            if name in apk:
                apkName= apk
                print u'正在安装渠道%s：%s' %(name.encode("utf-8"),apkName)
                break

        apkPath = os.getcwd() + "/apk/"+apkName
        if not os.path.exists(apkPath):
            print u'%s apk not exist!' %apkName
            return None,None,None
        cmd = r'aapt.exe dump badging ' + apkPath
        p = os.popen(cmd)
        cmdText = p.read()
        pkgName = re.findall(r"package: name='(.*?)'", cmdText)
        mainActivity = re.findall(r"launchable-activity: name='(.*?)'", cmdText)
        if len(pkgName) and len(mainActivity):
            return pkgName[0], mainActivity[0],apkPath
        else:
            return None,None,None

    # 使用adb的方式找到连接的手机设备
    def finddevices(self):
        p = os.popen("adb devices")
        devices = re.findall(r'(.*?)\s+device', p.read())
        if len(devices) > 1:
            deviceIds = devices[1:]
            print u'共找到%s个手机' % str(len(devices) - 1)
            for i in deviceIds:
                print u'ID为%s' % i
            return deviceIds
        else:
            print u'没有找到手机，请检查'
            return []

    #安装apk
    def installAPK(self,path,pkgName):
        if path is None or pkgName is None:
            return
        apkPath=path
        if not os.path.exists(apkPath):
            print u'Apk not exist!'
            return
        cmd=r'adb install '+apkPath
        p=os.popen(cmd)
        if re.findall(r'Failure',p.read()):
            cmd = r'adb uninstall ' + pkgName
            p = os.popen(cmd)
            time.sleep(2)
            cmd = r'adb install ' + apkPath
            p = os.popen(cmd)

    #卸载apk
    def uninstallAPK(self,pkgname):
        if pkgname is None:
            return
        pkgName = pkgname
        cmd = r'adb uninstall ' + pkgName
        p = os.popen(cmd)
        if re.findall(r'Failure', p.read()):
            return False
        else:
            return True

    #打开apk
    def openAPK(self,pkgName, mainActivity):
        if pkgName == None or mainActivity == None:
            print u"can not get the apk info!"
            return None
        cmd = r'adb shell am start -n ' + pkgName + r'/' + mainActivity

        try:
            p = os.popen(cmd)
            cmdText = p.read()
            print cmdText
        except:
            print u'fail to  open the apk!'

    def runTheTest(self):
        while True:
            try:
                task = self._workQueue.get(False)
                testPlan.installAPK(task['apkPath'], task['pkgName'])
                testPlan.openAPK(task['pkgName'], task['mainActivity'])
                time.sleep(3)  # 等待闪屏
                task['instance'].Run()
                #task['instance'].Run(1)#登陆
                #task['instance'].Run(2)#计费登陆
                #task['instance'].Run(3)#支付
                #测试结果存入队列
                self._getResult(task['instance'].loginSuccess,task['instance'].jf_loginSuccess,task['instance'].oderSuccess,task['instance'].displayRotation,task['instance'].nrow)
                self.device.press.home()
                testPlan.uninstallAPK(task['pkgName'])
            except Queue.Empty:
                break
            except:
                print u"running fail!"

    #生成测试类
    def genWork(self):
        if self.testList.empty():
            return
        if self.device is None:
            return
        while True:
            try:
                task = {}.fromkeys(['instance','pkgName','mainActivity','apkPath'])
                channeldate = self.testList.get(False)
                pkgName, mainActivity, apkPath = testPlan.getApkInfo(channeldate['channelName'])
                task['pkgName']=pkgName
                task['mainActivity'] = mainActivity
                task['apkPath'] = apkPath
                testClass='channel.'+channeldate['channelName']+'()'#拼接类名
                taskInstance=eval(testClass)#实例化接口测试类
                taskInstance.setParam(pkgName,channeldate['nrow'],self.device)#记录测试渠道在excel中相应的行数
                task['instance']=taskInstance
                self._workQueue.put(task)#存入队列
            except Queue.Empty:
                break
            except:
                print u" Instantiation errors!"

    def clickPoint(self,x,y,phoneX,phoneY):
        if self.sizeX==None or self.sizeY==None or self.displayHeight==None:
            phoneInfo= self.device.info
            print phoneInfo
            self.displayRotation=phoneInfo['displayRotation']
            self.sizeX=phoneInfo['displayWidth']
            self.sizeY=phoneInfo['displayHeight']
            # 根据手机调试模式获取的像素点坐标计算真实的点击位置，需要减去屏幕下方虚拟按键的位置。
        if phoneY>phoneX and self.displayRotation == 1:  # 横屏
         clickX = int(self.sizeX * x / phoneX)
        clickY = int(self.sizeY * y / phoneY)
        self.device.click(clickX, clickY)
        return self

    #必须使用Utf7Ime输入法才能调用该方法
    def clickPointInput(self,text):
        cmd='adb shell am broadcast -a ADB_INPUT_CODE --ei code 67 --ei repeat 20'
        p = os.popen(cmd)
        time.sleep(1)
        cmdInput=r"adb shell am broadcast -a ADB_INPUT_TEXT --es msg " + text
        p = os.popen(cmdInput)


if __name__ == '__main__':
    testPlan=startTestPlan()
    testPlan.installInputMethod()#安装测试脚本使用的输入法
    testPlan.readExcel(XLS_DIR,XLS_FILENAME)#读取需要测试的渠道
    deviceIds =testPlan.finddevices()#获取设备ID
    if len(deviceIds):
        print u'将对ID为%s的手机进行操作...' % deviceIds[0]
        testPlan.device=Device(deviceIds[0])
        #testPlan.clickPoint(1730,80,1794,1080)
        testPlan.genWork()#实例化渠道测试脚本
        testPlan.runTheTest()
        testPlan.writeExcel(XLS_DIR,XLS_FILENAME,XlS_OUT,testPlan.result)#测试结果输出到excel
    testPlan.uninstallIputMethod()#卸载测试输入法

# -*-coding:utf-8 -*-
from common.page.base_page import BasePaeg
class Login(BasePaeg):
    input_loginbt = 'xpath=> /html/body/div[1]/div/div[1]/div/a[1]'
    input_user = 'id=>UserName'
    input_password = 'id=>UserPassword'
    input_loginrt = 'id=>LoginButton'
    def type_loginUser(self,text):
        self.type(self.input_user,text)
    def type_loginPw(self,password):
        self.type(self.input_password,password)
    def type_loginLogin(self):
        self.click(self.input_loginbt)
    def type_loginRLogin(self):
        self.click(self.input_loginrt)

class Resit(BasePaeg):
    input_regist = 'xpath=>/html/body/div[1]/div/div[1]/div/a[2]'
    input_Mobile = 'id=>txtMobile'
    input_pwd='id=>txtPwd'
    input_ImgCode='id=>txtImgCode'
    input_MobileCode ='id=>txtMobileCode'
    input_Tl='id=>toLogin'

    def type_regist(self):
        self.click(self.input_regist)
    def type_moblie(self,text):
        self.type(self.input_Mobile,text)
    def type_pwd(self,password):
        self.type(self.input_pwd,password)
    def type_imgacode(self,text):
        self.type(self.input_ImgCode,text)
    def type_mobilecode(self,text):
        self.type(self.input_MobileCode,text)
    def type_tl(self):
        self.click(self.input_Tl)

class Search(BasePaeg):
    input_textpage = 'id=>pageText'
    input_btnsearchprodut = 'id=>BtnSearchProdut'

    def type_textpage(self,text):
        self.type(self.input_textpage,text)
    def type_btnsearch(self):
        self.click(self.input_btnsearchprodut)






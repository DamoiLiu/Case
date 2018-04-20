#-*- coding:utf-8 -*-
import ConfigParser
import os

Cpath = os.path.dirname(os.path.realpath(__file__)) + '/'
CCpath = os.path.abspath(Cpath  + "config.ini")

Cong = ConfigParser.ConfigParser()
Cong.read(CCpath)
Dat = Cong.get("DATABASE","base_url")
print Dat

print "Login username is :"
User = Cong.get("DATABASE","login_user")
print User

print "Login password is :"
Pw = Cong.get("DATABASE","login_password")
print Pw

Ll= Cong.get("LOG","log_path")
print Ll

MH = Cong.get("EMAIL","mail_host")
print MH

MU = Cong.get("EMAIL","mail_user")
print MU

MP = Cong.get("EMAIL","mail_password")
print MP

SE = Cong.get("EMAIL","sender")
print SE

RE = Cong.get("EMAIL","recevier")
print RE

SB = Cong.get("EMAIL","subject")
print SB

RP = Cong.get("PATH","report_path")
print RP



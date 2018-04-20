#*-*- coding:utf-8 -*-
import random
from faker import Factory
faker = Factory().create('zh_CN')

def random_phone_number():
    """随机手机号码"""
    return faker.phone_number()

def random_str(min_chars=6, max_chars=8):
    """随机数字长度"""
    return faker.pystr(min_chars=min_chars, max_chars=max_chars)

if __name__ == '__main__':
    print (random_phone_number())
    print (random_str())
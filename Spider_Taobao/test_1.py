# *- coding: utf-8 -*-
import requests
import codecs
import datetime
import json
import csv
import time
import re
from bs4 import BeautifulSoup
headers = {
    "Accept":"*/*",
    "Accept-Language" :"zh-CN,zh;q=0.8",
    "User-Agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36",
    'Referer': "https://detail.m.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-14571687321.99.JsXAYT&id=537841713070&rn=127b1fee98370b4efbf794063fd199fe&abbucket=17"
}
def add(a,b):
    print(a,b)
    return a+b

if __name__ == '__main__':
    a=["2"]*5
    b = ["1"]*5
    a = (map(add,a,b))
    # print(a)
    # print(type({'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}["2"]))

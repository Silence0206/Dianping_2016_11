# *- coding: utf-8 -*-
import requests
import codecs
import datetime
import json
import csv
import time
import re
from bs4 import BeautifulSoup
import pandas as pd

def mainPaser(url):
    Headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36"}
    Response = requests.get(url, headers=Headers)
    Interial = BeautifulSoup(Response.content, 'lxml')
    pageConfig = Interial.find('script', text=re.compile('g_page_config'))
    return pageConfig.string
if __name__ == '__main__':
    pageConfig_string =mainPaser("https://s.taobao.com/search?q=%E8%84%B1%E7%9A%AE%E7%BB%BF%E8%B1%86")
    neededColumns = ['category', 'comment_count', 'item_loc', 'nick',
                     'raw_title', 'reserve_price', 'view_price', 'view_sales']
    print(pageConfig_string)
    PageConfig = re.search(r'g_page_config = (.*?);\n',
                           pageConfig_string)
    print(PageConfig.group(1))
    pageConfigJson = json.loads(PageConfig.group(1))
    # print(pageConfigJson)
    pageItems = pageConfigJson['mods']['itemlist']['data']['auctions']
    # print(pageItems)
    pageItemsJson = json.dumps(pageItems)
    # print(pageItemsJson)
    pageData = pd.read_json(pageItemsJson)
    # print(pageData)
    # print(pageData)
    # neededData = pageData[Paser.neededColumns]
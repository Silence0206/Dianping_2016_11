# *- coding: utf-8 -*-
import requests
import mysql.connector
import codecs
import datetime
import json
import csv
import time
import re
from bs4 import BeautifulSoup
"""
用于爬店铺信息和羽绒服分类下的商品信息
爬H5页面 找里面的js
地址形如
(meiyong)url = "https://only.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692171.0.0&sort=d&shop_cn=%E7%BE%BD%E7%BB%92%E6%9C%8D&ascid=1290623524&scid=1290623524&p=1&page_size=12&from=h5&shop_id=60129786&ajson=1&_tm_source=tmallsearch"
url = "https://only.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692363.0.0&sort=d&shop_cn=%E5%85%A8%E9%83%A8%E7%BE%BD%E7%BB%92%E6%9C%8D&ascid=1265455843&scid=1265455843&p=1&page_size=12&from=h5&shop_id=60129786&ajson=1&_tm_source=tmallsearch"
url = "https://semir.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692171.0.0&sort=d&shop_cn=%E5%A5%B3%E8%A3%85%E7%BE%BD%E7%BB%92%E6%9C%8D&ascid=1255576091&scid=1255576091&p=1&page_size=12&from=h5&shop_id=61127277&ajson=1&_tm_source=tmallsearch"
url = "https://bosideng.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692363.0.0&sort=d&shop_cn=2016%E5%A5%B3%E6%AC%BE&ascid=1201039383&scid=1201039383&p=1&page_size=12&from=h5&shop_id=57301762&ajson=1&_tm_source=tmallsearch"
"""
#s羽绒服
url_yrf = [
    "https://bosideng.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692363.0.0&sort=d&shop_cn=2016%E5%A5%B3%E6%AC%BE&ascid=1201039383&scid=1201039383&p=1&page_size=12&from=h5&shop_id=57301762&ajson=1&_tm_source=tmallsearch",
    "https://semir.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692171.0.0&sort=d&shop_cn=%E5%A5%B3%E8%A3%85%E7%BE%BD%E7%BB%92%E6%9C%8D&ascid=1255576091&scid=1255576091&p=1&page_size=12&from=h5&shop_id=61127277&ajson=1&_tm_source=tmallsearch",
    "https://only.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692363.0.0&sort=d&shop_cn=%E5%85%A8%E9%83%A8%E7%BE%BD%E7%BB%92%E6%9C%8D&ascid=1265455843&scid=1265455843&p=1&page_size=12&from=h5&shop_id=60129786&ajson=1&_tm_source=tmallsearch"
]
url_dy = [
    "https://only.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692171.0.0&sort=d&shop_cn=%E5%85%A8%E9%83%A8%E6%AF%9B%E5%91%A2%E5%A4%A7%E8%A1%A3&ascid=1262032952&scid=1262032952&p=1&page_size=12&from=h5&shop_id=60129786&ajson=1&_tm_source=tmallsearch",
    "https://semir.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692363.0.0&sort=d&shop_cn=%E6%AF%9B%E5%91%A2%E5%A4%96%E5%A5%97&ascid=1248376303&scid=1248376303&p=1&page_size=12&from=h5&shop_id=61127277&ajson=1&_tm_source=tmallsearch",
]

"""
num:限制一个店铺该类爬多少个商品
url：给的是对应分类的链接
"""
def getItem(url,num):
    res = requests.get(url)
    content =json.loads(res.text,"utf8")
    shop_id = content["shop_id"]
    user_id = content["user_id"]
    shop_title = content["shop_title"]
    shop_Url = content["shop_Url"]
    total_page = content["total_page"]
    items = content["items"]
    total_results = content["total_results"]
    shopList = [user_id,shop_id,shop_title,shop_Url,total_results,total_page]
    with codecs.open("data\\" + '店铺列表大衣.csv', 'a+', 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(shopList)
    print("=======写入店铺=========")
    print(shopList)
    print("===========即将写入该店铺该分类链接下商品详细信息============")
    count = 0
    for item in items:
        if(count < num):
            sold = item["sold"]
            item_id = item["item_id"]
            title = item["title"]
            img = item["img"]
            quantity = item["quantity"]
            totalSoldQuantity = item["totalSoldQuantity"]
            url = item["url"]
            price = item["price"]
            infoList = [user_id, shop_title, item_id, title, totalSoldQuantity, price, sold, url]
            with codecs.open("data\\" + '大衣.csv', 'a+', 'utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(infoList)
            print(infoList)
            count +=1






if __name__ == '__main__':
    for url in url_dy:
        print(url)
        getItem(url,10)
        time.sleep(5)
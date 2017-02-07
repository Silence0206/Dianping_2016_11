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

headers = {
    "Accept":"*/*",
    "Accept-Language" :"zh-CN,zh;q=0.8",
    "User-Agent" : "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36",
    'Referer': "https://detail.m.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-14571687321.99.JsXAYT&id=537841713070&rn=127b1fee98370b4efbf794063fd199fe&abbucket=17",
    'cookie':"cna=AxMWEHzPBiQCAdOh95mI/QFW; x=__ll%3D-1%26_ato%3D0; _m_user_unitinfo_=center; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; hng=CN%7Czh-cn%7CCNY; _tb_token_=e55641e0e5eb7; uc1=cookie15=UtASsssmOIJ0bQ%3D%3D&existShop=true; uc3=nk2=2HC2uuFuRz36njE1&id2=UoWzWcTfvgOT&vt3=F8dARHr7k7%2B31Ov0Ff0%3D&lg2=VT5L2FSpMGV7TQ%3D%3D; uss=AnDWaZxfUxw1wnd%2BNcWiThIY78n2mXGnqJWCsP8LPFaEL2PzyV0F5rXzbQ%3D%3D; lgc=%5Cu82B1%5Cu82B1%5Cu5BB6%5Cu7684%5Cu73A9%5Cu5B50; tracknick=%5Cu82B1%5Cu82B1%5Cu5BB6%5Cu7684%5Cu73A9%5Cu5B50; cookie2=18578ab6c9a28948fff79bcc686611a7; cookie1=VTk9z64OA%2B7NNEuBYVQ93qw%2FqypHoRRjORvFDuXj65A%3D; unb=144002137; skt=8a58de0a4e925b63; t=c43fd57a3ffb45c781f4def173741340; _l_g_=Ug%3D%3D; _nk_=%5Cu82B1%5Cu82B1%5Cu5BB6%5Cu7684%5Cu73A9%5Cu5B50; cookie17=UoWzWcTfvgOT; login=true; _m_h5_tk=079039e7a74f2d0c6a56409f139f58f2_1485772347511; _m_h5_tk_enc=6bd30837b01aa2be9d63f300a21b023c; l=AnR0oUQmjUlbUYf5U7do4D71xCnmTJg0; isg=AgIC-RnL7lLk2_2O9Ny6aa2UUwijUQbtY8UXY0wbL3Ujn6MZNGMX_aufPSEc",
}
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
url_lx_yrf = [
    "https://lachapelle.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692363.0.0&sort=d&shop_cn=%E7%BE%BD%E7%BB%92%E6%9C%8D%2F%E6%A3%89%E6%9C%8D%E4%BC%9A%E5%9C%BA&ascid=1292620462&scid=1292620462&p=1&page_size=12&from=h5&shop_id=111717832&ajson=1&_tm_source=tmallsearch",
    "https://lababite.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692363.0.0&sort=d&shop_cn=%E7%BE%BD%E7%BB%92%E6%9C%8D%2F%E6%A3%89%E6%9C%8D&ascid=1277126165&scid=1277126165&p=1&page_size=12&from=h5&shop_id=145900035&ajson=1&_tm_source=tmallsearch",
    "https://puella.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692363.0.0&sort=d&shop_cn=%E7%BE%BD%E7%BB%92%E6%9C%8D&ascid=1183907576&scid=1183907576&p=1&page_size=12&from=h5&shop_id=145901297&ajson=1&_tm_source=tmallsearch",
    "https://7modifier.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692171.0.0&sort=d&shop_cn=%E3%80%90%E7%BE%BD%E7%BB%92%2F%E6%A3%89%E6%9C%8D%E3%80%91&ascid=1272306214&scid=1272306214&p=1&page_size=12&from=h5&shop_id=145900751&ajson=1&_tm_source=tmallsearch",
]
url_lx_dy = [
    "https://lababite.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692363.0.0&sort=d&shop_cn=%E6%AF%9B%E5%91%A2%E5%A4%A7%E8%A1%A3&ascid=1277126166&scid=1277126166&p=1&page_size=12&from=h5&shop_id=145900035&ajson=1&_tm_source=tmallsearch",
    "https://lachapelle.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692363.0.0&sort=d&shop_cn=%E6%AF%9B%E5%91%A2%E5%A4%96%E5%A5%97&ascid=1265593813&scid=1265593813&p=1&page_size=12&from=h5&shop_id=111717832&ajson=1&_tm_source=tmallsearch"
    "https://puella.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692171.0.0&sort=d&shop_cn=%E5%91%A2%E5%A4%A7%E8%A1%A3&ascid=1280108421&scid=1280108421&p=1&page_size=12&from=h5&shop_id=145901297&ajson=1&_tm_source=tmallsearch",
    "https://7modifier.m.tmall.com/shop/shop_auction_search.do?spm=a320p.7692363.0.0&sort=d&shop_cn=%E5%91%A2%E5%A4%A7%E8%A1%A3&ascid=1273386170&scid=1273386170&p=1&page_size=12&from=h5&shop_id=145900751&ajson=1&_tm_source=tmallsearch",
]
"""
num:限制一个店铺该类爬多少个商品
url：给的是对应分类的链接
"""
def getItem(url,num,typename):
    res = requests.get(url, headers=headers)
    content =json.loads(res.text,"utf8")
    shop_id = content["shop_id"]
    user_id = content["user_id"]
    shop_title = content["shop_title"]
    shop_Url = content["shop_Url"]
    total_page = content["total_page"]
    items = content["items"]
    total_results = content["total_results"]
    shopList = [user_id,shop_id,shop_title,shop_Url,total_results,total_page]
    with codecs.open("data\\" + typename+'_店铺列表.csv', 'a+', 'utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(shopList)
    print("=======写入店铺=========")
    print(shopList)
    print("===========即将写入该店铺该分类链接下商品详细信息============")
    count = 0
    time.sleep(3)
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
            with codecs.open("data\\" +typename+ '_商品链接.csv', 'a+', 'utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(infoList)
            print(infoList)
            count +=1






if __name__ == '__main__':
    for url in url_lx_dy:
        print(url)
        getItem(url,100,"大衣")
        time.sleep(5)
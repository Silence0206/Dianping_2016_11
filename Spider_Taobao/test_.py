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
    'Referer': "https://detail.tmall.com/item.htm?spm=a1z10.3-b-s.w4011-14574898921.109.KJsltA&id=539149093287&rn=e61315666db7b52b40ffff392b94435e&abbucket=17",
    'cookie':"cna=AxMWEHzPBiQCAdOh95mI/QFW; x=__ll%3D-1%26_ato%3D0; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; _m_h5_tk=95dedf98d3adcead1a594e8c4ac0004d_1485752275690; _m_h5_tk_enc=d9903e848937ffd93d45ec90fae4761e; hng=CN%7Czh-cn%7CCNY; _tb_token_=IUIasGnGbKgC; uc1=cookie15=UIHiLt3xD8xYTw%3D%3D&existShop=true; uc3=nk2=2HC2uuFuRz36njE1&id2=UoWzWcTfvgOT&vt3=F8dARHr7ka7vxOs2XRI%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; lgc=%5Cu82B1%5Cu82B1%5Cu5BB6%5Cu7684%5Cu73A9%5Cu5B50; tracknick=%5Cu82B1%5Cu82B1%5Cu5BB6%5Cu7684%5Cu73A9%5Cu5B50; cookie2=69142dba7ac94f62f6a1f1031dd407b6; cookie1=VTk9z64OA%2B7NNEuBYVQ93qw%2FqypHoRRjORvFDuXj65A%3D; unb=144002137; skt=840535b413104137; t=c43fd57a3ffb45c781f4def173741340; _l_g_=Ug%3D%3D; _nk_=%5Cu82B1%5Cu82B1%5Cu5BB6%5Cu7684%5Cu73A9%5Cu5B50; cookie17=UoWzWcTfvgOT; login=true; isg=AmRk0wlL4Fk8IRuUpiJEk1-CNWJvb4hnkTPx2X6F8C_yKQTzpg1Y95qLmzvO; l=AgkJZg3gqFYGyspe9lwtrlmTmS5jVv2I",
}
#地址格式都是url这样
url = "https://rate.tmall.com/list_detail_rate.htm?itemId=537841713070&sellerId=356060330&order=3&append=0&content=1&currentPage=1"

def getOnePage(url,sellerid,itemid,filename):
    try:
        res = requests.get(url)
        res_text = re.sub('\'', '\"', res.text)
        content = json.loads("{" + res_text + "}", "utf8")["rateDetail"]
        lastPage = content["paginator"]["lastPage"]
        commentNum = content["rateCount"]["total"]
        rateList = content["rateList"]

        for item in rateList:
            auctionSku = item["auctionSku"]
            displayUserNick = item["displayUserNick"]
            id = item["id"]
            rateContent = item["rateContent"]
            rateDate = item["rateDate"]
            tamllSweetLevel = item["tamllSweetLevel"]
            sellerId = item["sellerId"]
            picNum = len(item["pics"])
            infoList = [itemid,sellerId, auctionSku, displayUserNick, id, rateContent, rateDate, tamllSweetLevel, picNum]
            # with codecs.open("onlydata\\"+sellerid + "_" + itemid + '_filter.csv', 'a+', 'utf-8') as f:
            with codecs.open("data\\"+filename+".csv", 'a+', 'utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(infoList)
            print(infoList)
    except BaseException as e:
        print(e)
        print("问题地址"+url)
        with codecs.open('log\FailLinks1.txt', 'a+', 'utf-8') as f:
            f.writelines(sellerid+","+ itemid+","+url+"\n")
    time.sleep(10)

"""
传进来的url的content要等于1！！！
"""
def getPageNum(url):
    res = requests.get(url)
    content = json.loads("{" + res.text + "}", "utf8")["rateDetail"]
    lastPage = content["paginator"]["lastPage"]
    commentNum = content["rateCount"]["total"]
    print("共"+str(lastPage)+"页")
    time.sleep(1)
    return lastPage

def spiderOneStore(sellerId,itemId,filename):
    firstUrl = "https://rate.tmall.com/list_detail_rate.htm?itemId=" + itemId + "&sellerId=" + sellerId + "&order=3&append=0&content=1&currentPage=1"
    pageNum = getPageNum(firstUrl)
    time.sleep(5)
    for i in range(1,pageNum+1):
        currURL= "https://rate.tmall.com/list_detail_rate.htm?itemId="+itemId+"&sellerId="+sellerId+"&order=3&append=0&content=1&currentPage="+str(i)
        print(currURL)
        getOnePage(currURL,sellerId,itemId,filename)

def readCSV(filename):
    with codecs.open(filename+".csv", 'r', 'utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)

#获取手写txt中的商品id
def getTextId(file_name):
    ids=[]
    with open (file_name, 'r') as f:#'fail_open_resURL.txt'
        for line in f.readlines():
            ids.append(line.split(",")[0])
    return ids

"""
获取羽绒服.csv中的商品然后爬
返回（店铺id，商品id）
"""
def getItemsFromCsv(file_name):
    with codecs.open(file_name+".csv", 'r', 'utf-8') as f:
        tuples = []
        for line in f.readlines():
            infos = line.split(",")
            idtuple = (infos[0],infos[2])
            tuples.append(idtuple)
    return tuples

def getFailCom(filename):
    with codecs.open(filename+".txt", 'r', 'utf-8') as f:
        infos = []
        for line in f.readlines():
            keys = line.split(",")
            infos.append((keys[0],keys[1],keys[2].strip()))
        print(infos)
        return infos



def main2():
    tuples = getItemsFromCsv("data\羽绒服_商品链接 - 副本")
    filename = '羽绒服_评论'
    print("=========获取待爬取商品列表=========")
    print(tuples)
    for item in tuples:
        spiderOneStore(item[0], item[1],filename)

def main3():
    infos = getFailCom("G:\Dianping2017\Dianping_2016_11\Spider_Taobao\log\FailLinks1")
    for info in infos:
        getOnePage(info[2],info[0],info[1],"羽绒服_评论")

if __name__ == "__main__":
    main3()



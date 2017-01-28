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
        with codecs.open('log\FailLinks.txt', 'a+', 'utf-8') as f:
            f.writelines(sellerid+","+ itemid+","+url+"\n")
    time.sleep(7)

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

def spiderOneStore(sellerId,itemId):
    firstUrl = "https://rate.tmall.com/list_detail_rate.htm?itemId=" + itemId + "&sellerId=" + sellerId + "&order=3&append=0&content=1&currentPage=1"
    pageNum = getPageNum(firstUrl)
    for i in range(1,pageNum+1):
        currURL= "https://rate.tmall.com/list_detail_rate.htm?itemId="+itemId+"&sellerId="+sellerId+"&order=3&append=0&content=1&currentPage="+str(i)
        print(currURL)
        getOnePage(currURL,sellerId,itemId)

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



#只对only sellerid写死
def createStoresLink(sellerId,idPath):
    ids = getTextId(idPath)#"only\only_lianyiqun.txt"
    stores = []
    # sellerId = "356060330"
    for itemId in ids:
        currURL = "https://rate.tmall.com/list_detail_rate.htm?itemId=" + itemId + "&sellerId=" + sellerId + "&order=3&append=0&content=0&currentPage=1"
        stores.append(currURL)
    print(stores)

def main2():
    tuples = getItemsFromCsv("data\大衣")
    print("=========获取待爬取商品列表=========")
    print(tuples)
    for item in tuples:
        spiderOneStore(item[0], item[1])


if __name__ == "__main__":
    infos = getFailCom("G:\Dianping2017\Dianping_2016_11\Spider_Taobao\log\FailLinks")
    for info in infos:
        getOnePage(info[2],info[0],info[1],"羽绒服评论")


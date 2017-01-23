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

def getOnePage(url,sellerid,itemid):
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
            infoList = [sellerId, auctionSku, displayUserNick, id, rateContent, rateDate, tamllSweetLevel, picNum]
            with codecs.open("onlydata\\"+sellerid + "_" + itemid + '_filter.csv', 'a+', 'utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(infoList)
            print(infoList)
    except BaseException as e:
        print(e)
        print("问题地址"+url)
        with open('log\FailLinks.txt', 'a') as f:
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
        print((tuples))
    return tuples

# def getStoreLink(url):
#     res = requests.get(url)
#     soup = BeautifulSoup(res.text, 'lxml')
#     print(soup)
    # all_line = soup.find(class_="J_TItems")
    # print(all_line)
    # all_line = soup.find(class_="J_TItems").find_all(class_="item4line1",limit=4)
    # for item4line1 in all_line:
    #     items = item4line1.select(".item")
    #     for item in items:
    #         id = item["data-id"]
    #         href = item.select(".detail > .item-name")[0]["href"]
    #         print(id,href)


#https://rate.tmall.com/list_detail_rate.htm?itemId=539330410500&sellerId=356060330&order=3&append=0&content=0&currentPage=10
#https://rate.tmall.com/list_detail_rate.htm?itemId=521269150100&sellerId=653206261&order=3&append=0&content=0&currentPage=3
def main1():
    spiderOneStore("https://rate.tmall.com/list_detail_rate.htm?itemId=539968109660&sellerId=356060330&order=3&append=0&content=0&currentPage=1","356060330","539968109660")

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
    getItemsFromCsv("data\羽绒服")


if __name__ == "__main__":
    # itemIds = getTextId("only\only_lianyiqun.txt")
    # sellerIds = ["356060330"]*len(itemIds)
    # terms = list(zip(sellerIds,itemIds))
    # for term in terms:
    #     # print(term[0],term[1])
    #     spiderOneStore(term[0],term[1])
    main2()


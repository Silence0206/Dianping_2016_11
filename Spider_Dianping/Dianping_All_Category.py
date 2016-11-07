# *- coding: utf-8 -*-
import mysql.connector
import requests
import datetime
import re
import time
from bs4 import BeautifulSoup
import logging

class get_Categorys():
    def __init__(self,url,usr, pwd, dbname):
        self.url = url
        self.session = requests.session()
        self.headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Host": "www.dianping.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            'Referer': "http://www.dianping.com/shanghai/life",
             'Cookie':'m_rs=5a23972d-921a-4d46-9ff8-d385d3381dbd; _hc.v=00182c04-e7c3-0953-dc3a-0c57f60bdb0b.1469080663; __utma=1.273426386.1469369064.1469369064.1469369064.1; __utmz=1.1469369064.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dper=79e1190dfef09628df10db9edd2c9590a25d955f69a85bfe684d4a4ff5d2ef02; ua=13816174065; PHOENIX_ID=0a65026a-1562272a84d-126c111; ll=7fd06e815b796be3df069dec7836c3df; s_ViewType=10; JSESSIONID=6043782DB8A392CA09529A51163D3CA0; aburl=1; cy=1; cye=shanghai'

        }
        self.conn = mysql.connector.connect(user=usr, password=pwd, database=dbname)
        self.tuples = [] #存所有序列

    def create_database(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                'create table category (category_id varchar(20) primary key, category_name varchar(20),category_link  text(20),add_time datetime default NULL,flag bool )')
            self.conn.commit()
            cursor.close()
            print("餐厅种类表建立成功")
        except BaseException as e:
            print("建立餐厅种类表出问题啦", e)
    #单条插入
    def insert_category(self,category_id,category_name,category_link,add_time):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                'INSERT INTO category (category_id,category_name,category_link,add_time,flag)VALUES (%s, %s, %s, %s, %s);',
                (category_id,category_name,category_link,add_time, False))
            self.conn.commit()
            cursor.close()
            print(category_id,category_name,category_link,add_time, "插入成功")
        except BaseException as e:
            print("插入失败",e)

    #批量插入
    def insert_All_category(self,categoryList):
        try:
            cursor = self.conn.cursor()
            sql = 'INSERT INTO category (category_id,category_name,category_link,add_time,flag)VALUES (%s, %s, %s, %s, %s)'
            cursor.executemany(sql,categoryList)
            self.conn.commit()
            cursor.close()
            print("批量插入成功")
        except BaseException as e:
            print("插入失败",e)

    def get_category(self):
        html = self.session.get(self.url, headers=self.headers).text
        soup = BeautifulSoup(html, 'lxml')
        try:
            classfyList = soup.find(id="classfy").find_all("a")
        except BaseException as e:
            print("未找到分类列表")
            classfyList = None
            return
        for item in classfyList:
            try:
                id = item.get("href").split('/')[-1]
                name=item.get_text(strip=True)
                link = "http://www.dianping.com"+item.get("href")
                time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.tuples.append((id,name,link,time,False))
            except BaseException as e:
                print("解析某条出错",e)






if __name__ == '__main__':
    test=get_Categorys("http://www.dianping.com/search/category/1/10",'root', '58424716', 'dianping')
    test.create_database()
    test.get_category()
    if(test.tuples):
        test.insert_All_category(test.tuples)
    # # 一条条插入
    # for item in test.tuples:
    #     test.insert_category(item[0],item[1],item[2],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))




# *- coding: utf-8 -*-
import mysql.connector
import requests
import datetime
from bs4 import BeautifulSoup
#爬取上海各个行政区
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language" :"zh-CN,zh;q=0.8",
    "Host": "www.dianping.com",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    'Referer': "http://www.dianping.com/shanghai/life"
}


def create_database(usr, pwd, db):
    global conn
    conn = mysql.connector.connect(user=usr, password=pwd, database=db)
    cursor = conn.cursor()
    cursor.execute('create table area (area_id varchar(20) primary key, area_name varchar(20),area_link  text(20),area_time datetime default NULL,flag bool )')
    conn.commit()
    cursor.close()

#更新一条记录的状态
def insert_area(region_id,region_name, region_href,time):
    try:
        global conn
        cursor = conn.cursor()
        cursor.execute('INSERT INTO area (area_id,area_name,area_link,area_time,flag)VALUES (%s, %s, %s, %s, %s);',(region_id, region_name,region_href,time,False))
        conn.commit()
        cursor.close()
        print(region_id, region_name, region_href, time,"插入成功")
    except BaseException as e:
        print("出问题啦", e)
    finally:
        pass


if __name__ == "__main__":
    create_database('root', '58424716', 'dianping')
    res = requests.get("http://www.dianping.com/search/category/1/10", headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    regions = soup.find(id="region-nav")
    for region in regions.find_all("a"):
        region_href = "http://www.dianping.com"+region["href"]
        region_name = region.get_text()
        region_id = region["href"].split("/")[-1]
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_area(region_id,region_name,region_href,time)
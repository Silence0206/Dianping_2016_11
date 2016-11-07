# *- coding: utf-8 -*-
import mysql.connector
import requests
import datetime
from bs4 import BeautifulSoup
#根据行政区爬商圈
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language" :"zh-CN,zh;q=0.8",
    "Host": "www.dianping.com",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    'Referer': "http://www.dianping.com/shanghai/life"
}


def create_database(usr, pwd, db):
    try:
        global conn
        conn = mysql.connector.connect(user=usr, password=pwd, database=db)
        cursor = conn.cursor()
        cursor.execute(
            'create table bussi_region (bussi_id varchar(20) primary key, bussi_name varchar(20),bussi_link  text(20),area_id varchar(20),add_time datetime default NULL,flag bool )')
        conn.commit()
        cursor.close()
    except BaseException as e:
        print("建立商区表出问题啦", e)
    finally:
        pass


#更新一条记录的状态
def insert_bussi(bussi_id,bussi_name,bussi_link,area_id,add_time):
    global conn
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO bussi_region (bussi_id,bussi_name,bussi_link,area_id,add_time,flag)VALUES (%s, %s, %s, %s, %s, %s);',
        (bussi_id, bussi_name, bussi_link, area_id, add_time, False))
    conn.commit()
    cursor.close()
    print(bussi_id, bussi_name, bussi_link, area_id, add_time, "插入成功")




def read_list(usr, pwd, db):
    try:
        global conn
        cursor = conn.cursor()
        cursor.execute( 'select * from area')
        rows = cursor.fetchall()
        cursor.close()
        #conn.close()##最后再关
        return  rows
    except BaseException as e:
        print("读取行政区列表出问题啦", e)
        return

def find_bussi_fromArea(url,areaId):
    try:
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        print("开始爬 id为",areaId+"的",url)
        busis=soup.find(id="region-nav-sub").find_all("a")
        for bussi in busis[1:]:
            bussi_id = bussi["href"].split("/")[-1]
            bussi_name = bussi.get_text()
            bussi_link = "http://www.dianping.com"+bussi["href"]
            add_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_bussi(bussi_id, bussi_name, bussi_link, areaId, add_time)
    except BaseException as e:
        print("爬的时候出问题啦",e)
        pass

if __name__ == "__main__":
    create_database('root', '58424716', 'dianping')
    area_rows = read_list('root', '58424716', 'dianping')
    for area in area_rows:
        area_link =area[2]
        areaId = area[0]
        find_bussi_fromArea(area_link,areaId)

# *- coding: utf-8 -*-
#提取商区表的所有数据，根据每个商区页面爬取它按照评论数逆序排列的50页商家
import mysql.connector
import requests
import datetime
import time
import re
from bs4 import BeautifulSoup
SleepNum = 1     # 抓取页面的间隔时间，可为0
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language" :"zh-CN,zh;q=0.8",
    "Host": "www.dianping.com",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    'Referer': "http://www.dianping.com/shanghai/life",
    'Cookie':'_hc.v=00182c04-e7c3-0953-dc3a-0c57f60bdb0b.1469080663; __utma=205923334.275296798.1469082376.1469082376.1469109403.2; __utmz=205923334.1469082376.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); PHOENIX_ID=0a650c81-15610b18a16-8a1918; _dp.ac.v=d0884a6b-b29b-4748-90a4-4f71e1bc8535; dper=4dcc94bf30f951ac9a83cfdc9df8d32056c8aab3926eb9220b40603ad7c444ff; ll=7fd06e815b796be3df069dec7836c3df; ua=732379020%40qq.com; ctu=b33af298f0f018b44702e07460c6750f2148460b1f3f12d2a2a92cf0e629162e; s_ViewType=10; aburl=1; cy=1; cye=shanghai; _hc.s=\"\\\"00182c04-e7c3-0953-dc3a-0c57f60bdb0b.1469080663.1469158888.1469159378\\\"\"'
}

def create_database(usr, pwd, db):
    global conn
    try:
        conn = mysql.connector.connect(user=usr, password=pwd, database=db)
        cursor = conn.cursor()
        cursor.execute(
            'create table restaurants (res_id varchar(20) primary key, res_name varchar(90),'
            '  res_link  text(20),isgroup bool,ispromote bool,isbook bool,iscard bool,isout bool,'
            'rank INT ,comm_num INT ,mean_price INT,category_Id varchar(20),'
            'taste DOUBLE ,envir DOUBLE ,service DOUBLE ,bussi_areaId varchar(20),'
            ' addr text(50),addtime datetime default NULL,flag bool )')
        conn.commit()
        cursor.close()
    except BaseException as e:
        print("出问题啦", e)
    finally:
        pass


#更新一条记录的状态
def insert_res(res_id,res_name,res_link,isgroup,ispromote,isbook,iscard,isout,rank,comm_num,mean_price,category_Id,taste,envir,service,bussi_areaId,addr,addtime):
    global conn
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO restaurants (res_id,res_name,res_link,isgroup,ispromote,isbook,iscard,isout,rank,comm_num,mean_price,category_Id,taste,envir,service,bussi_areaId,addr,addtime,flag)'
        'VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s);',
        (
        res_id, res_name, res_link, isgroup, ispromote, isbook, iscard, isout, rank, comm_num, mean_price,
        category_Id, taste, envir, service, bussi_areaId, addr, addtime, False))
    conn.commit()
    cursor.close()
    print(res_id, res_name, res_link, isgroup, ispromote, isbook, iscard, isout, rank, comm_num,
          mean_price, category_Id, taste, envir, service, bussi_areaId, addr, addtime, "插入成功")

#分析一页的数据并存储数据库
def find_res_onePage(url):
    try:
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')
        # 页码
        if(soup.find(class_="page") is not  None):
            curr_pageNum = soup.find(class_="page").find(class_="cur").get_text()
            print("开始爬", url, "\n该页为第", curr_pageNum, "页")
        else:
            print("开始爬", url, "\n该页为第1页 共1页")
            curr_pageNum = 1
        shops = soup.find(id="shop-all-list")
    except BaseException as e:
        print(url,"打开出错休息5秒 错误原因：", e)
        time.sleep(5)
        return ("")
    for shop in shops.find_all("li"):
        try:
            atts = shop.attrs
            if (atts.get('data-midas') is None): #推广的不要
                item = shop.find(class_="txt")  # 每家店总标签
                name_a = item.select(".tit > a")  # 带店名的那个快捷方式
                name = name_a[0].get_text(strip=True)
                href = "http://www.dianping.com" + name_a[0]["href"]
                id = name_a[0]["href"].split("/")[-1]
                igroup = ipromote = ibook = iout = icard = False
                promo_div = item.select(".tit > .promo-icon")[0]
                promos = promo_div.select("a")
                if (promos != []):
                    for pro in promos:
                        clas_name = pro["class"][0]
                        if (clas_name == "igroup"):
                            igroup = True
                        elif (clas_name == "ipromote"):
                            ipromote = True
                        elif (clas_name == "ibook"):
                            ibook = True
                        elif (clas_name == "iout"):
                            iout = True
                        else:
                            pass
                # 评分点评数人均
                comment_div = item.select(".comment ")[0]
                rank = comment_div.select("span")[0]["class"][1]  # sml-str50
                mode = re.compile(r'\d+')
                rank = int(mode.findall(rank)[-1])
                comm_num = comment_div.select("a:nth-of-type(1) ")[0].find("b")
                if (comm_num is not None):
                    comm_num = int(comm_num.get_text())
                else:
                    comm_num = 0
                mean_price = comment_div.select("a:nth-of-type(2) ")[0].find("b")
                if (mean_price is not None):
                    mean_price = int(mean_price.text.replace("￥", ""))
                else:
                    mean_price = 0
                # 口味环境服务
                if(item.find(class_="comment-list") is not None):
                    comment_list = item.select(".comment-list ")[0]
                    taste = comment_list.select("span:nth-of-type(1) ")[0].find("b").get_text()
                    envir = comment_list.select("span:nth-of-type(2) ")[0].find("b").get_text()
                    service = comment_list.select("span:nth-of-type(3) ")[0].find("b").get_text()
                else:
                    taste=envir=service=0
                # 分类 商区 地址
                tag_addr = item.select(".tag-addr ")[0]
                categoryId = tag_addr.select("a:nth-of-type(1)")[0]["href"].split("/")[-1]
                bussi_areaId = tag_addr.select("a:nth-of-type(2)")[0]["href"].split("/")[-1]
                addr = tag_addr.select(".addr")[0].get_text(strip=True)
                addtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                insert_res(id, name, href, igroup, ipromote, ibook, icard, iout, rank,
                       comm_num, mean_price, categoryId, taste, envir, service, bussi_areaId, addr, addtime)
        except BaseException as e:
            print("解析该页的某条数据出错啦",e)
    print("第", curr_pageNum, "页爬取完成")
    if(soup.find(class_="page") is not None):
        next_page = soup.find(class_="page").find(class_="next")
    else:
        next_page = None
    if(next_page is not None):
        return ("http://www.dianping.com" +next_page["href"], curr_pageNum, url)
    else:
        return ("", curr_pageNum, url)
            # print(id, name, "c3580", href, igroup, ipromote, ibook, icard, iout, rank,
            #              comm_num, mean_price, categoryId, taste, envir, service, bussi_areaId, addr, addtime)
            # 页码

def read_list(usr, pwd, db):
    try:
        conn1 = mysql.connector.connect(user=usr, password=pwd, database=db)
        cursor = conn1.cursor()
        cursor.execute( 'select * from bussi_region')
        rows = cursor.fetchall()
        cursor.close()
        conn1.close()
        return  rows
    except BaseException as e:
        print("出问题啦", e)
        return



#存取某商圈50页面数据
def find_all(url):
    link = url
    while (link != ""):
        link = find_res_onePage(link)[0]

create_database('root', '58424716', 'dianping')
a=read_list('root', '58424716', 'dianping')
for item in a:
    region_id=item[0] #商圈id 商圈名称 商圈链接
    region_name=item[1]
    region_link =item[2]+"o10" #店铺按照点评最多排序
    print("========开始爬取 商圈id:",region_id,"商圈名称：",region_name,"链接：",region_link)
    find_res_onePage(region_link,region_id)
    try:
        find_all(region_link)
    except BaseException as e:
        print("爬取该商圈出错啦",e)
        pass
        # find_res_onePage("http://www.dianping.com/search/category/1/10/c3580p46?aid=67224668%2C66553218%2C58311855%2C67218964%2C57309973%2C59398184")
# find_all("http://www.dianping.com/search/category/1/10/r22948o10")
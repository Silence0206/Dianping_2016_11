# *- coding: utf-8 -*-
import mysql.connector
import requests
import datetime
import re
import time
from bs4 import BeautifulSoup
import logging
#根据店铺地址爬评论
SleepNum = 1     # 抓取页面的间隔时间，可为0
headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Connection":"keep-alive",
    "Accept-Language" :"zh-CN,zh;q=0.8",
    "Host": "www.dianping.com",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    'Referer': "http://www.dianping.com/shanghai/life",
    # 'Cookie':'_hc.v=00182c04-e7c3-0953-dc3a-0c57f60bdb0b.1469080663; __utma=1.273426386.1469369064.1469369064.1469369064.1; __utmz=1.1469369064.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dper=5529c55bfbd478e8c1613429bfde641841a70874a3484cd0259f2c34696bdc02; ua=15651383078; PHOENIX_ID=0a017429-1562227b555-ae953b6; ll=7fd06e815b796be3df069dec7836c3df; JSESSIONID=B596AEA7C9E6A9AF4B51AFD1AC85FFC9; aburl=1; cy=1; cye=shanghai'
    'Cookie':'m_rs=5a23972d-921a-4d46-9ff8-d385d3381dbd; _hc.v=00182c04-e7c3-0953-dc3a-0c57f60bdb0b.1469080663; __utma=1.273426386.1469369064.1469369064.1469369064.1; __utmz=1.1469369064.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dper=79e1190dfef09628df10db9edd2c9590a25d955f69a85bfe684d4a4ff5d2ef02; ua=13816174065; PHOENIX_ID=0a65026a-1562272a84d-126c111; ll=7fd06e815b796be3df069dec7836c3df; s_ViewType=10; JSESSIONID=6043782DB8A392CA09529A51163D3CA0; aburl=1; cy=1; cye=shanghai'
}
proxies = {

}

#配置日志
# 创建一个logger
logger = logging.getLogger()
logger.setLevel(logging.ERROR)
# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('DpComlog.txt')
# 定义handler的输出格式formatter
formatter = logging.Formatter('%(asctime)s  %(funcName)s  %(module)s [line:%(lineno)d] %(levelname)s %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

def create_database(usr, pwd, db):
    global conn
    try:
        conn = mysql.connector.connect(user=usr, password=pwd, database=db)
        cursor = conn.cursor()
        cursor.execute(
            'create table comments (comment_Id varchar(20) primary key, res_id varchar(20),'
            '  member_Id  varchar(20),member_name varchar(30),isVIP bool ,'
            'member_rank INT ,given_rank INT ,mean_price INT,'
            'taste INT ,envir INT ,service INT ,comment_text text,'
            ' comment_time datetime,addtime datetime default NULL,flag bool )')
        conn.commit()
        cursor.close()
    except mysql.connector.Error as e:
        logger.error(e)
        print("创建数据库出问题啦", e)

#访问过的店铺做标记
def set_flag(resId):
    global conn
    conn = mysql.connector.connect(user='root', password='58424716', database='dianping')
    try:
        cursor = conn.cursor()
        cursor.execute('UPDATE restaurants SET flag=TRUE  WHERE res_id =%s'% resId)
        conn.commit()
        cursor.close()
    except mysql.connector.Error as e:
        print("标记已爬店铺ID出问题", e)
        logger.error(e)
        with open('Flag_error_resId.txt', 'a') as error_resIdLog:
            error_resIdLog.writelines("时间：", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),"做标记失败的店铺："+resId+"\n")
        conn.rollback

# 更新一条记录的状态（某家店的某条评论）
def insert_rescomments (comment_Id , res_id ,member_Id , member_name,isVIP, member_rank  ,given_rank  ,mean_price ,
            taste  ,envir  ,service  ,comment_text , comment_time ,addtime   ):
    global conn2
    conn2 = mysql.connector.connect(user='root', password='58424716', database='dianping',charset='utf8mb4')
    cursor = conn2.cursor()
    cursor.execute(
        'INSERT INTO comments (comment_Id , res_id ,member_Id , member_name,isVIP, member_rank  ,given_rank  ,mean_price ,taste  ,envir  ,service  ,comment_text , comment_time ,addtime,flag)'
        'VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s);',
        (comment_Id , res_id ,member_Id , member_name,isVIP, member_rank  ,given_rank  ,mean_price ,taste  ,envir  ,service  ,comment_text , comment_time ,addtime, False))
    conn2.commit()
    cursor.close()
    print(comment_Id, res_id, member_Id, member_name,isVIP, member_rank, given_rank, mean_price, taste, envir, service,comment_text, comment_time, addtime ,"插入成功")

def find_comment_onePage(url):
    try:
        print("新一轮onepage",url)
        resId = url.split("/")[4]
        if ("review_more" not in url):
            url += "/review_more"
        req = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(req.text, 'lxml')
        # 页码
        pageDiv = soup.find(class_="Pages").find(class_="Pages")
        if ( pageDiv is not None):
            curr_pageNum = pageDiv.find(class_="PageSel").get_text().replace(u'\xa0', u' ')
            print("开始爬", url, "\n该页为第", curr_pageNum, "页")
        else:
            print("开始爬", url, "\n该页为第1页 共1页")
            curr_pageNum = 1
        comts = soup.find(class_="comment-list").find("ul")
    except BaseException as e:
        print(url, "打开出错休息2秒 错误原因：", e)
        error_resLog= open('fail_open_resURL.txt', 'a')
        error_resLog.writelines(url+"打开页面失败的店铺："+"时间："+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"原因：" + str(e) + "=========================\n")
        error_resLog.close()
        logger.error(e)
        time.sleep(1)
        return ("")
    for comt in comts.find_all("li",recursive=False):#只检查子节点！！！
        try:
            comment_Id = comt["data-id"]
            memnber_Id = comt.select(".pic > a")[0]["user-id"]
            memnber_name = comt.select(".pic > .name")[0].get_text().replace(u'\xa0', u' ').replace(u'\xa5', u' ')
            isVIP = False
            if(comt.find(class_="icon-vip") is not None):
                isVIP = True
            rank_span = comt.find(class_="contribution").find("span")
            rank = rank_span["class"][1]
            mode = re.compile(r'\d+')
            member_rank = int(mode.findall(rank)[-1])
            content = comt.find(class_="content")
            if(content.select(".user-info > .item-rank-rst")):
                given_rank=content.select(".user-info > .item-rank-rst")[0]["class"][1]
                given_rank = int(mode.findall(given_rank)[-1])
            else:
                given_rank =0

            mean_price = content.find(class_="comm-per")
            if(mean_price is not None):
                mean_price =int(mean_price.text.replace("人均 ￥","").replace("消费 ￥","").replace("费用 ￥","").replace(u'\xa0', u' ') )
            else:
                mean_price = 0
            comment_list = content.find(class_="comment-rst")
            taste=envir=service=0
            if(comment_list is not None):
               taste = comment_list.select("span:nth-of-type(1) ")[0].get_text()[2]
               envir = comment_list.select("span:nth-of-type(2) ")[0].get_text()[2]
               service = comment_list.select("span:nth-of-type(3) ")[0].get_text()[2]
            com_text=content.find(class_="J_brief-cont").get_text(strip=True).replace(u'\xa0', u' ')
            addtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            year = datetime.datetime.now().strftime("%Y-")
            #处理各种日期情况： 09-07-07  更新于07-07 21:45 ！ 09-07-08！07-24
            comment_timeStr = content.find(class_="time").get_text()
            if("更新于" not in comment_timeStr ):
                if(len(comment_timeStr) == 5):
                    comment_time = datetime.datetime.strptime(year+comment_timeStr,"%Y-%m-%d")
                elif(len(comment_timeStr) == 8):
                    comment_time = datetime.datetime.strptime("20"+comment_timeStr,"%Y-%m-%d")
                else:
                    comment_time = "0000-00-00 00:00:00"
            else:
                comment_timeStr =content.find(class_="time").get_text().split("更新于")[1]
                if (len(comment_timeStr) == 11):
                    comment_time = datetime.datetime.strptime(year + comment_timeStr, "%Y-%m-%d %H:%M")
                elif(len(comment_timeStr) == 5):
                    comment_time = datetime.datetime.strptime(year+comment_timeStr,"%Y-%m-%d")
                elif(len(comment_timeStr) == 8):
                    comment_time = datetime.datetime.strptime("20"+comment_timeStr,"%Y-%m-%d")
                else:
                    comment_time = "0000-00-00 00:00:00"
            insert_rescomments(comment_Id, resId, memnber_Id, memnber_name, isVIP, member_rank, given_rank, mean_price,
                               taste, envir, service, com_text, comment_time, addtime)
            # print(comment_Id, resId, memnber_Id, memnber_name, isVIP, member_rank, given_rank, mean_price,taste, envir, service, com_text, comment_time, addtime)
        except BaseException as e:
            print("解析该页的某条数据出错啦", e)
            with open('error_resId.txt', 'a') as error_resIdLog:
                error_resIdLog.writelines("某条数据解析错误 页面地址：" + url +"评论人" +memnber_name+"\n")
                error_resIdLog.writelines("时间："+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"原因：" + str(e) + "=========================\n")
            logger.error(e)
            time.sleep(1)
    print("第", curr_pageNum, "页爬取完成")
    time.sleep(2)
    if (pageDiv is not None):
        next_page = pageDiv.find(class_="NextPage")
    else:
        next_page = None

    if(next_page is not None):
        return ("http://www.dianping.com/shop/"+resId+"/review_more"+next_page["href"],resId, curr_pageNum, url)
    else:
        return ("", resId,curr_pageNum, url)

def find_all_page(url):
    link = url
    while (link != ""):
        link = find_comment_onePage(link)[0]

def read_list(usr, pwd, db,areaId):
    try:
        conn1 = mysql.connector.connect(user=usr, password=pwd, database=db)
        cursor = conn1.cursor()
        cursor.execute( 'SELECT * FROM dianping.restaurants where  Bussi_areaid= "%s" and flag=false order by  res_id'% areaId)
        rows = cursor.fetchall()
        cursor.close()
        conn1.close()
        return  rows
    except BaseException as e:
        print("出问题啦", e)
        return

#获取爬了一半就死的店面
def getFail(file_name):
    urls=[]
    with open (file_name, 'r') as f:#'fail_open_resURL.txt'
        for line in f.readlines():
            if("pageno" in line.split("打开")[0]):
                # print(line.strip().split("打开")[0])
                urls.append(line.strip().split("打开")[0])
    return urls


def main(bussi_areaId):
    create_database('root', '58424716', 'dianping')
    a = read_list('root', '58424716', 'dianping',bussi_areaId)
    print(a)
    with open('start.txt', 'a') as startLog:
        startLog.writelines("开始时间：" + datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S") + "\n")
    for item in a:
        region_id = item[0]  # 店铺id 店铺名称 店铺链接
        region_name = item[1]
        region_link = item[2]
        print("========开始爬取 店铺id:", region_id, "店铺名称：", region_name, "店铺链接：", region_link)
        try:
            find_all_page(region_link)
            set_flag(region_id)
            with open('success.txt', 'a') as success_resIdLog:
                success_resIdLog.writelines(
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + region_id + region_link + "\n")

        except BaseException as e:
            print("爬取该店铺出错啦", e)
            logger.error(e)
            with open('error_resId.txt', 'a') as error_resIdLog:
                error_resIdLog.writelines("时间：" + datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S") + "findall出问题：" + region_id + "   " + region_link + "\n")
        time.sleep(2)


#真正的主函数
# main("r812")
#记录在爬了一半失败的文档中把他们提取出来再来一遍
if __name__ == '__main__':
    urls = getFail('fail_open_resURL.txt')
    print(urls)
    for url in urls:
        try:
            print(type(url))
            resId = url.split("/")[4]
            find_all_page(url)
            set_flag(resId)
        except BaseException as e:
            print(url,e)
            with open('fail_open_resURL1.txt', 'a') as error_resIdLog:
                error_resIdLog.writelines(url + "打开页面失败的店铺：" + "时间：" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "原因：" + str(
        e) + "=========================\n")

#
# find_all_page("http://www.dianping.com/shop/11552135/review_more?pageno=45")
# set_flag("11552135")



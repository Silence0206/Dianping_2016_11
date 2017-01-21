#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import datetime
import time
import codecs
from multiprocessing.dummy import Pool as ThreadPool
import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
	'Cookie':'_hc.v=3edd337d-6f9e-9764-21dc-a65901046f99.1466694124; PHOENIX_ID=0a016717-158b316b71d-bad799; __utma=1.2036653388.1480473621.1480473621.1480473621.1; __utmb=1.1.10.1480473621; __utmc=1; __utmz=1.1480473621.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); thirdtoken=32888B3D1B6301F8C2BB36F6165CF8F0; _thirdu.c=dc7cf1d04d99c7315ca99bcc67778eda; dper=cdefae703cc81ccd108d83494853aa63e27c4f8403d6ca80af1a1a0cff88f27b; ll=7fd06e815b796be3df069dec7836c3df; ua=%E5%8F%B0%E6%B9%BE%E6%BC%82%E6%B5%81%E5%AE%A2; ctu=6b83bc096d8c5b144736577714cb1a98ba531c0d9df381821a97e7f3a19c7918; uamo=13651715541; s_ViewType=10; JSESSIONID=374B07700E3FB75EED10A176D9F1D4B3; aburl=1; cy=1; '
}

def get_shop_link():
	num = 1
	link_list = []
	for page in xrange(5,51):
		res = requests.get('http://www.dianping.com/search/category/1/10/r5939p'+str(page)+'?aid=69733715%2C3464923%2C32868149%2C70897453%2C67796584%2C15090062',headers= headers)
		soup = BeautifulSoup(res.content,'html.parser')
		for tit in soup.select('.tit > a'):
			try:
				print num,tit['title'],tit['href']
				link = 'http://www.dianping.com'+tit['href']
				num +=1
				link_list.append(link)
				time.sleep(1)
			except Exception, e:
				print e
	return link_list
			

def get_shop_info(url):
	info_list = []
	res = requests.get(url,headers=headers)
	soup = BeautifulSoup(res.content,'html.parser')
	try:
		title = soup.select('.breadcrumb > span')[0].get_text()
		star = soup.select('.basic-info > .brief-info > span')[0]['title']
		avg = soup.select('.basic-info > .brief-info > .item')[1].text.replace('人均：','')
		add = soup.select('.basic-info > .address > .item')[0]['title']
		tel = soup.select('.basic-info > .tel > .item')[0].text
		branch = soup.select('.basic-info > .shop-name > .branch')[0].text
		info_list.append(title)
		info_list.append(star)
		info_list.append(avg)
		info_list.append(add)
		info_list.append(tel)
		info_list.append(branch)
		with codecs.open(u'dianping_qingpu.csv','a+','gb18030') as f:
			writer = csv.writer(f)
			writer.writerow(info_list)
			print title,star,avg,add,tel,branch
	except Exception, e:
		print e
		

def main():
	map(get_shop_info, get_shop_link())

if __name__ == '__main__':
	main()
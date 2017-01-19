# -*- coding:utf8 -*-
import requests


if __name__ == '__main__':
    url_get_base = "http://api.ltp-cloud.com/analysis/?"
    api_key = '49g5t251rBiB4YHLzcPA2QxDJB9jffqfoRDqVmbW'
    text = '我是中国人。'
    pattern ='all'
    format = 'xml'
    res = requests.get(url_get_base+
                                    "api_key="+api_key+"&"
                                    +"text="+text+"&"
                                    +"format="+format+"&"
                                    +"pattern="+pattern)

    print (res.text)


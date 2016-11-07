# *- coding: utf-8 -*-
import mysql.connector
import datetime
import re
import jieba
import jieba.posseg #需要另外加载一个词性标注模块
import time
import logging
import  codecs



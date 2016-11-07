# *- coding: utf-8 -*-
from os import path
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import mysql.connector
from scipy.misc import imread
import matplotlib.pyplot as plt
import  random
import numpy as np
from PIL import Image

def read_list(usr, pwd, db):
    try:
        conn1 = mysql.connector.connect(user=usr, password=pwd, database=db)
        cursor = conn1.cursor()
        cursor.execute( 'SELECT  word_name,word_times FROM dianping.word_frequency  where word_tag="a" order by word_times DESC  ')
        rows = cursor.fetchall()
        cursor.close()
        conn1.close()
        return  rows
    except BaseException as e:
        print("取评论出问题啦", e)

        return

def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(300, 0%%, %d%%)" % random.randint(60, 100)


###########设置字体不能忘记！！！！！
def main1():
    d = path.dirname(__file__)
    frequencies=read_list('root', '58424716', 'dianping')
    wordcloud = WordCloud(font_path = 'msyh.ttc').fit_words(frequencies)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

#遮罩图片的白色部分将被视作透明,只在非白色部分区域作图
#存取图片的名字
def main2(pic_name):
    d = path.dirname(__file__)
    frequencies = read_list('root', '58424716', 'dianping')
    alice_coloring = imread(path.join(d, pic_name))
    # stopwords = set(STOPWORDS)
    # stopwords.add("的")
    wc = WordCloud(background_color="white",  # 背景颜色max_words=2000,# 词云显示的最大词数
                   max_words=2000,
                   font_path='msyh.ttc',
                   mask=alice_coloring,  # 设置背景图片
                   stopwords=STOPWORDS.add("的"), max_font_size=40,  # 字体最大值
                   random_state=42)
    wc.generate_from_frequencies(frequencies)
    """画图是imshow开头 axis结尾  最后一次性show出来"""
    #从背景图片生成颜色值
    image_colors = ImageColorGenerator(alice_coloring)
    # 以下代码显示图片
    plt.imshow(wc)
    plt.axis("off")
    # 绘制词云
    plt.figure()
    # recolor wordcloud and show
    # we could also give color_func=image_colors directly in the constructor
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis("off")
    # 绘制背景图片为颜色的图片----显示原图
    plt.figure()
    plt.imshow(alice_coloring, cmap=plt.cm.gray)
    plt.axis("off")
    # plt.show()
    # 保存图片
    wc.to_file(path.join(d, "名称.png"))

    plt.figure()
    plt.title("Custom colors")
    plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3))
    wc.to_file("del_a_new_hope.png")
    plt.axis("off")

    plt.show()

main2("hero2.jpg")
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 19:11:02 2021

@author: Shine'lon
"""


import requests
from lxml import etree
def find_animation(wq,answer_titles,answser_urls):
    r=requests.get('https://www.yhdm123.com/video/search/'+wq+'.html')
    # print(r.status_code)
    x=etree.HTML(r.text)
    answser_urls=x.xpath('/html/body/div[1]/div/div[2]/ul[1]/li/a/@href')
    answer_titles=x.xpath('/html/body/div[1]/div/div[2]/ul[1]/li/a/@title')
    # print(answer_titles)
    # for i in range(len(answer_titles)):
    #     title_url[answer_titles[i]]='https://www.yhdm123.com/'+answser_urls[i]
    # print(d)
    #搜索结果列表
    for i in range(len(answer_titles)):
        print(i,': '+answer_titles[i])
    return answer_titles,answser_urls

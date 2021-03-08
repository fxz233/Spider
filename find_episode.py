# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 19:47:23 2021

@author: Shine'lon
"""
import requests
from lxml import etree

def find_episode(ani_url,epi_dict):
    r=requests.get(ani_url)
    # print(r.text)
    x=etree.HTML(r.text)
    epiurls=x.xpath('/html/body/div[1]/div/div[3]/ul/li/a/@href')
    epititles=x.xpath('/html/body/div[1]/div/div[3]/ul/li/a/@title')
    # print(epis)
    epi_max=len(epiurls)
    for i in range(epi_max):
        epi_dict[i+1]=epiurls[i]
    # print(epi_dict)
    return epi_max,epititles
    
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 16:57:05 2021

@author: Shine'lon
"""
import re
import requests
from lxml import etree
from selenium import webdriver
# import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def ts_request(urls_queue,episode_url):#具体集的地址
    
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36','X-Requested-With': 'XMLHttpRequest','connection':'close'}
    r=requests.get(episode_url,headers=header)
    html=r.text
    x=etree.HTML(html)
    temp=x.xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/script[1]/text()')
    temp1=re.search('url.*?(http.*?)/sha.*?',temp[0])
    browser=webdriver.PhantomJS()
    browser.get(episode_url)
 
    browser.switch_to.frame(browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/div[1]/iframe[1]'))
    wait=WebDriverWait(browser,20)#waittime=20s
    while True:
        try :
            # time.sleep(20)
            wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/script[5]')))
            ihtml=browser.page_source
            browser.close()
            # print(ihtml)
            break
        except Exception  as timeout_err:
            print(timeout_err,'请求子页面超时,请检查网络.')
            if_wait=input('是否继续等待(y/n)或者刷新页面(refresh):')
            if if_wait=='y':
                print('loading...')
                # b.refresh()
                continue
            elif if_wait=='refresh':
                browser.refresh()
                continue
            else:
                browser.close()
                print('退出')
                break
    ix=etree.HTML(ihtml)
    base_url=re.sub(r'\\','',temp1.group(1))#播放器域名 http://iqiyi.cdn9-okzy.com
    # print(base_url)
    
    # 获取sign值
    temp2=ix.xpath('/html/body/script[5]/text()')
    # print(temp2)
    temp3=re.search('main.*?"(/.*?sign=.*?)"',temp2[0])
    # print(temp3.group(1))
    
    # 拼接url   
    # http://iqiyi.cdn9-okzy.com/20200628/11819_1c14aed2/index.m3u8?sign=82a754710203b950ca519ffdb147bf5f
    temp4=base_url+temp3.group(1)
    # print(temp4)
    # temp4='http://iqiyi.cdn9-okzy.com/20200628/11819_1c14aed2/index.m3u8?sign=82a754710203b950ca519ffdb147bf5f'

    #获取m3u8地址的后部分
    r2=requests.get(temp4)
    temp5=r2.text
    temp6=re.search('EXT-.*?\n(.*)',temp5)
    temp7=temp6.group(1)
    
    #拼接最终m3u8文件的url
    temp8=re.search('(.*?)index.*',temp4)
    m3u8_url=temp8.group(1)+temp7
    print('m3u8文件地址:',m3u8_url)
    #请求m3u8文件
    r3=requests.get(m3u8_url)
    m3u8_page=r3.text
 
    l=re.findall('EXTINF.*?,\n(.*?ts)\n', m3u8_page,re.S)
    # print(l)
    # ts文件的前缀
    temp9=re.search('(.*?)index.*',m3u8_url)
    temp10=temp9.group(1)
    print('temp10:',temp10)

    #拼接ts文件url
    count=0
    while count<len(l):
        urls_queue.put((count,temp10+l[count]))
        count+=1
   
    return len(l)#文件总数
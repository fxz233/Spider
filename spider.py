# -*- coding: utf-8 -*-
"""
Created on Sat Mar  6 15:13:10 2021

@author: Shine'lon
"""

from download_thread import create_thread,activate_thread
from Download import download
from Ts_request import ts_request
from find_animation import find_animation
from find_episode import find_episode
# import selenium
# from selenium import webdriver
# import time
# from lxml import etree
import queue





def main():
    urls_queue=queue.Queue()#save ts file urls
    # q_lock=threading.Lock()
    buffer_dict={}
    thread_num=0#seq of the thread
    thread_max=50
    wq=''#key world
    epi_dict={}
    answer_titles=[]
    answer_urls=[]
    signal=1
    wq=input('请输入关键词')
    answer_titles,answer_urls=find_animation(wq,answer_titles,answer_urls)#print the seq-ani_title list
    # print(answer_urls)
    wantedani_seq=int(input('请输入想看的动漫对应的序号:'))
    ani_url='https://www.yhdm123.com'+answer_urls[wantedani_seq]
    print(ani_url)
    
    epi_max,epititles= find_episode(ani_url,epi_dict)
    print(answer_titles[wantedani_seq],'共有',epi_max,'集')
    print(epititles)
    start_episode=int(input('从哪一集开始下载:'))
    end_episode=int(input('哪一集结束:'))
    
    epi_seq=start_episode
    
    while epi_seq<=end_episode:
        episode_url='https://www.yhdm123.com'+epi_dict[epi_seq]
        print(episode_url)
        fseq_max=ts_request(urls_queue,episode_url)#fill urls_queue with ts file url
        print('文件数:',fseq_max)
        
        create_thread(thread_num, thread_max, threads,urls_queue,buffer_dict,signal)
        activate_thread(threads)
        
        #download to local
        download(buffer_dict,signal,fseq_max,answer_titles[wantedani_seq],epi_seq)
        epi_seq+=1
        # print(threading.alive_)/ignore
    return
# #------------------------------#
threads=[] #thread pool

try:
    main()
    print('finish')
except KeyboardInterrupt as Interrupted_Error:
    print('程序中断:KeyboardInterrupt',Interrupted_Error)
    for t in threads:
        t.signal=0#end the download_thread

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
from total_time import total_time
import time
import threading
import random
def main(threads):
    urls_queue=queue.PriorityQueue()#save ts file urls maxsize=50
    # q_lock=threading.Lock()
    buffer_dict={}
    thread_num=0#seq of the thread start from 0
    thread_max=50
    wq=''#key world
    epi_dict={}
    answer_titles=[]
    answer_urls=[]
    wq=input('请输入关键词')
    answer_titles,answer_urls=find_animation(wq,answer_titles,answer_urls)#print the seq-ani_title list
    # print(answer_titles)
    if answer_titles:
        # print(answer_urls)
        wantedani_seq=int(input('请输入想看的动漫对应的序号:'))
        ani_url='http://www.yhdm123.com'+answer_urls[wantedani_seq]
        print(ani_url)
        
        epi_max,epititles= find_episode(ani_url,epi_dict)
        print(answer_titles[wantedani_seq],'共有',epi_max,'集')
        print(epititles)
        start_episode=int(input('从哪一集开始下载:'))
        end_episode=int(input('哪一集结束:'))
        
        epi_seq=start_episode
        
        while epi_seq<=end_episode:
            episode_url='http://www.yhdm123.com'+epi_dict[epi_seq]
            print('episode_url :',episode_url)
            fseq_max=ts_request(urls_queue,episode_url)#fill urls_queue with ts file url
            print('文件数:',fseq_max)
            
            create_thread(thread_num, thread_max, threads,urls_queue,buffer_dict,1,retry)# trig signl =1
             #download to local
            dlocal_thread=threading.Thread(target=download,args=(buffer_dict,fseq_max,answer_titles[wantedani_seq],epi_seq,download_signal))
            
            activate_thread(threads)
            dlocal_thread.start()
            #网络拥塞时,减少线程数
            nowork_time=0
            while True:
                if nowork_time<6:
                    old_retry=retry[0]
                    time.sleep(30)
                    if (retry[0]-old_retry>4):
                        random.seed(time.time()) 
                        rand_num2=random.randint(1, 4)
                        for i in range(rand_num2):
                            rand_num=random.randint(0, 50)
                            threads[rand_num].signal=0
                            print('close','thread-',threads[rand_num].num)
                    elif retry[0]==-1:
                        break
                    else:
                        nowork_time+=1
                else:
                    print('调整已关闭')
                    break
            threads=[]
            epi_seq+=1#下一集
    else:
        print('找不到你想看的')
    return



# #------------------------------#
if __name__=='__main__':
    threads=[] #thread pool
    retry=[0]#记录所有重试次数
    download_signal=[1]
    try:
        start_time=time.time()
        main(threads)
        for i in threads:#阻塞主线程
            i.join()
        end_time=time.time()
        total=end_time-start_time
        total_time(start_time,end_time)
        
    except KeyboardInterrupt as Interrupted_Error:
        print('程序中断:KeyboardInterrupt',Interrupted_Error)
        download_signal[0]=0
        for t in threads:
            t.signal=0#end the download_thread

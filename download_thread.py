# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 16:50:32 2021

@author: Shine'lon
"""

import threading
import requests
import time
class DownloadThread(threading.Thread):
    def __init__(self,num,urls_queue,buffer_dict,signal):
        super().__init__(daemon=True)
        self.num=num
        self.urls_queue=urls_queue
        self.buffer_dict=buffer_dict
        self.signal=signal
       
    def run(self):
        print('thread '+str(self.num)+' start')
        while self.signal:
            try:
                ts_list=self.urls_queue.get()
                seq=ts_list[0]#获取序列号
                print(seq,'已取')
                retry=0
                while retry<3:
                    try:
                        r4=requests.get(ts_list[1],timeout=10)#发起请求
                        # print('thread '+str(self.num)+' :'+str(r4.status_code))
                        self.buffer_dict[seq]=r4.content
                        break
                    except Exception as unknownerr:
                        print('状态码:',r4.status_code,'Exception:',unknownerr)
                        time.sleep(4)
                        print('重新尝试')
                        retry+=1
                        continue
                    if retry==3:
                        self.urls_queue.put(ts_list)#尝试次数超过3次,放回未下载地址,退出
                        break#直接退出
            except Exception as queue_err:
                print('队列已空,Exception:',queue_err)
                break
        print('thread '+str(self.num)+' end')
        
#create thread pool
def create_thread(thread_num,thread_max,threads,urls_queue,buffer_dict,signal):
     while thread_num<thread_max:
        t=DownloadThread(thread_num,urls_queue,buffer_dict,signal)
        threads.append(t)
        thread_num+=1
def activate_thread(threads):
    for t in threads:
        t.start()
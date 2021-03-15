# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 16:50:32 2021

@author: Shine'lon
"""

import threading
import requests
import time
class DownloadThread(threading.Thread):
    def __init__(self,num,urls_queue,buffer_dict,signal,retry):
        super().__init__(daemon=True)
        self.num=num
        self.urls_queue=urls_queue
        self.buffer_dict=buffer_dict
        self.signal=signal
        self.retry=retry
    def run(self):
        # print('thread '+str(self.num)+' start')
        while self.signal:
            if not self.urls_queue.empty():
                ts_list=self.urls_queue.get()
                seq=ts_list[0]#获取序列号
                # print(seq,'已取')
                try:
                    # print(ts_list[1])
                    rr=requests.get(ts_list[1],timeout=20)#发起请求
                    # print(ts_list[1])
                    # print('thread '+str(self.num)+' :'+str(r4.status_code))
                    self.buffer_dict[seq]=rr.content
                except Exception as unknownerr:
                    print('Exception:',unknownerr)
                    self.urls_queue.put((seq,ts_list[1]))
                    print('push:',seq)
                    time.sleep(4)
                    # print('重新尝试')
                    self.retry[0]=self.retry[0]+1
                    continue
            else:
                self.retry[0]=-1
                break
        # print('thread '+str(self.num)+' end')
#create thread pool
def create_thread(thread_num,thread_max,threads,urls_queue,buffer_dict,signal,retry):
     while thread_num<thread_max:
        t=DownloadThread(thread_num,urls_queue,buffer_dict,signal,retry)
        threads.append(t)
        thread_num+=1
def activate_thread(threads):
    for t in threads:
        t.start()
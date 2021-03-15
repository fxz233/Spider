# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 16:56:09 2021

@author: Shine'lon
"""

import time
import re
import random
def download(buffer_dict,fseq_max,file_name,epi_seq,download_signal):
    #写入文件
    seq=0
    temp_2=re.sub(r'\\','',file_name)
    temp_3=re.sub('/','',temp_2)
    temp_4=re.sub('!','',temp_3)
    temp_5=re.sub('\?','',temp_4)
    temp_6=re.sub(':','',temp_5)
    temp_7=re.sub(r'\|','',temp_6)
    file_nam=re.sub('\s','',temp_7)
    while seq<fseq_max:
        if download_signal[0]:
            try: 
                with open ('C:\\Users\Shine\'lon\\Desktop\\from spider\\'+file_nam+'第'+str(epi_seq)+'集'+'.mp4','ab')as f:
                    f.write(buffer_dict[seq])
                    buffer_dict.pop(seq)
                    seq+=1
            except KeyError as err:
                print('KeyError:',err)
                random.seed(time.time())
                slptime=random.randint(3,12)
                time.sleep(slptime)
                continue
            except FileNotFoundError as notfileerr:
                print('err:',notfileerr)
                raise KeyboardInterrupt#抛出异常,使线程退出
                break
        else:
            print('中断:退出本地下载')
            break
        
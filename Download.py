# -*- coding: utf-8 -*-
"""
Created on Sun Mar  7 16:56:09 2021

@author: Shine'lon
"""

import time
def download(buffer_dict,signal,fseq_max,file_name,epi_seq):
    #写入文件
    seq=0
    while seq<fseq_max:
        try: 
            with open ('C:\\Users\Shine\'lon\\Desktop\\from spider\\'+file_name+'str(epi_seq)'+'.mp4','ab')as f:
                f.write(buffer_dict[seq])
                seq+=1
        except KeyError as err:
            print('KeyError:',err)
            time.sleep(3)
            continue
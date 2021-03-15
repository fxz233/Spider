# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 09:58:10 2021

@author: Shine'lon
"""


def total_time(st,et):
    tt=et-st
    h=tt//3600
    s=tt%60
    m=(tt-h*3600)//60
    print('finish,total time:%02d h %02d m %02d s'%(h,m,s))

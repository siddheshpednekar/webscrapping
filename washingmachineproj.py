# -*- coding: utf-8 -*-
"""
Created on Sat Mar 27 22:26:40 2021

@author: siddh
"""

import time
start = time.process_time()

from bs4 import BeautifulSoup as bs
from selenium import webdriver
import pandas as pd
import re
import numpy as np


technical_details = pd.DataFrame()
additional_information = pd.DataFrame()
tempratings = []
tempreviews = []
tempprice = []
tempactualprice = []

count_page = 0
count_rows = 0

link='https://www.amazon.in/s?k=washing+machine&qid=1615306641&ref=sr_pg_1'
for j in range(1,11):
    driver=webdriver.Chrome("D:/ds/chromedriver_win32/chromedriver.exe")
    driver.get(link)
    content=driver.page_source
    cont=bs(content)
    for i in cont.find_all('div',attrs={'class':'a-section a-spacing-medium'}):
        try:
            link2 = i.find('a',attrs={'class':'a-size-base a-link-normal s-no-hover a-text-normal'})
            c=link2.attrs
            link3="https://www.amazon.in"+c['href']
            
        
            t1=pd.read_html(link3, attrs={'id':'productDetails_techSpec_section_1'})
            t2=pd.read_html(link3, attrs={'id':'productDetails_detailBullets_sections1'})
        
            tdf1=pd.DataFrame({'row1':t1[0][0],'row2':t1[0][1]})
            tdf2=pd.DataFrame({'row1':t2[0][0],'row2':t2[0][1]})
        
        
            dftrans1 = tdf1.T
            dftrans1.columns=dftrans1.iloc[0]
            newdf1 = dftrans1[1:]
        
            dftrans2 = tdf2.T
            dftrans2.columns=dftrans2.iloc[0]
            newdf2 = dftrans2[1:]
             
            technical_details=pd.concat([technical_details, newdf1])
            additional_information=pd.concat([additional_information, newdf2])
            
            price = i.find('span',attrs={'class':'a-price-whole'})
            actualprice = i.find('span',attrs={'class':'a-price a-text-price'})
            ratings = i.find('div',attrs={'class':'a-row a-size-small'})
             
            
            try:    
                rating=ratings.text
                rating=re.findall(r'\d.\d|\d+',rating)
                reviews=int(rating[-1])
                rating=float(rating[0])
            except:
                rating=None
                reviews=None
            tempratings.append(rating)
            tempreviews.append(reviews)
            
            
            try:
                price=price.text
            except:
                price=None
            tempprice.append(price)
            
            try:
                actualPrice=actualprice.text
                actualPrice = actualPrice.split("₹")
                actualPrice = actualPrice[-1]
            except:
                actualPrice=None
            tempactualprice.append(actualPrice)
            
            count_rows+=1
            print(count_rows)
                
        except Exception as e:
            print(e)
            continue
        
    
    count_page+=1
    print(count_page)
        
for i in range(0, len(tempprice)):
    try:
        tempprice[i]=(int(tempprice[i].replace(',','')))
    except:
        tempprice[i]=None
    try:
        tempactualprice[i]=(int(tempactualprice[i].replace(',','')))
    except:
        tempactualprice[i]=None
        
rrpa = pd.DataFrame({'ratings':tempratings,
                     'reviews:':tempreviews,
                     'price':tempprice,
                     'mrp':tempactualprice})
additional_information.set_index(np.arange(0,len(additional_information)), inplace=True)
technical_details.set_index(np.arange(0,len(technical_details)), inplace=True)
all_details=pd.concat([technical_details,additional_information, rrpa], axis=1)
print(len(tempprice))
print(len(tempactualprice))

all_details.to_excel("washingmachineprojop.xlsx") 
print(time.process_time() - start)
        
        
        
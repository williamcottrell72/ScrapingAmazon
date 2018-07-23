import pickle
import numpy as np
from scipy import stats
import requests
from bs4 import BeautifulSoup
import pandas as pd
from subprocess import call

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

import os

filename='url_data.pkl'

with open('place_codes','rb') as file:
    places=pd.read_csv(file,',')
codes=list(places['usny'].values[:32])+['usny']

chromedriver = "/home/williamcottrell72/Downloads/chromedriver_linux64/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver


flash_urls=[f'https://www.amazon.com/s/ref=sr_pg_{x}?rh=n%3A172282%2Ck%3Ausb+flash+drive+stick&page={x}&keywords=usb+flash+drive+stick&ie=UTF8&qid=1531285754' for x in range(1,400)]
urls=[f'https://www.amazon.com/s/ref=sr_pg_{x}?rh=n%3A2335752011%2Cn%3A%212335753011%2Cn%3A2407755011%2Cn%3A2407774011&page={x}&ie=UTF8&qid=1531254193' for x in range(400)]

#driver = webdriver.Chrome(chromedriver)



def get_urls(soup):
    url_list=[]
    souplist=list(soup.find_all('div',class_="a-row a-spacing-none sx-line-clamp-4"))
    for item in souplist:
        href=item.find_all('a')[0].get('href')
        if href[:4]=='http':
            url_list.append(href)
    return url_list

def full_url_list(urls):
    big_list=[]
    for url in urls:
        driver.get(url)
        soup=BeautifulSoup(driver.page_source,'html.parser')
        big_list.append(get_urls(soup))
    return(big_list)

def flatten1(nested):
    flat=[]
    for x in nested:
        for y in x:
            flat.append(y)
    return flat

def scrape_urls(urls,filename):
    try:
        with open(filename,'rb') as picklefile:
            flat_url_list=pickle.load(picklefile)
    except:
        flat_url_list = flatten1(full_url_list(urls))
        random_list=np.random.permutation(flat_url_list)

        with open(filename,'wb') as picklefile:
            pickle.dump(random_list,picklefile)
    return flat_url_list

def build_df():
    test=1
    x=100
    data=[]
    while test:
        name=f'cache/cache_{x}.pkl'
        try:
            with open(name,'rb') as pkl:
                data_temp=pickle.load(pkl)
            data+=data_temp
            x+=100
        except:
            test=0
            return pd.DataFrame(data,columns=['url','stars','pics','descriptors','desLength','price'])

def fix_row(row):
    return [float(x) for x in list(row)]

def clean_df():
    df=build_df()
    clean1=df.dropna().drop(columns=['url'])
    clean2=[]
    for i in range(clean1.shape[0]):
        try:
            clean_row=[fix_row(clean1.iloc[i])]
            clean2+=clean_row
        except:
            pass
    return pd.DataFrame(clean2,columns=['stars','pics','descriptors','desLength','price'])





#Now we need to specify the location of particular objects we are interested in.

def get_price(soup):
    try:
        return soup.find_all('span',id='priceblock_ourprice')[0].text[1:]
    except(IndexError):
        pass

def get_picNumber(soup):
    try:
        return len(soup.find_all('input',class_='a-button-input'))
    except:
        pass

def get_descriptors(soup):
    try:
        comments1=soup.find_all('div',id="featurebullets_feature_div")
        comments2=comments1[0].find_all('ul',class_="a-unordered-list a-vertical a-spacing-none")
        return len(comments2[0].find_all('li'))
    except(IndexError):
        pass

def get_desLength(soup):
    try:
        title_string=soup.find_all('span',id="productTitle")[0].text
        true_len=0
        for x in list(title_string):
            if (x!='\n') and (x!=' '):
                true_len+=1
        return true_len
    except:
        pass

def get_stars(soup):
    try:
        return float(soup.find_all('span',class_='arp-rating-out-of-text')[0].text[:3])
    except(IndexError):
        pass


def get_data(flat_urls,codes=codes):
    data=[]
    tmp=[]
    ct=1
    os.system("mkdir data_cache")
    for url in flat_urls:
        driver.get(url)
        soup=BeautifulSoup(driver.page_source,'html.parser')
        try:
            stars=get_stars(soup)
        except(NameError):
            pass
        try:
            price=get_price(soup)
        except(NameError):
            pass
        try:
            pics=get_picNumber(soup)
        except(NameError):
            pass
        try:
            descriptors=get_descriptors(soup)
        except(NameError):
            pass
        try:
            desLength=get_desLength(soup)
        except(NameError):
            pass
        data_element=[url,stars,pics,descriptors,desLength,price]
        data.append(data_element)
        tmp.append(data_element)
        x=stats.gamma.ppf(np.random.rand(1)[0],.5)
        time.sleep(x)

        if (ct%100==0):
            with open(f'data_cache/cache_{ct}.pkl','wb') as picklefile:
                pickle.dump(tmp,picklefile)
            tmp=[]
            os.system("expressvpn disconnect")
            time.sleep(10)
            command="expressvpn connect "+np.random.choice(codes)
            os.system(command)
            time.sleep(20)
        print(ct)
        ct+=1
    return data

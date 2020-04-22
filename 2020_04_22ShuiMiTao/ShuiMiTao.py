#爬取水蜜桃首页多套图片
#爬取水蜜桃首页指定套图
#爬取水蜜桃图库指定套图
#网页使用Ajax，但手动输入时无用
#此项目直接采用模拟方法,使用selenium
import requests
import bs4
from selenium import webdriver
import re
import os
import time


def GetHtml(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Referer": "https://www.baidu.com/"}
    try:
        response=requests.get(url,headers=headers)
        response.raise_for_status()
        response.encoding=response.apparent_encoding
        return response.text
    except:
        return None

def CreateDirectory(path):
    if(os.path.exists(path)):
        print('文件夹已存在')
    else:
        os.mkdir(path)
        print('文件夹创建成功')

def FindJpgUrl(html,JpgUrlList):
    soup=bs4.BeautifulSoup(html,'html.parser')
    for t in soup.find_all('a'):
        if isinstance(t,bs4.element.Tag):
            if('href' in t.attrs):
                if re.match(r'/article/\d*/',t.attrs['href']):
                    print(t.attrs['href'])

if __name__=='__main__':
    JpgUrlList=[]
    url='https://smtmm.win'
    html=GetHtml(url)
    FindJpgUrl(html,JpgUrlList)

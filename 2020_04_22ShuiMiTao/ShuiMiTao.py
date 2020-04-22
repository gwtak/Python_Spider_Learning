#爬取水蜜桃首页多套图片
#爬取水蜜桃首页指定套图
#爬取水蜜桃图库指定套图
#原网页https://smtmm.win/#/?page=1
#使用Ajax,laxy load
#仅在首页进行JS渲染
#障眼法，不输入‘#’
#直接输入https://smtmm.win/?page=2
#可以完成任意页面的跳跃
#懒得写了
import requests
import bs4
import re
import os
import time


def GetHtml(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Referer": "https://smtmm.win/"}
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
                    #print(t.attrs['href'])
                    JpgUrlList.append(t.attrs['href'])

def DeleteRepetiton(JpgUrlList):
    for i in range(len(JpgUrlList)-1):
        #print(JpgUrlList[i])
        if(JpgUrlList[i]==JpgUrlList[i+1]):
            JpgUrlList[i+1]=None

def JumpToJpgPage(url,path):
    print(url)
    CreateDirectory(path)
    html = GetHtml(url)
    num=1
    soup=bs4.BeautifulSoup(html,'html.parser')
    for t in soup.find_all('a'):
        if isinstance(t,bs4.element.Tag):
            if('href' in t.attrs):
                print(t)
                '''
                if re.match(r'/static/images/\S*\.jpg',t.attrs['href']):
                    DowmloadJpg('https://smtmm.win'+t.attrs['href'],path,num)
                    num=num+1
                    '''

def DowmloadJpg(url,path,num):
    try:
        r=requests.get(url)
        r.raise_for_status()
        with open(path+str(num),'wb') as f:
            f.write(r.content)
            f.close()
    except:
        print('一套图片已完成')

if __name__=='__main__':
    JpgUrlList=[]
    path='pics/'
    url='https://smtmm.win/#/?page=2'
    html=GetHtml(url)
    #print(html)
    FindJpgUrl(html,JpgUrlList)
    DeleteRepetiton(JpgUrlList)
    print('输入‘1’：爬取首页多套图片')
    print('输入‘2’：爬取首页指定套图')
    print('输入‘3’：爬取指定网页套图')
    n = input()
    if (n == '1'):
        print('输入套图数量')
        m = input()
        i = -1
        while (int(m)):
            i = i + 1
            while (JpgUrlList[i] == None):
                i = i + 1
            JumpToJpgPage(url + JpgUrlList[i], path)
            m = int(m) - 1
    elif (n == '2'):
        print('输入要爬取的序号')
        m = input()
        i = -1
        while (int(m)):
            i = i + 1
            while (JpgUrlList[i] == None):
                i = i + 1
            m = int(m) - 1
        JumpToJpgPage(url + JpgUrlList[i], path)
    elif (n == '3'):
        print('输入网址')
        url = input()
        JumpToJpgPage(url, path)
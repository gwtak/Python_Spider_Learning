#爬取水蜜桃首页多套图片
#爬取水蜜桃首页指定套图
#爬取水蜜桃图库指定套图
#原网页https://smtmm.win/#/?page=1
#使用Ajax,laxy load
#仅在首页进行JS渲染
#障眼法，不输入‘#’
#直接输入https://smtmm.win/?page=1
#可以完成任意页面的跳跃
import requests
import bs4
import re
import os
import time


def GetHtml(url):
    print(url)
    try:
        response=requests.get(url)
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
    soup=bs4.BeautifulSoup(html,'html.parser')
    for t in soup.find_all('title'):
        if isinstance(t,bs4.element.Tag):
            path=path+re.match(r'[\u4e00-\u9fa5]*',t.text).group(0)+'/'
            CreateDirectory(path)
    num = 1
    for t in soup.find_all('img'):
        if isinstance(t,bs4.element.Tag):
            if('data-original' in t.attrs):
                #print(t.attrs['data-original'])
                if re.match(r'/static/images/\S*\.jpg',t.attrs['data-original']):
                    DownloadJpg('https://smtmm.win'+t.attrs['data-original'],path,num)
                    num=num+1

def DownloadJpg(url,path,num):
    print(url)
    try:
        r=requests.get(url)
        r.raise_for_status()
        with open(path+str(num)+'.jpg','wb') as f:
            f.write(r.content)
            f.close()
        print('一张图片已完成')
    except:
        print('一套图片已完成')

def Select(path):
    url='https://smtmm.win'
    url_page='https://smtmm.win/?page='
    print('输入‘1’，爬取多套图片')
    print('输入‘2’，爬取指定套图')
    print('输入‘3’，爬取网页套图')
    c=input()
    list=[]
    if(c=='1'):
        print('输入套图数量')
        num=input()
        page = int((int(num) - 1) / 10 + 1)  # 避免float类型
        for p in range(int(page)):
            html = GetHtml(url_page + str(p+1))
            FindJpgUrl(html, list)
            DeleteRepetiton(list)
        count=-1
        for i in range(int(num)):
            count=count+1
            while(list[count]==None):
                count=count+1
            JumpToJpgPage(url+list[count],path)
            i=i+1
    elif(c=='2'):
        print('输入套图序号')
        num = input()
        page = int((int(num) - 1) / 10 + 1)  # 避免float类型
        num = int(num) % 10
        html = GetHtml(url_page + str(page))
        FindJpgUrl(html, list)
        DeleteRepetiton(list)
        count = -1
        for i in range(num):
            count = count + 1
            while (list[count] == None):
                count = count + 1
            JumpToJpgPage(url + list[count], path)

    elif(c=='3'):
        print('输入套图网页')
        u=input()
        JumpToJpgPage(u,path)

if __name__=='__main__':
    path='pics/'
    Select(path)
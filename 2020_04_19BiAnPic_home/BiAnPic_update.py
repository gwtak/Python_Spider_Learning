#爬取较为清晰的图片
import requests
import bs4
import os
import re
import time


def GetHtml(url):#获取html
    try:
        response=requests.get(url)
        response.raise_for_status()
        response.encoding=response.apparent_encoding
        return response.text
    except:
        return ""

def CreateDirectory(path):#创建文件夹
    if os.path.exists(path):
        print('文件夹已存在')
    else:
        os.mkdir(path)
        print('文件夹创建成功')

def FindJpgUrl(html,list):#在主页查找图片链接(封面)
    count=0;#当前页面只有21张封面，防止出错
    soup=bs4.BeautifulSoup(html,'html.parser')
    for t in soup.find_all('a'):
        if isinstance(t,bs4.element.Tag):
            if(('href' in t.attrs)and('target' in t.attrs)and(not re.match(r'http*',t.attrs['href']))):
                list.append(t.attrs['href'])
                #print(count,t.attrs['href'])
                if(count==20):return 0
                else:count=count+1

def DownJpg(url,html,path):#下载清晰图片(非封面)
    soup=bs4.BeautifulSoup(html,'html.parser')
    for t in soup.find_all('img'):
        if isinstance(t,bs4.element.Tag):
            if(('alt' in t.attrs)and('data-pic' in t.attrs)and('src' in t.attrs)and('title' in t.attrs)):
                #print(t)
                r=requests.get(url+t.attrs['src'])
                with open(path+t.attrs['alt']+'.jpg','wb') as f
                    f.write(r.content)
                    f.close()
                print('一个文件保存成功')
                #time.sleep(1)


def JumpToJpgPage(url,list,path):#跳转到图片页面
    for p in list:
        html=GetHtml(url+p)
        print(url+p)
        DownJpg(url,html,path)

if __name__=='__main__':
    list=[]
    end_1 = '/index_'
    end_2 = '.html'
    url='http://pic.netbian.com'
    path='pics_update/'
    CreateDirectory(path)
    html=GetHtml(url)
    FindJpgUrl(html,list)
    for i in range(2,3):#页数,第一页与后面几页的链接不一样
        html=GetHtml(url+end_1+str(i)+end_2)
        FindJpgUrl(html,list)
    JumpToJpgPage(url, list, path)
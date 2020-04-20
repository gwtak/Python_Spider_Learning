#爬取美图录首页多套图片
#爬取美图录首页指定套图
#爬取美图录图库指定套图
import requests
import bs4
import re
import os
import time

def GetHtml(url):
    try:
        response=requests.get(url)
        response.raise_for_status()
        response.encoding=response.apparent_encoding
        return response.text
    except:
        return ""

def CreateDirectory(path):#创建文件夹
    if(os.path.exists(path)):
        print('文件夹已存在')
    else:
        os.mkdir(path)
        print('文件夹创建成功')

def FindJpg(html,JpgUrlList):#查找封面
    soup=bs4.BeautifulSoup(html,'html.parser')
    for t in soup.find_all('a'):
        if isinstance(t,bs4.element.Tag):
            if(('href' in t.attrs)and('target' in t.attrs)):
                if(re.match(r'https\:\/\/www\.meitulu\.com\/item\/\d{1,5}\.html',t.attrs['href'])):
                    #print(t.attrs['href'])
                    JpgUrlList.append(t.attrs['href'])

def DeleteRepetition(JpgUrlList):#重复链接置None
    for i in range(len(JpgUrlList)-1):
        if(JpgUrlList[i]==JpgUrlList[i+1]):
            JpgUrlList[i+1]=None

def JumpToJpgPage(url):#跳转jpg页面，提取图片名字、图片编号
    html=GetHtml(url)
    soup=bs4.BeautifulSoup(html,'html.parser')
    path='pics/'
    CreateDirectory(path)
    for t in soup.find_all('title'):
        if isinstance(t,bs4.element.Tag):
            path=path+t.string+'/'
            CreateDirectory(path)
    num=re.search(r'\d{1,5}',url).group(0)
    #print(num)
    DownloadJpg(num,path)

def DownloadJpg(num,path):#下载图片，直接进入图库，不模拟翻页动作
    i=1
    #print(num)
    #print(path)
    while 1:
        url = 'https://mtl.gzhuibei.com/images/img/' + str(num) + '/' + str(i) + '.jpg'
        print(url)
        try:
            r=requests.get(url)
            #print(r.status_code)
            r.raise_for_status()
            with open(path+str(i)+'.jpg','wb') as f:#字符串拼接时，要格外注意类型，str与int无法拼接，当其在try/except中时，不会报错，但会直接退出，难以发现
                f.write(r.content)
                f.close()
            print('一张图片已完成')
        except:
            print('一套图片已完成')
            return
        i = i + 1
        #time.sleep(1)#避免干扰服务器正常运行


if __name__=='__main__':
    print('输入‘1’：首页多套图爬取')
    print('输入‘2’：首页指定套图爬取')
    print('输入‘3’：图库指定编号爬取')
    k=input()
    JpgUrlList=[]
    url='https://www.meitulu.com'
    html=GetHtml(url)
    FindJpg(html,JpgUrlList)
    DeleteRepetition(JpgUrlList)
    if(k=='1'):
        print('输入爬取套数：(<=36)')
        n=input()
        i = -1
        for count in range(int(n)):
            i = i + 1
            while (JpgUrlList[i] == None):
                i = i + 1
            JumpToJpgPage(JpgUrlList[i])
    elif(k=='2'):
        print('指定第几套：(<=36)')
        n = input()
        i = -1
        while (int(n)):
            i = i + 1
            while (JpgUrlList[i] == None):
                i = i + 1
            n = int(n) - 1
        JumpToJpgPage(JpgUrlList[i])
    elif(k=='3'):
        print('输入要爬取的图片编号：')
        n=input()
        JumpToJpgPage('https://www.meitulu.com/item/'+n+'.html')



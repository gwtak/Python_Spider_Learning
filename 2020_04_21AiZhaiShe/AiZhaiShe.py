#爬取爱宅社首页多套套图
#爬取爱宅社首页指定套图
#爬取指定网页套图
#下载速度有时会很慢，怀疑被检测，待优化
import requests
import bs4
import re
import os
import time

def GetHtml(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Referer": "https://www.baidu.com/"
    }
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
                #print(t.attrs['href'])
                if(re.match(r'/\w*/\d*/\d*/\d*\.html',t.attrs['href'])):
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
    html=GetHtml(url)
    soup=bs4.BeautifulSoup(html,'html.parser')
    for t in soup.find_all('title'):
        if isinstance(t,bs4.element.Tag):
            path=path+t.text+'/'
            CreateDirectory(path)
            break
    i=2
    num = 1
    while(html):
        for t in soup.find_all('img'):
            if isinstance(t, bs4.element.Tag):
                if (('src' in t.attrs) and ('alt' in t.attrs)):
                    #if re.match(r'https://www\.images\.zhaofulipic\.com:\S*\.jpg', t.attrs['src']):
                        #print(t.attrs['src'])
                        DownloadJpg(t.attrs['src'], path,num)
                        num = num + 1
        print('re=', re.match(r'https://uc6gu.com/\w*/\d*/\d*/\d*', url).group(0) + '_' + str(i) + '.html')
        html = GetHtml(re.match(r'https://uc6gu.com/\w*/\d*/\d*/\d*', url).group(0) + '_' + str(i) + '.html')
        soup = bs4.BeautifulSoup(html, 'html.parser')
        i = i + 1
    print('已保存一套图片')

def DownloadJpg(url,path,num):
    try:
        print(url)
        r=requests.get(url)
        r.raise_for_status()
        with open(path+str(num)+'.jpg','wb') as f:
            f.write(r.content)
            f.close()
        print('一张图片已保存')
        #time.sleep(0.5)#防止干扰服务器运行被发现
    except:
        return

if __name__=='__main__':
    JpgUrlList=[]
    url='https://uc6gu.com'
    path='pics/'
    html=GetHtml(url)
    FindJpgUrl(html,JpgUrlList)
    DeleteRepetiton(JpgUrlList)
    print('输入‘1’：爬取首页多套图片')
    print('输入‘2’：爬取首页指定套图')
    print('输入‘3’：爬取指定网页套图')
    n=input()
    if(n=='1'):
        print('输入套图数量')
        m=input()
        i=-1
        while(int(m)):
            i=i+1
            while(JpgUrlList[i]==None):
                i=i+1
            JumpToJpgPage(url+JpgUrlList[i],path)
            m=int(m)-1
    elif(n=='2'):
        print('输入要爬取的序号')
        m=input()
        i=-1
        while(int(m)):
            i=i+1
            while (JpgUrlList[i] == None):
                i = i + 1
            m=int(m)-1
        JumpToJpgPage(url + JpgUrlList[i], path)
    elif(n=='3'):
        print('输入网址')
        url=input()
        JumpToJpgPage(url,path)

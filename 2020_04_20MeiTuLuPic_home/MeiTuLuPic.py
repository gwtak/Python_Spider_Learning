import  requests
import bs4
import re
import os

def GetHtml(url):
    try:
        response=requests.get(url)
        response.raise_for_status()
        response.encoding=response.apparent_encoding
        return response.text
    except:
        return ""

def FindJpg(html,JpgUrlList):
    soup=bs4.BeautifulSoup(html,'html.parser')
    for t in soup.find_all('a'):
        if isinstance(t,bs4.element.Tag):
            if(('href' in t.attrs)and('target' in t.attrs)):
                if(re.match(r'https\:\/\/www\.meitulu\.com\/item\/\d{5}\.html',t.attrs['href'])):
                    #print(t.attrs['href'])
                    JpgUrlList.append(t.attrs['href'])

def DeleteRepetition(JpgUrlList):#重复链接置None
    for i in len(JpgUrlList)-1:
        if(JpgUrlList[i]==JpgUrlList[i+1]):
            JpgUrlList[i+1]=None

def JumpToJpgPage(url):


def DownloadJpg(url,path):


if __name__=='__main__':
    #print('爬取主页几套图片:(<=36)')
    n=input()
    JpgUrlList=[]
    url='https://www.meitulu.com'
    html=GetHtml(url)
    FindJpg(html,JpgUrlList)
    DeleteRepetition(JpgUrlList)
    i=0
    for count in range(n):
        while(JpgUrlList[i]==None):
            i=i+1
        path=JumpToJpgPage(JpgUrlList[i])
        CreateDirectory(path)
        DownloadJpg(url,path)
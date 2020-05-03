#javbus首页多套av封面和预览图
#javbus首页指定av封面和预览图
#javbus指定页面av封面和预览图
#使用ajax加载磁力链接
#分析ajax获取磁力链接
import bs4
import re
import requests
import os

def CreateDirectory(path):
    if(os.path.exists(path)):
        print('文件夹已存在')
    else:
        os.mkdir(path)
        print('文件夹创建成功')

def GetHtml(url):
    try:
        response=requests.get(url)
        response.raise_for_status()
        response.encoding=response.apparent_encoding
        return response.text
    except:
        return None

def FindUrl(html,list,url):
    soup=bs4.BeautifulSoup(html,'html.parser')
    for t in soup.find_all('a'):
        if isinstance(t,bs4.element.Tag):
            if('href' in t.attrs):
                if re.match(url+r'\w*-\d*',t.attrs['href']):
                    #print(t.attrs['href'])
                    list.append(t.attrs['href'])


def Select(path):
    print('输入‘1’，爬取首页多套项目')
    print('输入‘2’，爬取首页指定项目')
    print('输入‘3’，爬取指定网页项目')
    c=input()
    list = []
    url='https://www.javbus.icu/'#javbus网址
    if(c=='1'):
        print('请输入要爬取的项目数量<=30')
        num=input()
        html=GetHtml(url)
        FindUrl(html,list,url)
        for i in range(int(num)):
            Search(list[i],path)
    elif((c=='2')):
        print('请输入要爬取的序号>0')
        num = input()
        if(int(num)>30):
            page=int((int(num)-1)/30)+1
            num=int(num)%30
            #print(n)
            page_url='https://www.javbus.icu/page/'+str(page)
            html = GetHtml(page_url)
            FindUrl(html, list, url)
            #print(len(list))
            Search(list[int(num)-1], path)
        else:
            html = GetHtml(url)
            print(html)
            FindUrl(html, list, url)
            Search(list[int(num) - 1], path)
    elif(c=='3'):
        print('请输入要爬取的网页')
        input_url=input()
        Search(input_url,path)

def Search(url,path):
    print(url)
    html = GetHtml(url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    for t in soup.find_all('title'):
        if isinstance(t,bs4.element.Tag):
            print(t.text)
            path=path+t.text+'/'
            CreateDirectory(path)
    for t in soup.find_all('img'):
        if isinstance(t,bs4.element.Tag):
            if('src' in t.attrs):
                if re.match(r'https://pics.javcdn.pw/cover/\S*\.jpg',t.attrs['src']):
                    # print(t.attrs['src'])
                    DownloadJpg(t.attrs['src'], path + '封面.jpg')
    i = 1
    for t in soup.find_all('a'):
        if isinstance(t,bs4.element.Tag):
            if('href' in t.attrs):
                #print(t.attrs['href'])
                if re.match(r'https://pics.dmm.co.jp/digital/video/\S*\.jpg',t.attrs['href']):
                    DownloadJpg(t.attrs['href'], path+str(i)+'.jpg')
                    i=i+1
    print('预览图下载完成')


def DownloadJpg(url,path):
    r=requests.get(url)
    print(path)
    with open(path,'wb')as f:
        f.write(r.content)
        f.close()
    print('一个文件下载成功')

if __name__=='__main__':
    path='index/'
    CreateDirectory(path)
    n=Select(path)

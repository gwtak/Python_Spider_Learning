#面向对象：类的尝试
#class base(url)、def CreateDirectory(path)、def DownloadJpg(url,path,name)可复用
import os
import bs4
import re
import requests
import time

#网页类
class base():
    def __init__(self,url):
        self.url=url
        self.html=self.GetHtml(url)
        self.title=self.Title()
        print(url)
        print(self.title)

    #获取html
    def GetHtml(self,url):
        try:
            response=requests.get(url)
            response.raise_for_status()
            response.encoding=response.apparent_encoding
            return response.text
        except:
            return ''

    #查找所需要的url
    #输入参数：标签名、属性名、正则表达式
    def FindUrl(self, tag, attr, re_str):
        m_list=[]
        soup = bs4.BeautifulSoup(self.html, 'html.parser')
        for t in soup.find_all(tag):
            if isinstance(t, bs4.element.Tag):
                if (attr in t.attrs):
                    if (re.match(re_str, t.attrs[attr])):
                        #print(t.attrs[attr])
                        m_list.append(t.attrs[attr])
        return list(set(m_list))#删除重复的url

    #网页标题
    def Title(self):
        soup=bs4.BeautifulSoup(self.html, 'html.parser')
        t=soup.find(name='title')
        return t.text

#创建文件夹
def CreateDirectory(path):
    if(os.path.exists(path)):
        print('文件夹已存在')
    else:
        os.mkdir(path)
        print('文件夹创建成功')

#图片下载
def DownloadJpg(url,path,name):
    print(url)
    try:
        r=requests.get(url)
        r.raise_for_status()
        with open(path+str(name)+'.jpg','wb') as f:
            f.write(r.content)#r.content：二进制网页内容
            f.close()
        print('一张图片已完成')
    except:
        print('一套图片已完成')



if __name__=='__main__':
    url="https://www.nvshens.net"
    path='pics/'
    CreateDirectory(path)
    print('输入‘1’，爬取指定套图')
    print('输入‘2’，爬取所给网页')
    choice=input()
    if(choice=='1'):
        print('输入套图序号')
        num=input()
        num=int(num)
        page=int(num/20)
        num=num%20
        if(page):
            select_page = base(url+'/gallery/'+str(page-1)+'.html')
        else:
            select_page=base(url+'/gallery')
        url_list = select_page.FindUrl('a', 'href', r'/g/\d*/')
        jpg_page=base(url+url_list[num-1])
        base_url=jpg_page.url
        path=path + jpg_page.title+'/'
        CreateDirectory(path)
        i=1
        name=0
        while(1):
            jpg_list = jpg_page.FindUrl('img','src',r'https://(t1|img)\.onvshen\.com:85/\S*\.jpg')
            for t in jpg_list:
                time.sleep(1)#下载速度实在是太快了，节制一点
                DownloadJpg(t,path,name)
                name = name + 1
            i=i+1
            jpg_page=base(base_url+str(i)+'.html')
            if(jpg_page.title=='该页面未找到-宅男女神'):break

    elif(choice=='2'):
        print('输入套图网页')
        jpg_url=input()
        jpg_page = base(jpg_url)
        base_url = jpg_page.url
        path = path + jpg_page.title + '/'
        CreateDirectory(path)
        i = 1
        name = 0
        while (1):
            jpg_list = jpg_page.FindUrl('img', 'src', r'https://(t1|img)\.onvshen\.com:85/\S*\.jpg')
            for t in jpg_list:
                time.sleep(1)  # 下载速度实在是太快了，节制一点
                DownloadJpg(t, path, name)
                name = name + 1
            i = i + 1
            jpg_page = base(base_url + str(i) + '.html')
            if (jpg_page.title == '该页面未找到-宅男女神'): break
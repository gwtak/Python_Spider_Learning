#仅爬取封面
import time
import requests
import os
import bs4

def GetHtml(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding=response.apparent_encoding
        return response.text
    except:
        return ""

def CreateDirectory(path):
    if os.path.exists(path):
        print('文件夹已存在')
    else:
        os.mkdir(path)
        print('文件夹创建成功')


def FindJpg(html,url,path):
    soup=bs4.BeautifulSoup(html,'html.parser')
    count=0
    for t in soup.find_all('img'):
        if(isinstance(t,bs4.element.Tag)and('src' in t.attrs)):
            path_tmp = path + t.attrs['alt'] + '.jpg'
            url_tmp = url + t.attrs['src']
            print(url_tmp)
            r = requests.get(url_tmp)
            with open(path_tmp, 'wb') as f:
                f.write(r.content)
                f.close()
                print('一个文件保存成功')
                #time.sleep(1)
                if(count==20):return 0#一个页面有21张图片
                else:count=count+1


if __name__=='__main__':
    url='http://pic.netbian.com'
    end_1='/index_'
    end_2='.html'
    path='pics/'
    CreateDirectory(path)
    html = GetHtml(url)
    FindJpg(html, url, path)
    for i in range(2,3):#页数
        html=GetHtml(url+end_1+str(i)+end_2)
        FindJpg(html,url,path)

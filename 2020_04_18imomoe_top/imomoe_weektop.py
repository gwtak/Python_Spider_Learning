#爬取樱花动漫-日本动漫一周排行榜
import requests
import bs4
import re

def GetHtmlText(url):
    try:
        response = requests.get(url)
        response.encoding=response.apparent_encoding#编码
        response.raise_for_status()
        return response.text
    except:
        return ""

def FillList(list,html):
    soup=bs4.BeautifulSoup(html,"html.parser")
    for u in soup.find_all('a'):
        if(re.match(r'.view*',u.attrs['href'])):
            list.append(u.attrs['title'])

def PrintList(list,num):
    for i in range(num):
        print(i+1,list[i])

if __name__=="__main__":
    list=[]
    url="http://www.imomoe.in/top/hottv.html"
    html=GetHtmlText(url)
    FillList(list,html)
    PrintList(list,100)

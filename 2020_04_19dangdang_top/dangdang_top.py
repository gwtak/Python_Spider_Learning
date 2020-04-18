#爬取当当网当日图书畅销榜
import bs4
import requests


def GetHtmlText(url):
    try:
        response=requests.get(url)
        response.raise_for_status()
        return response.text
    except:
        return ""

def FillList(book,html):
    soup=bs4.BeautifulSoup(html,"html.parser")
    for t in soup.find_all('img'):
        if(isinstance(t,bs4.element.Tag)):
            if('alt' in t.attrs):
                book.append(t.attrs['alt'])

def PrintList(book,num):
    for i in range(num):
        print(book[i])

if __name__=='__main__':
    writer=[]
    price=[]
    url='http://bang.dangdang.com/books/bestsellers/1-'
    for i in range(1,5):
        book = []
        html=GetHtmlText(url+str(i))
        FillList(book,html)
        PrintList(book,20)
import re
import requests
import os
import bs4

def GetHtml(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except:
        return ""

def FindJpg(html):
    soup=bs4.BeautifulSoup(html)
    for t in soup.find_all('img'):
        if(isinstance(t,bs4.element.Tag)):
            if('src' in t.attrs):
                

#def SaveJpg():


if __name__=='__main__':
    url='http://pic.netbian.com/'
    html=GetHtml(url)

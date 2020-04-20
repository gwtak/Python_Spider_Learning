import requests
import bs4
import os

def GetHtml(url):
    try:
        response=requests.get(url)
        response.raise_for_status()
        response.encoding=response.apparent_encoding
        return response.text
    except:
        return ""

def FindJpgUrl(html,JpgUrlList):


if __name__=='__main__':
    JpgUrlList=[]
    url='https://uc6gu.com'
    html=GetHtml(url)
    FindJpgUrl(html,JpgUrlList)

    print(html)
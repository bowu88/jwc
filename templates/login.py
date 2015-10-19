# -*- coding:utf-8 -*-
import requests
from StringIO import StringIO
import urllib
from bs4 import BeautifulSoup
from PIL import Image

ctgu_request = requests.session()
url = "http://210.42.38.26:84/jwc_glxt/"
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Host':'210.42.38.26:84',
    'Upgrade-Insecure-Requests':1,
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    }

r = ctgu_request.get(url,headers=headers)

page = r.text

def bs(page,tag,name):
    soup = BeautifulSoup(page)
    soup_result = soup.find(attrs={tag:name})
    return soup_result['value']

__VIEWSTATE =  bs(page,'name','__VIEWSTATE')
__EVENTVALIDATION =  bs(page,'name','__EVENTVALIDATION')


def getImage(cookie):
    url = "http://210.42.38.26:84/jwc_glxt/ValidateCode.aspx"
    imgHeaders = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'210.42.38.26:84',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Cookie':'ASP.NET_SessionId='+cookie
    }

    r = ctgu_request.get(url,headers = imgHeaders)
    i = Image.open(StringIO(r.content)).save('test.jpg')


def login(__VIEWSTATE,__EVENTVALIDATION,cookie):
    headers = {
        'Cookie':'ASP.NET_SessionId='+cookie,
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Origin':'http://210.42.38.26:84',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'210.42.38.26:84',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Referer': 'http://210.42.38.26:84/jwc_glxt/Login.aspx?xttc=1'
    }

    # headers = dict(headers)
    CheckCode = raw_input('please input code')
    print CheckCode
    form = {
        '__VIEWSTATE':__VIEWSTATE,
        'txtUserName':2012136121    ,
        'btnLogin.x': 0,
        'btnLogin.y': 0,
        'txtPassword':'uniquedream456',
        'CheckCode':CheckCode,
        '__EVENTVALIDATION':__EVENTVALIDATION
    }
    data = urllib.urlencode(form)
    login_url = "http://210.42.38.26:84/jwc_glxt/Login.aspx?xttc=1"
    result = ctgu_request.post(login_url,headers=headers,data=data)




def getGrade(cookie):
    headers = {
        'Cookie':'ASP.NET_SessionId='+cookie,
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Origin':'http://210.42.38.26:84',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Host':'210.42.38.26:84',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Upgrade-Insecure-Requests':1,
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Referer': 'http://210.42.38.26:84/jwc_glxt/Login.aspx?xttc=1'
    }

    Grade_url = 'http://210.42.38.26:84/jwc_glxt/Student_Score/Score_Query.aspx'
    result  = ctgu_request.get(Grade_url,headers=headers)
    if result:
        soup = BeautifulSoup(result.text)
        tr_title = soup.find(attrs={'class':'HeaderStyle'})
        # print tr_title

        tr_chengji = tr_title.find_next_siblings()

        for child in tr_chengji[0].children:
            print child
    #     print tr_chengji[0]
    else:
        print 'error'



def logOut():
    logOut_url = 'http://210.42.38.26:84/jwc_glxt/Login.aspx?xttc=1'
    page = ctgu_request.get(logOut_url,headers=headers).text
    # print page

if __name__ == '__main__':
    getImage(r.cookies['ASP.NET_SessionId'])
    login(__VIEWSTATE,__EVENTVALIDATION,r.cookies['ASP.NET_SessionId'])

    try:
        getGrade(r.cookies['ASP.NET_SessionId'])
    except:
        pass
    finally:
        logOut()
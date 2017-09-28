#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Jarod Zheng'

'''
Get Baidu Download URL
'''

import argparse
import http.cookiejar
import urllib.request, urllib.parse, urllib.error
import random  
import re  



import json
import distutils.spawn
import subprocess


class Parser(object):
    def __init__(self, url):

        # Check URL format starts with "pan.baidu.com".
        if not url.find('pan.baidu.com'):
            raise Exception('-->>> URL must contain https://pan.baidu.com.')

        self.url = url
        print (self.url)

        self.fn = ''
        self.fs_id = ''
        self.share_uk = ''
        self.share_id = ''
        self.share_timestamp = ''
        self.share_sign = ''
        self.html = ''
        self.m = ''
        self.dlink = ''



        my_headers = [  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36", # 本机 Chrome
                        "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A365 Safari/600.1.4", # IOS Safari
                        "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/40.0.2214.69 Mobile/12A365 Safari/600.1.4", # IOS Chrome
                        "Mozilla/5.0 (Linux; Android 4.4.4; HTC D820u Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.89 Mobile Safari/537.36", # Android Chrome
                        "Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; HTC D820u Build/KTU84P) AppleWebKit/534.24 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.24 T5/2.0 baidubrowser/5.3.4.0 (Baidu; P1 4.4.4)" # Android 百度浏览器

        ]

        random_header = random.choice(my_headers)  
      
 
        req = urllib.request.Request(self.url)  
        req.add_header("User-Agent", "Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12A365 Safari/600.1.4")  
        #req.add_header("GET",self.url)  
        #req.add_header("Host","pan.baidu.com")  
        #req.add_header("Referer","https://pan.baidu.com/share/init?surl=jH4KE38") 
        

        #req.add_header("Accept","text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        #req.add_header("Accept-Encoding","gzip, deflate, sdch, br")
        #req.add_header("Accept-Language","en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2")
        #req.add_header("Cache-Control","max-age=0")
        #req.add_header("Connection","max-age=0")
        #req.add_header("Upgrade-Insecure-Requests","1")
        #req.add_header("Accept-Encoding","gzip, deflate, sdch, br")
        #req.add_header("Accept-Encoding","gzip, deflate, sdch, br")



        '''
        Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
        Accept-Encoding:gzip, deflate, sdch, br
        Accept-Language:en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2
        Cache-Control:max-age=0
        Connection:keep-alive
        Cookie:panlogin_animate_showed=1; PANWEB=1; __cfduid=d420755ba7e7c6c0d669c51ecadec567c1484203235; bdshare_firstime=1484556436985; BAIDUID=8D94AA591F47D21904D2871B5A7B7587:FG=1; PSTM=1488768470; BIDUPSID=D9CCAB486FAF77F2CB196C3D651FDFED; FP_UID=f40f80e586c3aa7098ed43bd3885076f; MCITY=-%3A; BDCLND=3phATBLpYK9BsqybhaJHkoqJXPlrsKq1J76JRgYkwGo%3D; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1506389313,1506396318,1506404874,1506405407; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1506405414; cflag=15%3A3; PSINO=1; H_PS_PSSID=1437_12897_21125_17001_22160; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598
        Host:pan.baidu.com
        Referer:https://pan.baidu.com/share/init?surl=jH4KE38
        Upgrade-Insecure-Requests:1
        User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36
        '''


        cookie = http.cookiejar.CookieJar()
        handler = urllib.request.HTTPCookieProcessor(cookie)
        self.opener = urllib.request.build_opener(handler)


        # Open Baidu URL by cusomized Opener
        try:
            response = self.opener.open(req)
            self.html = response.read().decode('utf-8')

            #self.html = urllib.request.urlopen(req).read().decode('utf-8')
            #print(self.html)
        except:
            raise Exception('--->>> URL Error')

        # Check HTML page correct or not
        if self.html.find('<head>') == False:
            raise Exception('--->>> Cannot get correct HTML page.')




    def getYunData(self):

        regexhtml = r'"server_filename":"(.+?)"'
        pattern = re.compile(regexhtml, re.UNICODE)
        self.m = pattern.search(self.html)
        self.fn = self.m.group(1)
        self.m = re.search(r'"fs_id":"(\d+)",', self.html)
        self.fs_id = self.m.group(1)


        #self.m = re.search(r'yunData.SHARE_UK = "(\d+)";'  , self.html, re.UNICODE)
        self.m = re.search(r'"uk":(\d+),', self.html, re.UNICODE)
        self.share_uk = self.m.group(1)
        #self.m = re.search(r'yunData.SHARE_ID = "(\d+)";'  , self.html, re.UNICODE)
        self.m = re.search(r'"shareid":(\d+),'  , self.html, re.UNICODE)
        self.share_id = self.m.group(1)
        #self.m = re.search(r'yunData.TIMESTAMP = "(\d+)";' , self.html, re.UNICODE)
        self.m = re.search(r'"timestamp":(\d+),' , self.html, re.UNICODE)
        self.share_timestamp = self.m.group(1)
        #self.m = re.search(r'yunData.SIGN = "([0-9a-f]+)";', self.html, re.UNICODE)
        self.m = re.search(r'"downloadsign":"([0-9a-f]+)",', self.html, re.UNICODE)
        self.share_sign = self.m.group(1)


    def dict_get(self, dict, objkey, Default):
        tmp = dict
        for k,v in tmp.items():
            if k == objkey:
                return v
            else:
                if type(v) is list:
                    v = v[0]
                    ret = self.dict_get(v, objkey, Default)
                    if ret is not Default:
                        return ret
        return Default





    def getDlink(self):

        purl = 'http://pan.baidu.com/api/sharedownload?sign='+self.share_sign+'&timestamp='+self.share_timestamp
        pdata = "encrypt=0&product=share&uk="+self.share_uk+"&primaryid="+self.share_id+"&fid_list=%5B"+self.fs_id+"%5D"
        pdata = pdata.encode('utf-8')

        res = urllib.request.urlopen(purl, pdata)
        jdata = json.loads(res.read().decode('utf-8'))
        #print(jdata)

        if not jdata.get('errno'):
            self.dlink = self.dict_get(jdata, 'dlink', None)
        else:
            raise Exception('Cannot get download link. Please try again later.')



if __name__ == '__main__':
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("echo", help="echo the string you use here")
    args = parser.parse_args()
    print (args.echo)
    '''

    ourl = input("Please input BaiduPan URL: ")
    ourl = 'http://pan.baidu.com/s/1gfN99L5'
    run = Parser(ourl)
    
    run.getYunData()
    print('----------------------------------------------')
    print('fn = ', run.fn)
    print('fs_id = ', run.fs_id)
    print('share_uk = ', run.share_uk)
    print('share_id = ', run.share_id)
    print('share_timestamp = ', run.share_timestamp)
    print('share_sign = ', run.share_sign)
    print('----------------------------------------------')

    run.getDlink()
    print ("Download Link: ", run.dlink)






#!/usr/bin/python
#-*- coding:UTF-8 -*-;
import urllib.error;
import urllib.request;
import urllib.parse;
import socket;

def WebHttp(url):
    req = urllib.request.Request(url);
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36");
    response = urllib.request.urlopen(req);
    data = response.read();
    try:
        html = data.decode('UTF-8', 'ignore');
    except:
        html = data.decode('GBK', 'ignore');
    return html;

def ImgHttp(url):
    timeout = 20;
    socket.setdefaulttimeout(timeout);
    req = urllib.request.Request(url);
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36");
    req.add_header("Accept", 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8');
    try:
        response = urllib.request.urlopen(req);
        data = response.read();
    except urllib.error as e:
        print(e);
        data = 0;
    return data;

#a = WebHttp("https://search.jd.com/Search?keyword=笔记本&enc=utf-8");
#print(a);
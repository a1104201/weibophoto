#!/usr/bin/python
#-*- coding:UTF-8 -*-;
from PyQt5.QtCore import *;
from lib.webHttp import *;
import threading;
import re;

class WeiboThread(QThread):
    trigger = pyqtSignal([str, int]);
    url = "http://photo.weibo.com/%s/talbum/detail/photo_id/";
    img_url = "http://photo.weibo.com/%s/wbphotos/large/photo_id/%s";

    def __init__(self, weibo_name, weibo_uid, folder):
        super(WeiboThread, self).__init__();
        self.weibo_name = weibo_name;
        self.weibo_uid = weibo_uid;
        self.folder = folder;

    def run(self):
        self.trigger.emit("%s微博相册开始抓取..." % self.weibo_name, 0);
        self.url = self.url % self.weibo_uid;
        data = WebHttp(self.url);
        p = re.search(r"album_photo_ids\: \[([0-9,]+)\]", data);
        ids = p.group(1).split(',');
        self.trigger.emit("total", len(ids));
        i = 0;
        for id in ids:
            self.getImage(id);
            #t = threading.Thread(target=self.getImage, args=(id,));
            #t.setDaemon(True);
            #t.start();
            i += 1;
            self.trigger.emit("num", i);

        self.trigger.emit("===========================采集完成===========================", 0);


    #相册图片抓取主程序
    def getImage(self, id):
        img_url = self.img_url % (self.weibo_uid, str(id));
        imgHtml = WebHttp(img_url);
        imgs = re.search('<img id="pic" src="(.*?)" onload=', imgHtml);
        try:
            img_link = imgs.group(1);
            img_name = img_link.split("/")[-1];
            if not ".jpg" in img_name:
                img_name = img_name + '.jpg';
            filename = self.folder + img_name;
            self.trigger.emit("抓取 ==> " + img_link, 0);
            imgData = ImgHttp(img_link)
            if imgData != 0:
                self.saveImg(imgData, filename);
                self.trigger.emit(filename + " ==> 保存成功", 0)
            else:
                self.trigger.emit("抓取超时跳过", 0);
        except:
            self.trigger.emit(img_url + " ==> 读取错误", 0);

    def saveImg(self, data, filename):
        with open(filename, 'wb') as f:
            f.write(data);
            f.close();


#!/usr/bin/python
#-*- coding:UTF-8 -*-;
from PyQt5.QtCore import *;
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *;
from PyQt5 import uic;
from func.LoginWeibo import *;
from func.WeiboThread import *;
import sys;
import os;

class MainForm(QWidget):
    isLogin = 0;
    folder = '';

    def __init__(self):
        super(MainForm, self).__init__();
        uic.loadUi("ui/weibo.ui", self);
        self.setWindowIcon(QIcon("ico\sina.ico"));
        self.retranslateUi();

    def retranslateUi(self):
        self.runButton.clicked.connect(self.run);
        self.openButton.clicked.connect(self.openFolder);
        self.showRunInfo("欢迎使用，精灵的微博相册抓取系统!!!!!");

    def run(self):
        self.username = self.usernameEdit.text();
        self.password = self.passwordEdit.text();
        self.weibo_name = self.weibonameEdit.text();
        self.weibo_uid = self.weibouidEdit.text();

        if self.username and self.password and self.weibo_name and self.weibo_uid:
            #检测是否需要登录微博
            if not self.isLogin:
                self.weiboLogin();

            #创建采集目录
            self.isFolder();

            #执行文件图片采集
            self.pBar.setMinimum(0);
            self.runThread();
        else:
            QMessageBox.warning(self, '警告', '请填写完整数据信息', QMessageBox.Yes);

    def weiboLogin(self):
        self.showRunInfo("登录中,请稍候...")

        #执行微博登录
        weibo = LoginWeibo(self.username, self.password);
        self.isLogin = weibo.login();
        if self.isLogin:
            msg = "微博登录成功!!!";
            self.usernameEdit.setEnabled(False);
            self.passwordEdit.setEnabled(False);
        else:
            msg = "微博登录失败!!!";

        item = QListWidgetItem();
        item.setText(msg);
        self.showListWidget.addItem(item);

    #创建采集目录
    def isFolder(self):
        folder = "微博图片";#主图片存放目录
        if not os.path.exists(folder):
            os.mkdir(folder, 777);

        self.folder = "%s/%s/" % (folder, self.weibo_name);#指定人物图片存放目录
        if not os.path.exists(self.folder):
            os.mkdir(self.folder, 777);

    #开启采集进程
    def runThread(self):
        self.goThread = WeiboThread(self.weibo_name, self.weibo_uid, self.folder);
        self.goThread.trigger.connect(self.showRunInfo);
        self.goThread.start();

    #显示采集信息
    def showRunInfo(self, msg, num = 0):
        #设定进度条最大值
        if msg == 'total' and num > 0:
            self.pBar.setMaximum(num);
        #设定进度条增长值
        if msg == 'num' and num:
            self.pBar.setValue(num);

        if not num:
            item = QListWidgetItem();
            item.setText(msg);
            self.showListWidget.addItem(item);
            self.showListWidget.scrollToBottom(); #辣条始终在底部显示

    #打开保存目录
    def openFolder(self):
        if self.folder:
            print("正在打开");
        else:
           QMessageBox.warning(self, '警告', '没有可打开的目录', QMessageBox.Yes);

    #设定键盘监听
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == 16777220 or QKeyEvent.key() == 16777221:
            self.run();



if __name__ == "__main__":
    app = QApplication(sys.argv);
    form = MainForm();
    form.show();
    sys.exit(app.exec_());



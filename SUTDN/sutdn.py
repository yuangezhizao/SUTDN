#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-
"""
    :Author: yuangezhizao
    :Time: 2019/4/6 0006 16:26
    :Site: https://www.yuangezhizao.cn
    :Copyright: © 2019 yuangezhizao <root@yuangezhizao.cn>
"""
import logging
import re

import requests

logging.getLogger('requests').setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)


class SUTDN:
    MY_URL = 'http://lab.yuangezhizao.cn/SUTDN'
    BASE_URL = 'http://192.168.100.200/'
    LOGIN_AJAX_METHOD = 'eportal/user.do?method=login_ajax&param=true&'
    CHECK_AUTH_STATE = 'eportal/user.do?method=checkAuthState'
    FRESH_METHOD = 'eportal/user.do?method=fresh&userIndex='
    OFFLINE_METHOD = 'eportal/userV2.do?method=offline'

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.session = requests.Session()

    def find_login_page(self):
        logging.info('检查网络状态')
        r = self.session.get(self.MY_URL).text
        if 'yuangezhizao' in r:
            logging.info('已在线')
            return 0
        else:
            logging.info('未在线')
            return re.findall("'(.*?)'", r, re.S)[0]

    def login(self):
        location = self.find_login_page()
        if not location:
            return logging.info('无需登录')
        for i in range(1, 4):
            logging.info('已尝试次数：' + str(i))
            self.session.get(location)
            data = {
                'is_auto_land': 'false',
                'usernameHidden': self.username,
                'username_tip': 'Username',
                'username': self.username,
                'strTypeAu': '',
                'uuidQrCode': '',
                'authorMode': '',
                'pwd_tip': 'Password',
                'pwd': self.password
            }
            params = location[41:]
            r = self.session.post(self.BASE_URL + self.LOGIN_AJAX_METHOD, params=params, data=data)
            try:
                reason = re.findall('<div id="errorInfo_center" val="(.*?)">', r.text, re.S)[0]
                logging.info('登录失败：' + reason)
            except Exception as e:
                logging.info('登录成功')
                r = self.session.get(self.BASE_URL + self.CHECK_AUTH_STATE)
                # 必须带有登录态才能获取 userIndex（因此 self.fresh 只能使用存储的 userIndex
                userIndex = re.findall("userIndex='(.*?)' ", r.text, re.S)[0]
                IsOnline = re.findall('<IsOnline>(.*?)</IsOnline>', r.text, re.S)[0]
                isAutoLogin = re.findall('<isAutoLogin>(.*?)</isAutoLogin>', r.text, re.S)[0]
                LeavingTime = re.findall('<LeavingTime>(.*?)</LeavingTime>', r.text, re.S)[0]
                userRealName = re.findall('<userRealName>(.*?)</userRealName>', r.text, re.S)[0]
                userGroup = re.findall('<userGroup>(.*?)</userGroup>', r.text, re.S)[0]
                onlineTime = re.findall('<onlineTime>(.*?)</onlineTime>', r.text, re.S)[0]
                SysMsg = re.findall('<SysMsg>(.*?)</SysMsg>', r.text, re.S)[0]
                freshtime = re.findall('<freshtime>(.*?)</freshtime>', r.text, re.S)[0]
                freshretries = re.findall('<freshretries>(.*?)</freshretries>', r.text, re.S)[0]
                accountInfo = re.findall('<accountInfo>(.*?)</accountInfo>', r.text, re.S)[0]
                system_notice = re.findall('<system-notice>(.*?)</system-notice>', r.text, re.S)[0]
                netaccesstype = re.findall('<netaccesstype>(.*?)</netaccesstype>', r.text, re.S)[0]
                t = re.findall('<t>(.*?)</t>', r.text, re.S)[0]
                qrCodeUrl = re.findall('<qrCodeUrl>(.*?)</qrCodeUrl>', r.text, re.S)[0]
                IP = re.findall('IP : (.*?)<', r.text, re.S)[0]

                logging.info('可用时长：' + LeavingTime)
                logging.info('用户组：' + userGroup)
                logging.info('账户信息：' + accountInfo)

                with open('../userIndex.txt', 'w') as f:
                    f.write(userIndex)

                self.fresh()
                return 1
        return 0

    def logout(self):
        r = self.session.get(self.BASE_URL).text
        if '已下线' in r:
            logging.info('无需下线')
        else:
            r = self.session.post(self.BASE_URL + self.OFFLINE_METHOD).text
            if '已下线' in r:
                logging.info('下线成功')
            else:
                logging.info('下线失败')

    def fresh(self):
        with open('../userIndex.txt', 'r') as f:
            userIndex = f.read()
        r = self.session.get(self.BASE_URL + self.FRESH_METHOD + userIndex).text
        if 'IsOnline' not in r:
            message = re.findall('window.alert\("(.*?)!"\);', r, re.S)[0]
            logging.info('心跳包发送失败：' + message)
        else:
            logging.info('心跳包发送成功')

            IsOnline = re.findall('<IsOnline>(.*?)</IsOnline>', r, re.S)[0]
            isAutoLogin = re.findall('<isAutoLogin>(.*?)</isAutoLogin>', r, re.S)[0]
            LeavingTime = re.findall('<LeavingTime>(.*?)</LeavingTime>', r, re.S)[0]
            userRealName = re.findall('<userRealName>(.*?)</userRealName>', r, re.S)[0]
            userGroup = re.findall('<userGroup>(.*?)</userGroup>', r, re.S)[0]
            onlineTime = re.findall('<onlineTime>(.*?)</onlineTime>', r, re.S)[0]
            SysMsg = re.findall('<SysMsg>(.*?)</SysMsg>', r, re.S)[0]
            freshtime = re.findall('<freshtime>(.*?)</freshtime>', r, re.S)[0]
            freshretries = re.findall('<freshretries>(.*?)</freshretries>', r, re.S)[0]
            accountInfo = re.findall('<accountInfo>(.*?)</accountInfo>', r, re.S)[0]
            system_notice = re.findall('<system-notice>(.*?)</system-notice>', r, re.S)[0]
            netaccesstype = re.findall('<netaccesstype>(.*?)</netaccesstype>', r, re.S)[0]
            t = re.findall('<t>(.*?)</t>', r, re.S)[0]
            qrCodeUrl = re.findall('<qrCodeUrl>(.*?)</qrCodeUrl>', r, re.S)[0]

            logging.info('可用时长：' + LeavingTime)
            logging.info('在线时长：' + str(onlineTime) + ' min')

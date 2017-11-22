# -*- coding: utf-8 -*-
import re
import logging

import requests

logging.basicConfig(level=logging.INFO)


class SUTDN:
	"""
	SUTDN（SUT Dormitory Network）类
	"""
	LOCAL_URL = 'http://192.168.0.1'
	POST_URL_0 = 'http://192.168.100.200/eportal/user.do?method=login_ajax&param=true&'
	CHECK_URL_0 = 'http://192.168.100.200/eportal/user.do?method=checkAuthState&'
	FRESH_URL_0 = 'http://192.168.100.200/eportal/user.do?method=fresh&userIndex='

	# session = requests.Session()
	# 警告：三次以上出校验码

	def __init__(self, username=None, password=None):
		"""
		init
		"""
		self.username = username
		self.password = password
		self.session = requests.Session()
		# self.userIndex = userIndex
		# TODO：如何无需加参数但是可以自由使用

	def find_login_page(self):
		"""
		寻找登陆页面函数
		原理：宿舍内网未联外网状态下 302 重定向跳转，理论上 LOCAL_URL 为任何值均可
		"""
		text = self.session.get(self.LOCAL_URL).text
		param_url = re.findall("'(.*?)'", text, re.S)[0]
		logging.info(u'获取含参链接中')
		return param_url

	def login(self):
		"""
		登陆函数
		原理：POST 明文数据包
		"""
		param_url = self.find_login_page()
		post_url = self.POST_URL_0 + param_url[41:]
		r = self.session.get(param_url)
		logging.info(u'获取登陆链接中')
		if r.status_code != 200:
			logging.error(u'获取登录页面失败')
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
		r = self.session.post(post_url, data=data, allow_redirects=False)
		location = r.headers['Location']
		logging.info(u'获取跳转链接中')
		r = self.session.get(location, data=data, allow_redirects=False).text
		if 'alert' in r:
			logging.info(u'登陆成功')
		elif u'您的账户已欠费' in r:
			logging.info(u'欠费')
			return 0
		elif u'认证系统已发现相同的网卡物理地址用户在线' in r:
			logging.info(u'认证系统已发现相同的网卡物理地址用户在线')
			return 0
		elif u'您之前上网没有正常下线，请重新认证' in r:
			logging.info(u'未正常下线，尝试下线中')
			self.offline()
			return 0
		elif u'你使用的账号已达到同时在线用户数量上限' in r:
			logging.info(u'你使用的账号已达到同时在线用户数量上限')
			return 0
		elif u'密码不匹配,请输入正确的密码' in r:
			logging.info(u'密码不匹配,请输入正确的密码')
			return 0
		elif u'用户名以空格开头或结尾' in r:
			logging.info(u'用户名以空格开头或结尾')
			return 0
		elif u'用户不存在' in r:
			logging.info(u'用户不存在')
			return 0
		else:
			print r
			raise Exception('啊咧，我也不知道这是什么页面，发给我看看吧')

		check_url = self.CHECK_URL_0 + location[68:]
		r = self.session.get(check_url, allow_redirects=False)

		userIndex = re.findall('var userIndex = "(.*?)";', r.text, re.S)[0]
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

		logging.info(u'可用时长：' + LeavingTime)
		logging.info(u'用户组：' + userGroup)
		logging.info(accountInfo)

		file_object = open('../userIndex.txt', 'w')
		file_object.write(userIndex)
		file_object.close()
		self.fresh()

	def offline(self):
		"""
		下线函数
		"""
		url = 'http://192.168.100.200'
		r = self.session.get(url).text
		if u'已下线' in r:
			logging.info(u'无需下线')
		else:
			r = self.session.post('http://192.168.100.200/eportal/userV2.do?method=offline').text
			if u'已下线' in r:
				logging.info(u'下线成功')

	def fresh(self):
		"""
		刷新在线信息函数
		"""
		f = open('../userIndex.txt', 'r')
		userIndex = f.read()
		fresh_url = self.FRESH_URL_0 + userIndex
		r = self.session.get(fresh_url)

		if re.findall('<IsOnline>(.*?)</IsOnline>', r.text, re.S)[0] == 'true':
			logging.info(u'心跳包发送成功')
		else:
			print r
			raise Exception('心跳包发送失败')

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

		logging.info(u'可用时长：' + LeavingTime)
		logging.info(u'在线时长：' + onlineTime + ' min')


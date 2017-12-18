# -*- coding: utf-8 -*-
import re
import json
import logging

import requests
logging.getLogger('requests').setLevel(logging.WARNING)

session = requests.session()
logging.basicConfig(level=logging.INFO)

state = {}

query_url = 'http://192.168.100.101:8080/selfservice/module/scgroup/web/login_judge.jsf'
data_url = 'http://192.168.100.101:8080/selfservice/module/userself/web/userself_ajax.jsf?methodName=indexBean.refreshSelfIndexData'
device_url = 'http://192.168.100.101:8080/selfservice/module/webcontent/web/onlinedevice_list.jsf'
phone_url = 'http://192.168.100.101:8080/selfservice/module/userself/web/regpassuserinfo_update.jsf'

kill_url = 'http://192.168.100.101:8080/selfservice/module/userself/web/userself_ajax.jsf?methodName=indexBean.kickUserBySelfForAjax'


def query_state(username, password):
	"""
	查询用户信息函数
	"""
	data = {
		'name': username,
		'password': password
	}
	r = session.post(url=query_url, data=data).text
	if "index_self" in r:
		logging.info('登陆自助查询成功')
	elif u'用户不存在或密码错误' in r:
		raise Exception('登陆自助查询失败，请检查用户名和密码并重试')
	else:
		print r
		raise Exception('啊咧，我也不知道这是什么页面，发给我看看吧')
	r = session.get(phone_url).text
	state['phone'] = re.findall(r"\d{11}", r, re.S)[0]

	r = session.get(data_url).text
	jsDict = json.loads(r)
	state['userUuid'] = jsDict['userUuid']
	state['userId'] = jsDict['userId']
	state['userName'] = jsDict['userName']
	state['lastLoginSelfTime'] = jsDict['lastLoginSelfTime']
	state['packageUuid'] = jsDict['packageUuid']
	state['packageName'] = jsDict['packageName']
	state['onlineNum'] = jsDict['onlineNum']
	state['fee'] = jsDict['fee']
	state['showFee'] = jsDict['showFee']
	state['prefee'] = jsDict['prefee']
	state['showPrefee'] = jsDict['showPrefee']
	state['greetings'] = jsDict['greetings']
	state['emotionalWordsInIndex'] = jsDict['emotionalWordsInIndex']
	state['emotionalWordsInLogin'] = jsDict['emotionalWordsInLogin']
	state['accountInfoUuid'] = jsDict['accountInfoUuid']
	state['needFee'] = jsDict['needFee']
	state['feeExpirationTime'] = jsDict['feeExpirationTime']
	state['haveDays'] = jsDict['haveDays']
	state['userState'] = jsDict['userState']
	state['canPrefund'] = jsDict['canPrefund']

	logging.info(u'用户名：' + state['userId'])
	logging.info(u'手机号：' + state['phone'])
	logging.info(u'套餐：' + state['packageName'][:2] + u'元套餐')
	logging.info(u'余额：' + state['showFee'] + u'元')
	logging.info(u'剩余日期：' + state['haveDays'] + u'天')
	logging.info(u'可使用至：' + state['feeExpirationTime'])

	r = session.get(device_url).text

	if state['onlineNum'] == '1':
		ip_0 = re.findall('<input id="userIp(.*?)">', r, re.S)[0][57:]
		mac_0 = re.findall('<input id="usermac(.*?)">', r, re.S)[0][56:]
		createTime_0 = re.findall('<input id="createTimeStr(.*?)">', r, re.S)[0][56:]
		state['mac_0'] = mac_0
		state['ip_0'] = ip_0
		state['createTime_0'] = createTime_0
		logging.info('在线[1]设备列表：')
		logging.info(u'\t设备一\tMAC：' + mac_0 + u'\tIP：' + ip_0 + u'\t上线时间：' + createTime_0)
	elif state['onlineNum'] == '2':
		ip_0 = re.findall('<input id="userIp(.*?)">', r, re.S)[0][57:]
		mac_0 = re.findall('<input id="usermac(.*?)">', r, re.S)[0][56:]
		createTime_0 = re.findall('<input id="createTimeStr(.*?)">', r, re.S)[0][56:]
		ip_1 = re.findall('<input id="userIp(.*?)">', r, re.S)[1][57:]
		mac_1 = re.findall('<input id="usermac(.*?)">', r, re.S)[1][56:]
		createTime_1 = re.findall('<input id="createTimeStr(.*?)">', r, re.S)[1][56:]
		state['mac_0'] = mac_0
		state['ip_0'] = ip_0
		state['createTime_0'] = createTime_0
		state['mac_1'] = mac_1
		state['ip_1'] = ip_1
		state['createTime_1'] = createTime_1
		logging.info('在线[2]设备列表：')
		logging.info(u'\t设备一\tMAC：' + mac_0 + u'IP：' + ip_0 + u'上线时间：' + createTime_0)
		logging.info(u'\t设备二\tMAC：' + mac_1 + u'IP：' + ip_1 + u'上线时间：' + createTime_1)
	elif state['onlineNum'] == '0':
		logging.info('无在线设备')
	else:
		logging.info('还有这种操作.jpg?')


def kill(username, ip):
	"""
	强制下线函数
	"""
	# TODO：保持会话
	data = 'key={0}:{1}'.format(username, ip)
	r = session.post(kill_url, data=data)
	logging.info(r.text)


if __name__ == '__main__':
	query_state('<username>', '<password>')

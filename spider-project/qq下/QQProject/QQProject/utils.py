# 一些工具函数
import os
import re
import time
import datetime


# 保存requests.content/text
def SaveHtml(content, savefile, filename):
	if not os.path.exists(savefile):
		os.mkdir(savefile)
	f = open(os.path.join(savefile, filename), 'w')
	f.write(str(content))
	f.close()


# 保存Cookie
def SaveCookie(cookie, savefile='./data'):
	if not os.path.exists(savefile):
		print('[Warning]: %s inexistence, create new one...' % savefile)
		os.mkdir(savefile)
	f = open(os.path.join(savefile, 'cookie.info'), 'w')
	f.write(str(cookie))
	f.close()


# 读取Cookie
def ReadCookie(datafile='./data'):
	if not os.path.exists(datafile):
		print('[Warning]: %s inexistence in <utils.py - ReadCookie func>...' % datafile)
		return None
	txtpath = os.path.join(datafile, 'cookie.info')
	if not os.path.isfile(txtpath):
		print('[Warning]: %s inexistence in <utils.py - ReadCookie func>...' % txtpath)
		return None
	f = open(txtpath, 'r')
	cookie = f.read().strip()
	return cookie if cookie else None


# 获得Headers
def GetHeader(cookie=None):
	if cookie:
		headers = {
			"accept-language": "zh-CN,zh;q=0.9",
			"accept-encoding": "gzip, deflate, sdch, br",
			"accept": "*/*",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
			"cookie": cookie
		}
	else:
		headers = {
			"accept-language": "zh-CN,zh;q=0.9",
			"accept-encoding": "gzip, deflate, sdch, br",
			"accept": "*/*",
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
		}
	return headers


# 获得gtk
def GetGtk(skey):
	thash = 5381
	for c in skey:
		thash += (thash<<5) + ord(c)
	return thash&2147483647


# 获得skey
def GetSkey(cookie):
	item = re.findall(r'p_skey=(.*?);', cookie)
	return item[0] if len(item) > 0 else None


# 读取我关心和关心我的好友QQ
def ReadCared(datafile):
	friends = []
	f = open(datafile)
	for line in f:
		line = line.strip()
		if line:
			try:
				int(line[0])
			except:
				continue
			friend = line.split(' ')
			for fri in friend:
				if fri not in friends:
					friends.append(fri)
	return friends


# 画柱状图
def DrawBar(data, mark_point=["min", "max"], barname=None):
	from pyecharts import Bar
	if barname is not None:
		bar = Bar(barname)
	else:
		bar = Bar()
	try:
		bar.add('', data[0], data[1], mark_point=mark_point)
	except:
		print('[Error]: Arguments format error in <utils.py - DrawBar func>...')
		return None
	if barname is None:
		barname = 'results'
	bar.render('%s.html' % barname)


# 画饼图
def DrawPie(data, piename=None):
	from pyecharts import Pie
	if piename is not None:
		pie = Pie(piename)
	else:
		pie = Pie()
	try:
		pie.add('', data[0], data[1], is_label_show=True)
	except:
		print('[Error]: Arguments format error in <utils.py - DrawPie func>...')
		return None
	if piename is None:
		piename = 'results'
	pie.render('%s.html' % piename)


# 画地图
def DrawMap(data, mapname=''):
	from pyecharts import Map
	map_ = Map(mapname, width=1200, height=600)
	try:
		map_.add('', data[0], data[1], maptype='china', is_visualmap=True, visual_text_color='#000')
	except:
		print('[Error]: Arguments format error in <utils.py - DrawMap func>...')
		return None
	if mapname is '':
		mapname = 'results'
	map_.render('%s.html' % mapname)


# 性别统计
def CountSex(friendsInfoDict):
	boy = 0
	girl = 0
	other = 0
	for key in friendsInfoDict:
		try:
			if friendsInfoDict[key]['sex'] == '2':
				girl += 1
			elif friendsInfoDict[key]['sex'] == '1':
				boy += 1
			else:
				other += 1
		except:
			other += 1
	return boy, girl, other


# 年龄统计
def CountAge(friendsInfoDict):
	ageDict = {}
	for key in friendsInfoDict:
		try:
			birthyear = friendsInfoDict[key]['birthyear']
		except:
			birthyear = ''
		if birthyear == '' or birthyear == '0':
			ageDict['other'] = ageDict.get('other', 0) + 1
		else:
			ageDict[birthyear] = ageDict.get(birthyear, 0) + 1
	items = sorted(ageDict.items(), key=lambda x: x[0], reverse=True)
	counts = []
	ages = []
	for item in items:
		birthyear = item[0]
		count = item[1]
		if birthyear != 'other':
			age = datetime.datetime.now().year - int(birthyear)
			ages.append(age)
			counts.append(count)
		else:
			ages.append('Unkown')
			counts.append(count)
	return [ages, counts]


# 地区统计
def CountArea(friendsInfoDict, areatype):
	areaDict = {}
	for key in friendsInfoDict:
		try:
			area = friendsInfoDict[key][areatype]
		except:
			area = ''
		if area == '':
			area = 'Unkown'
		areaDict[area] = areaDict.get(area, 0) + 1
	return [list(areaDict.keys()), list(areaDict.values())]


# 解析好友信息
def ParseFriendsInfo(qq, t_qq, datafile='./results'):
	info_txt = os.path.join(datafile, qq, t_qq+'_info.txt')
	if not os.path.exists(info_txt):
		return None
	infoDict = {}
	with open(info_txt) as f:
		for line in f:
			line=line.strip()
			# 昵称
			if line.startswith('"nickname":'):
				nickname = re.findall(r'"nickname":"(.*?)",', line)[0]
				infoDict['nickname'] = nickname
				continue
			# 空间名
			elif line.startswith('"spacename":'):
				spacename = re.findall(r'"spacename":"(.*?)",', line)[0]
				infoDict['spacename'] = spacename
				continue
			# 空间简介
			elif line.startswith('"desc":'):
				desc = re.findall(r'"desc":"(.*?)",', line)[0]
				infoDict['desc'] = desc
				continue
			# 空间签名
			elif line.startswith('"signature":'):
				signature = re.findall(r'"signature":"(.*?)",', line)[0]
				infoDict['signature'] = signature
				continue
			# 性别
			elif line.startswith('"sex":'):
				sex = re.findall(r'"sex":(.*?),', line)[0]
				infoDict['sex'] = sex
				continue
			# 出生年
			elif line.startswith('"birthyear":'):
				birthyear = re.findall(r'"birthyear":(.*?),', line)[0]
				infoDict['birthyear'] = birthyear
				continue
			# 出生月日
			elif line.startswith('"birthday":'):
				birthday = re.findall(r'"birthday":"(.*?)",', line)[0]
				infoDict['birthday'] = birthday
				continue
			# 血型
			elif line.startswith('"bloodtype":'):
				bloodtype = re.findall(r'"bloodtype":(.*?),', line)[0]
				infoDict['bloodtype'] = bloodtype
				continue
			# 星座
			elif line.startswith('"constellation":'):
				constellation = re.findall(r'"constellation":(.*?),', line)[0]
				infoDict['constellation'] = constellation
				continue
			# 国家
			elif line.startswith('"country":'):
				country = re.findall(r'"country":"(.*?)",', line)[0]
				infoDict['country'] = country
				continue
			# 省
			elif line.startswith('"province":'):
				province=re.findall(r'"province":"(.*?)",', line)[0]
				infoDict['province'] = province
				continue
			# 城市
			elif line.startswith('"city":'):
				city=re.findall(r'"city":"(.*?)",', line)[0]
				infoDict['city'] = city
				continue
			# 家乡国
			elif line.startswith('"hco":'):
				hco = re.findall(r'"hco":"(.*?)",', line)[0]
				infoDict['hco'] = hco
				continue
			# 家乡省
			elif line.startswith('"hp":'):
				hp=re.findall(r'"hp":"(.*?)",', line)[0]
				infoDict['hp'] = hp
				continue
			# 家乡城
			elif line.startswith('"hc":'):
				hc = re.findall(r'"hc":"(.*?)",', line)[0]
				infoDict['hc'] = hc
				continue
			# 婚否
			elif line.startswith('"marriage":'):
				marriage=re.findall(r'"marriage":(.*?),', line)[0]
				infoDict['marriage'] = marriage
				continue
			# 职业
			elif line.startswith('"career":'):
				career = re.findall(r'"career":"(.*?)",', line)[0]
				infoDict['career'] = career
				continue
			# 公司
			elif line.startswith('"company":'):
				company = re.findall(r'"company":"(.*?)",', line)[0]
				infoDict['company'] = company
				continue
			# 最后修改时间
			elif line.startswith('"ptimestamp":'):
				ptimestamp = re.findall(r'"ptimestamp":(.*?)}', line)[0]
				if ptimestamp != '':
					temp = time.localtime(float(ptimestamp))
					createtime = time.strftime('%Y-%m-%d %H:%M:%S', temp)
				else:
					createtime = ''
				infoDict['createtime'] = createtime
				continue
	return infoDict
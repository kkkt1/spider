# QQ空间爬虫
# 作者: Charles
# 公众号: Charles的皮卡丘
import init
import cookie
import requests
import re
from utils import *


# 谁在意我
def GetCaredme(qq, gtk, headers):
	url = 'https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin={}&do=1&rd=0.11376390567557748&fupdate=1&clean=0&g_tk={}'
	url = url.format(qq, gtk)
	res = requests.get(url, headers=headers)
	status = res.status_code
	if status != 200:
		print('[Error]: Fail to get who care me in <QQ_Spider - GetCaredme func>...')
		exit(-1)
	content = res.content
	SaveHtml(content, './results/{}'.format(qq), 'Caredme.txt')
	return content


# 我在意谁
def GetMecared(qq, gtk, headers):
	url = 'https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin={}&do=1&rd=0.11376390567557748&fupdate=1&clean=0&g_tk={}'
	url = url.format(qq, gtk)
	res = requests.get(url, headers=headers)
	status = res.status_code
	if status != 200:
		print('[Error]: Fail to get me care who in <QQ_Spider - GetMecared func>...')
		exit(-1)
	content = res.content
	SaveHtml(content, './results/{}'.format(qq), 'Mecared.txt')
	return content


# 获得我关心谁/谁关心我信息
def GetCared(qq, gtk, headers, savefile='./results'):
	savefile = os.path.join(savefile, qq, 'cared.list')
	Caredme = GetCaredme(qq, gtk, headers)
	friend1 = re.findall(r'"uin":(.*?),', str(Caredme))
	Mecared = GetMecared(qq, gtk, headers)
	friend2 = re.findall(r'"uin":(.*?),', str(Mecared))
	try:
		f = open(savefile, 'w')
	except:
		import init
		f = open(savefile, 'w')
	f.write('Caredme:\n')
	for friend in friend1:
		friend = friend.strip()
		if friend:
			f.write(str(friend) + ' ')
	f.write('\n\n\n')
	f.write('Mecared:\n')
	for friend in friend2:
		friend = friend.strip()
		if friend:
			f.write(str(friend) + ' ')
	print('[INFO]: Get care and cared successfully, save to %s...' % savefile)


# 爬取好友信息
def DownloadFriendsInfo(qq, t_qq, gtk, headers, faillog='./results'):
	url = 'https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all?uin={}&vuin={}&fupdate=1&g_tk={}'
	url = url.format(t_qq, qq, gtk)
	res = requests.get(url, headers=headers)
	status = res.status_code
	if status != 200:
		print('[Error]: Fail to get %s info in <QQ_Spider - GetMecared func>...' % str(t_qq))
		f = open(os.path.join(faillog, '{}.fail'.format(qq)), 'a')
		f.write(str(t_qq) + '\n')
		f.close()
		return None
	content = res.content
	content = content.decode('ascii', 'ignore')
	SaveHtml(content, './results/{}'.format(qq), '{}_info.txt'.format(t_qq))
	return content


# 获取所有好友信息
def GetAllFriendsInfo(qq, friends):
	friendsInfoDict = {}
	for friend in friends:
		infoDict = ParseFriendsInfo(qq, friend, datafile='./results')
		if infoDict is not None:
			friendsInfoDict[friend] = infoDict
	return friendsInfoDict



if __name__ == '__main__':
	username = QQ号
	password = 密码
	qq, gtk, headers = cookie.get(username, password)
	GetCared(qq, gtk, headers)
	friends = ReadCared(os.path.join('./results', qq, 'cared.list'))
	print('[INFO]: Start to download info of %d friends...' % len(friends))
	for friend in friends:
		DownloadFriendsInfo(qq, friend, gtk, headers)
	

	friendsInfoDict = GetAllFriendsInfo(qq, friends)
	'''
	# 性别分析
	boy, girl, other = CountSex(friendsInfoDict)
	data = [['boy', 'girl', 'other'], [boy, girl, other]]
	DrawPie(data, piename='QQ好友男女比')
	'''
	'''
	# 年龄分析
	data = CountAge(friendsInfoDict)
	DrawBar(data, barname='QQ好友年龄分布')
	'''
	# 地区分布分析
	data = CountArea(friendsInfoDict, 'province')
	DrawMap(data, mapname='QQ好友区域分布')
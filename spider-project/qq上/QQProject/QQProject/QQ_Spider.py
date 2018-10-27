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
def GetCared(qq, gtk, headers, savefile='./results/cared.list'):
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



if __name__ == '__main__':
	username = QQ number
	password = QQ password
	qq, gtk, headers = cookie.get(username, password)
	GetCared(qq, gtk, headers)
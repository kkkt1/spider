# 一些工具函数
import os
import re


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
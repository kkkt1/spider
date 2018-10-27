# 获得Cookie值
# 	若之前保存的Cookie有效则返回之前的Cookie，
# 	否则返回新的Cookie值。
# 作者: Charles
# 公众号: Charles的皮卡丘
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
import requests
import time
from utils import *


# 检查之前保存的Cookie是否还有效
def _CheckCookie(qq, gtk, headers):
	url = 'https://h5.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?uin={}&do=1&rd=0.11376390567557748&fupdate=1&clean=0&g_tk={}'
	url = url.format(str(qq), str(gtk))
	res = requests.get(url, headers=headers)
	status = res.status_code
	if status != 200 or '请先登录' in str(res.content):
		return False
	return True


# 账号密码模拟登陆获取新的Cookie
def _GetNewCookie(usr, pwd):
	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.get('http://qzone.qq.com')
	# 切到登陆模块
	driver.switch_to_frame('login_frame')
	driver.find_element_by_id('switcher_plogin').click()
	driver.find_element_by_id('u').clear()
	driver.find_element_by_id('u').send_keys(usr)
	driver.find_element_by_id('p').clear()
	driver.find_element_by_id('p').send_keys(pwd)
	driver.find_element_by_id('login_button').click()
	# 浏览器跳转
	time.sleep(5)
	driver.switch_to_default_content()
	page = etree.HTML(driver.page_source)
	nick = page.xpath('//*[@id="headContainer"]/div[2]/div/span[1]')
	if len(nick) > 0:
		print('[INFO]: %s Login Successfully...' % usr)
	else:
		print('[Error]: Fail to login %s in <cookie.py - _GetNewCookie func>...' % usr)
		driver.quit()
		exit(-1)
	items = [item['name'] + '=' + item['value'] for item in driver.get_cookies()]
	cookie = ';'.join(items)
	print('[INFO]: Get Cookie %s' % cookie)
	driver.quit()
	return cookie


# 获取QQ号, gtk和Header
def _GetQGH(username, cookie):
	headers = GetHeader(cookie=cookie)
	skey = GetSkey(cookie)
	if skey is None:
		print('[Error]: Skey inexistence in <cookie.py - _GetQGH func>...')
		exit(-1)
	try:
		int(username)
	except:
		print('[Error]: Username must be qqNo in <cookie.py - _GetQGH func>...')
		exit(-1)
	qq = username
	gtk = GetGtk(skey)
	return qq, gtk, headers


# 外部调用，获取cookie值
def get(username, password=None, datafile='./data', savefile='./data'):
	cookie = ReadCookie(datafile=datafile)
	if cookie is None:
		print('[INFO]: No cookie saved before, get new one...')
		cookie = _GetNewCookie(username, password)
		if cookie is None:
			print('[Error]: Fail to get cookie in <cookie.py - get func>...')
			exit(-1)
		SaveCookie(cookie, savefile=savefile)
		qq, gtk, headers = _GetQGH(username, cookie)
		return qq, gtk, headers
	qq, gtk, headers = _GetQGH(username, cookie)
	if not _CheckCookie(qq, gtk, headers):
		print('[INFO]: Cookie is out of date, get new one...')
		cookie = _GetNewCookie(username, password)
		if cookie is None:
			print('[Error]: Fail to get cookie in <cookie.py - get func>...')
			exit(-1)
		SaveCookie(cookie, savefile=savefile)
		qq, gtk, headers = _GetQGH(username, cookie)
	return qq, gtk, headers
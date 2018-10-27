# 美团美食板块商家信息爬取脚本
# 作者：Charles
# 公众号：Charles的皮卡丘
import json
import requests
import random
import urllib
import cookies
import time
from openpyxl import Workbook
import win_unicode_console
win_unicode_console.enable()


# 获得城市地址
def Get_City_Url(city_name):
	f = open('cities_url.json')
	cities_url = json.load(f)
	f.close()
	idx = cities_url['city_name'].index(city_name)
	return cities_url['city_url'][idx]


# 获得cookies值
def get_cookies():
	cookie = cookies.Cookies[random.randint(0, len(cookies.Cookies)-1)]
	return cookie


# 获得商家数据
def Get_Data(city_name, url):
	headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.32 Safari/537.36',
			'Cookie': get_cookies()
			}
	all_data = []
	num = 1
	while True:
		print('[INFO(Data)]:Getting Page %s' % num)
		num += 1
		page_url = url + 'api/poi/getPoiList?cityName={}&page={}'.format(urllib.parse.quote(city_name), num)
		try:
			res = requests.get(page_url, headers=headers)
		except:
			print('[INFO]:%s Requests Error...' % page_url)
			continue
		data_list = res.json()['data']['poiInfos']
		if len(data_list) < 1:
			print('[INFO]:All data has getted...')
			break
		for dl in data_list:
			# 店名
			name = dl['title']
			# 评分
			score = dl['avgScore']
			# 评论数量
			commentNum = dl['allCommentNum']
			# 均价
			price = dl['avgPrice']
			# 地址
			addr = dl['address']
			all_data.append([name, score, commentNum, price, addr])
		time.sleep(random.randint(1, 5))
	return all_data


# 结果保存到excel中
def save_to_excel(merchant_list, excel_name):
	wb = Workbook()
	ws = wb.active
	ws.append(['店名', '评分', '评论数量', '均价', '地址'])
	for ml in merchant_list:
		try:
			ws.append([ml[0], ml[1], ml[2], ml[3], ml[4]])
		except:
			print('[WARNING]:A merchant lost...')
			continue
	wb.save('./results/' + excel_name + '.xlsx')
	print('[INFO]:Data saved to excel successfully...')


def main():
	# 选你想要爬取的城市
	city_choice = input('Enter the city name(In Chinese):')
	try:
		city_url = Get_City_Url(city_choice)
	except:
		print('[ERROR]:City Name Error...')
		return
	city_cate_url = city_url + '/meishi/'
	# 开始爬取数据
	all_data = Get_Data(city_choice, city_cate_url)
	# 将数据存储到Excel中
	save_to_excel(all_data, city_choice)



if __name__ == '__main__':
	main()
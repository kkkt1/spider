import requests
import os
from urllib.request import urlretrieve


def download(url):
	headers = {
				'Accept-Charset': 'UTF-8',
				'Accept-Encoding': 'gzip, deflate',
				'Connection': 'Keep-Alive'
				}
	res = requests.get(url, headers=headers).json()
	hero_num = len(res['list'])
	print('[Hero Num]:%d' % hero_num)
	for hero in res['list']:
		pic_url = hero['cover']
		hero_name = hero['name'] + '.jpg'
		filename = './images/' + hero_name
		if not os.path.exists('images'):
			os.mkdir('images')
		urlretrieve(url=pic_url, filename=filename)
		print('[INFO]:Get %s picture...' % hero['name'])



if __name__ == '__main__':
	download("http://gamehelper.gm825.com/wzry/hero/list?game_id=7622")
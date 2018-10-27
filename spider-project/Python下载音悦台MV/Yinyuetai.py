# 音悦台MV下载脚本
# 作者：Charles
# 公众号：Charles的皮卡丘
import re
import requests
import click
from contextlib import closing


def Spider(url):
	mvid = url.split('/')[-1]
	info_url = 'http://www.yinyuetai.com/insite/get-video-info?flex=true&videoId={}'.format(mvid)
	res = requests.get(info_url)
	html = res.text
	rule = re.compile(r'http://\w*?\.yinyuetai\.com/uploads/videos/common/.*?(?=&br)')
	results = re.findall(rule, html)
	num = len(results)
	print('[HELP]:This mv has %d levels,so enter 1-%d...' % (num, num))
	print('[HELP]:The greater number, the better mv...')
	choice = input('Choose the mv quality:')
	try:
		choice = int(choice)
	except:
		print('[Warning]:Enter error,auto choose the worst mv...')
		choice = 1
	try:
		mv_url = results[choice-1]
	except:
		if choice < 1:
			mv_url = results[0]
		else:
			mv_url = results[-1]
	print('<Download link>: \n%s' % mv_url)
	with closing(requests.get(mv_url, stream=True)) as res:
		total_size = int(res.headers['content-length'])
		if res.status_code == 200:
			label = '[FileSize]:%0.2f MB' % (total_size/(1024*1024))
			with click.progressbar(length=total_size, label=label) as progressbar:
				with open(mvid+'.mp4', "wb") as f:  
					for chunk in res.iter_content(chunk_size=1024):
						if chunk:
							f.write(chunk)
							progressbar.update(1024)
		else:
			print('[ERROR]:Connect error...')
	
	
	
if __name__ == '__main__':
	print('[INFO]:yinyuetai mv downloader...')
	print('[URL]:http://www.yinyuetai.com')
	print('[Author]:Charles')
	url = input('Enter the mv url you want to download:')
	Spider(url)
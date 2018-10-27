import BaiduSearch_Spider
import sys
import time
from PyQt5.Qt import *
from PyQt5.QtWebEngine import *


class WebView(QWebEngineView):
	def __init__(self, parent):
		super().__init__(parent)
	def createWindow(self, webWindowType):
		global window
		return window.browser


class MainWindow(QMainWindow):
	def __init__(self, url, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.resize(800, 500)
		self.show()
		self.browser = WebView(self)
		self.browser.resize(self.size())
		self.browser.setUrl(QUrl(url))
		self.setCentralWidget(self.browser)


def show_results(results):
	for c in results:
		temp = c[0]
		temp = str(temp)
		con = temp.encode('gbk', 'ignore')
		content = con.decode('gbk', 'ignore')
		print(content+':')
		print(c[1])
		print('-'*60)


def show_Web(link):
	global window
	app = QApplication(sys.argv)
	window = MainWindow(link)
	window.show()
	sys.exit(app.exec_())


if __name__ == '__main__':
	while True:
			key_word = input('Enter the key word:')
			page_num = input('Enter the results pages:')
			try:
				page_num = int(page_num)
			except:
				print('pages should be digital...')
				continue
			if page_num < 1:
				print('Page number need >0...')
				continue
			results = BaiduSearch_Spider.Get_Precise_Results(key_word, page_num).run()
			print('[INFO]:Data Collected Successfully!')
			page = 0
			while True:
				print('')
				print('*'*60)
				print('Page%s:' % page)
				print('*'*60)
				print('')
				print('-'*60)
				show_results(results[page])
				print('*'*60)
				print('[Enter -1]: Back Page\n[Enter 1]: Next Page\n[Enter 0]: Select links')
				print('*'*60)
				select = input('You Select:')
				if select == '-1':
					if page > 0:
						page -= 1
					else:
						print('This is first page...')
						time.sleep(5)
					continue
				elif select == '1':
					if page < page_num-1:
						page += 1
					else:
						print('This is last page...')
						time.sleep(5)
					continue
				elif select == '0':
					print('*'*60)
					print('Select one link you may need...\n[The first one enter "0" and so on]')
					print('*'*60)
					link_index = input('You Select:')
					try:
						link_index = int(link_index)
					except:
						print('Error Enter...')
						continue
					if (link_index<0) or (link_index>len(results[page])-1):
						print('Index Error...')
						time.sleep(5)
						continue
					show_Web(results[page][link_index][1])
				else:
					print('Error Enter...')
					continue		
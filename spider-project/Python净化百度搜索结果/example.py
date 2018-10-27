import BaiduSearch_Spider


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
			print('[INFO]:Start to save data...')
			f = open('results.txt', 'w', encoding='utf-8')
			f.truncate()
			f.close()
			f = open('results.txt', 'a', encoding='utf-8')
			for i in range(page_num):
				f.write('Page%s:\n' % i)
				contents = results[i]
				for c in contents:
					f.write(str(c[0])+':'+str(c[1])+'\n')
			f.close()
			print('All things Done...')




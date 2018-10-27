import requests
import json
from bs4 import BeautifulSoup


def main():
	headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.32 Safari/537.36'
		}
	cities = {'city_name': [], 'city_url': []}
	first_letter = ''.join(map(chr, range(65, 91)))
	cityid = 'city-{}'
	url = 'http://www.meituan.com/changecity/'
	res = requests.get(url, headers=headers)
	soup = BeautifulSoup(res.text, 'lxml')
	for i in range(26):
		letter = first_letter[i]
		try:
			temp1 = soup.find('div', attrs={'id': cityid.format(letter)})
		except:
			print('[INFO]: temp1 Error by %s' % letter)
			continue
		try:
			temp2 = temp1.findAll('a', attrs={'class', True})
		except:
			print('[INFO]: temp2 Error by %s' % letter)
			continue
		print('[INFO]: Getting %s...' % letter)
		for a in temp2:
			print('%s: %s' % (a.string.strip(), 'http:'+a.attrs['href']))
			cities['city_name'].append(a.string.strip())
			cities['city_url'].append('http:'+a.attrs['href'])
	with open('cities_url.json', 'w') as f:
		json.dump(cities, f)
		f.close()



if __name__ == '__main__':
	main()
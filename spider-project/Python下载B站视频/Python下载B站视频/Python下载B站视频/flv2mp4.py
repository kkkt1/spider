# 作者： Charles
# 公众号： Charles的皮卡丘
# flv转mp4
import os


def transfer(flvpath, mp4path='./results'):
	if not os.path.exists(mp4path):
		os.mkdir(mp4path)
	files = sorted(os.listdir(flvpath))
	for file in files:
		if file[-3:] == 'flv':
			origin = os.path.join(flvpath, file)
			target = os.path.join(mp4path, file[:-3] + 'mp4')
			os.system('ffmpeg -i {} {}'.format(origin, target))


if __name__ == '__main__':
	transfer(flvpath='./videos')
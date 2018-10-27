# 初始化
# 作者: Charles
# 公众号: Charles的皮卡丘
import os


DATA_DIR = './data'
RESULTS_DIR = './results'


if not os.path.exists(DATA_DIR):
	os.mkdir(DATA_DIR)
if not os.path.exists(RESULTS_DIR):
	os.mkdir(RESULTS_DIR)
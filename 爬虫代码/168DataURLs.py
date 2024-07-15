# Editor:CharPy
# Edit time:2024/6/8 10:00
import time
import requests
from bs4 import BeautifulSoup
import urllib3
import random
import tqdm
# from selenium.webdriver.common.by import By
urllib3.disable_warnings()

# 读取headers文件
with open("My-Headers.txt", 'r', encoding='utf-8') as f:
	headers = eval(f.read())

# 获取每辆车的主页链接
def getCarPageURLs(PROV, PVAR):
	frontURL = "https://www.che168.com/{0}/list".format(PROV)
	frontResp = requests.get(frontURL, headers = headers)
	frontHtml = frontResp.content
	frontSoup = BeautifulSoup(frontHtml, 'html.parser')
	sumCars = frontSoup.find("div", class_ = "list-menu").find("a").get_text().replace("全部车源", "")
	sumCars = int(sumCars.replace("(", "").replace(")", ""))
	wantedPages = round((sumCars // 10) / 56)
	if wantedPages == 0:
		wantedPages = 1
	print("{0} requires {1} page(s)".format(PROV, wantedPages))

	Soups = []
	for i in tqdm.trange(1, wantedPages+1):
		# 首页
		url = "https://www.che168.com/{0}/a0_0msdgscncgpi1ltocsp{1}exx0/?pvareaid={2}". \
			format(PROV, str(i), PVAR)
		resp = requests.get(url, headers = headers)
		html = resp.content
		Soups.append(BeautifulSoup(html, 'html.parser'))
		time.sleep(random.uniform(2.5, 4.5))

	carCarPageURLs = []  # 存储所有汽车主页的链接
	for soup in Soups:  # 范围为(1, 101)
		try:
			allCars = soup.find("div", class_ = "tp-cards-tofu fn-clear").find("ul").find_all("li")
			for j in allCars:
				# 参数href即所需网址
				carURLs = j.find("a").get('href').split("?")[0]
				carCarPageURLs.append('https://www.che168.com' + carURLs)
		except AttributeError:
			break
		# print('--------------------------')
	return carCarPageURLs

# 按省份收集URL
provinces = {"beijing": 11, "shanghai": 31, "tianjin": 12, "chongqing": 50, "hebei": 13, "henan": 41, "hubei": 42, "hunan": 43, "shandong": 37, "shanxi": 14,
			 "sichuan": 51, "guizhou": 52, "yunnan": 53, "fujian": 35, "guangdong": 44, "guangxi": 45, "hainan": 46, "zhejiang": 33, "jiangsu": 32, "jiangxi": 36,
			 "heilongjiang": 23, "jilin": 22, "liaoning": 21, "gansu": 62, "qinghai": 63, "ningxia": 64, "xinjiang": 65, "shan_xi": 61, "anhui": 34, "namenggu": 15}
pvarid = 102179
for prov in provinces.keys():
	carPageURLs = getCarPageURLs(prov, pvarid)
	with open("URL/Large/CarPageURLs000000000000{0}.txt".format(provinces[prov]), 'w', encoding = 'utf-8') as f:
		f.write(str(carPageURLs))
		print("{0} done".format(prov))

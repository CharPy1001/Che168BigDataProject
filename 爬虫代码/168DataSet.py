# Editor:CharPy
# Edit time:2024/6/1 20:25
import os
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3
import random
from selenium import webdriver
from requests.exceptions import ConnectionError
# from selenium.webdriver.common.by import By
urllib3.disable_warnings()

# 读取headers文件
with open("My-Headers.txt", 'r', encoding='utf-8') as f:
	headers = eval(f.read())

# 定义表结构
frameColumns = ["CID", "动力类型", "厂商", "名称", "级别", "轴距(mm)",
				"报价(万)", "比新车便宜(万)", "所在地", "颜色", "表显里程", "年份", "上牌时间", "整车质保",
				"气缸数", "进气形式", "最大功率(Ps)", "最大扭矩(N·m)",
				"排量(mL)", "油箱容量(L)", "燃油标号", "环保标准",
				"电机类型", "电机布局", "电机总功率(Ps)", "电机总扭矩(N·m)",
				"电池类型", "电池容量(kWh)", "快充功能", "电池组质保",
				"变速箱挡位数", "变速箱类型",
				"驱动方式", "车体结构", "前悬架类型", "后悬架类型"]
# 详细信息的网站标识和导出csv中的列名对照关系如下: {"网页标识": "csv列名", ...}
infoPageBasics = {"厂商": "厂商", "车型名称": "名称",
				  "能源类型": "动力类型", "整车质保": "整车质保"}
infoPageBody = {"轴距(mm)": "轴距(mm)", "油箱容积(L)": "油箱容量(L)"}
infoPageEngine = {"气缸数(个)": "气缸数", "进气形式": "进气形式", "最大马力(Ps)": "最大功率(Ps)",
				  "最大扭矩(N·m)": "最大扭矩(N·m)", "排量(mL)": "排量(mL)",
				  "燃油标号": "燃油标号", "环保标准": "环保标准"}
infoPageMotor = {"电机类型": "电机类型", "电机布局": "电机布局",
				 "电动机总功率(Ps)": "电机总功率(Ps)", "电动机总扭矩(N·m)": "电机总扭矩(N·m)",
				 "电池类型": "电池类型", "电池能量(kWh)": "电池容量(kWh)",
				 "快充功能": "快充功能", "电池组质保": "电池组质保"}
infoPageGearbox = {"挡位个数": "变速箱挡位数", "变速箱类型": "变速箱类型"}
infoPageChassis = {"驱动方式": "驱动方式", "车体结构": "车体结构",
				   "前悬架类型": "前悬架类型", "后悬架类型": "后悬架类型"}
requiredInfoDict = {"基本参数": infoPageBasics, "车身": infoPageBody,
					"发动机": infoPageEngine, "电动机": infoPageMotor,
					"变速箱": infoPageGearbox, "底盘转向": infoPageChassis}

# 从车辆主页获取参数配置详情页
def jumpToInfoPage(carURL):
	resp = requests.get(carURL, headers=headers)
	html = resp.content
	soup = BeautifulSoup(html, 'html.parser')
	infoPageURL = "NoURL"
	try:
		LIs = soup.find("div", class_ = 'all-basic-content fn-clear').find_all("ul")[2].find_all("li")
		for item in LIs:
			if item.find("a") is not None:
				href = item.find("a").get('href')
				# print(href)
				if href != "javascript:void(0);":  # 直接抓到详情页
					infoPageURL = "https:{0}".format(href)
				else:  # 无法直接抓到详情页url，则抓取infoid并拼接后返回
					infoid = item.find("a").get("infoid")
					infoPageURL = "https://www.che168.com/CarConfig/CarConfig.html?infoid={0}".format(infoid)
		print("--infoPageURL:", infoPageURL)
	except AttributeError:
		print("--infoPageURL:", infoPageURL)
	return infoPageURL

def mergeDataFrame(fileFolder, dataPaths, gotSuffix):
	if gotSuffix is None:
		print("!!!文件后缀为空，无法合并")
		return
	if len(dataPaths) == 1:
		print("!!!文件夹中只有一个文件，无需合并")
		return

	df1 = pd.read_csv("Data/{0}/{1}".format(fileFolder, dataPaths[0]))
	df2 = pd.read_csv("Data/{0}/{1}".format(fileFolder, dataPaths[1]))
	newFrame = pd.concat([df1, df2], ignore_index = True)
	for i in range(2, len(dataPaths)):
		df = pd.read_csv("Data/{0}/{1}".format(fileFolder, dataPaths[i]))
		newFrame = pd.concat([newFrame, df], ignore_index = True)

	for dtp in dataPaths:
		os.remove("Data/{0}/{1}".format(fileFolder, dtp))
	print("触发合并, 得拥有{0}条数据的新DataFrame".format(len(newFrame)))

	newFrame.drop_duplicates(subset = 'CID')
	newFrame.to_csv("Data/{0}/二手之家{1}.csv".format(fileFolder, gotSuffix), index = False)


def save1(fileFolder, CarPageURLs, gotSuffix=None, gotSweeper=10):
	newSuffix = gotSuffix if gotSuffix is not None else time.strftime("%Y%m%d%H%M%S", time.localtime())
	with open("URL/{0}/CarPageURLs{1}.txt".format(fileFolder, newSuffix), "w", encoding = "utf-8") as urls:
		random.shuffle(CarPageURLs)  # 打乱URLs顺序
		urls.write(str(CarPageURLs))  # 导出剩余URL列表

	urlPaths = os.listdir("URL/{0}".format(fileFolder))
	if len(urlPaths) > gotSweeper+2:  # 合并零散的URLs
		print("触发合并, 删除中间多余的{0}份URL集合".format(gotSweeper))
		for ulp in urlPaths[1:len(urlPaths) - 1]:
			os.remove("URL/{0}/{1}".format(fileFolder, ulp))

def save2(dataFrame, fileFolder, CarPageURLs, gotSweeper=10):
	newSuffix = time.strftime("%Y%m%d%H%M%S", time.localtime())
	dataFrame.to_csv("Data/{0}/二手之家{1}.csv".format(fileFolder, newSuffix), index = False)  # 导出数据

	dataPaths = os.listdir("Data/{0}".format(fileFolder))
	if len(dataPaths) > gotSweeper:  # 合并零散的DataFrame
		mergeDataFrame(fileFolder, dataPaths, newSuffix)

	save1(fileFolder, CarPageURLs, newSuffix)

def calmDown(error=None):
	if error is None:
		time.sleep(random.uniform(3, 6))
	elif error == AttributeError:
		time.sleep(random.uniform(6, 12))
	elif error == TypeError:
		time.sleep(random.uniform(9, 18))
	elif error == ConnectionError:
		time.sleep(random.uniform(120, 180))


def grabInfo(fileFolder, fileSuffix, gotSweeper=10):
	if fileSuffix is None:
		print("!!!文件后缀为空，请重新设置")
		return True
	dataFrame = pd.DataFrame(columns = frameColumns)
	# 从文件读取车辆主页
	with open("URL/{0}/CarPageURLs{1}.txt".format(fileFolder, fileSuffix), "r", encoding = "utf-8") as urls:
		CarPageURLs = eval(urls.read())

	# 开始爬虫
	while len(CarPageURLs) > 0:
		index = len(dataFrame)  # 从dataFrame的末尾插入数据
		carURL = CarPageURLs.pop(0)  # 弹出车辆主页URL
		print("--carURL:", carURL)
		try:
			calmDown()  # 先睡一会儿，再爬

			'''准备工作'''
			carResp = requests.get(carURL, headers = headers)
			carHtml = carResp.content
			carSoup = BeautifulSoup(carHtml, 'html.parser')  # 车辆主页

			infoURL = jumpToInfoPage(carURL)  # 获取参数配置详情页URL
			if infoURL == "NoURL":  # 没有详情页，直接跳过
				continue
			# 有详情页，加入infoid
			dataFrame.loc[index, "CID"] = infoURL.split('=')[1]

			# infoResp = requests.get(infoURL)
			# infoHtml = infoResp.content
			# infoSoup = BeautifulSoup(infoHtml, 'html.parser')
			driver = webdriver.Edge()
			driver.get(infoURL)
			infoSoup = BeautifulSoup(driver.page_source, 'html.parser')  # 车辆详情页
			driver.quit()

			'''先爬取车辆卡片'''
			carbox = carSoup.find("div", class_ = 'car-box')

			year = carbox.find("h3").get_text()  # 获取车型年份
			yearPos = year.find("款")
			dataFrame.loc[index, "年份"] = year[yearPos - 4:yearPos]

			WhereWhenHowLong = carbox.find("ul", class_ = 'brand-unit-item fn-clear').\
				find_all("li")  # 获取所在地、上牌时间、表显里程
			for loc in WhereWhenHowLong:
				if loc.find("p").get_text() == "车辆所在地":
					dataFrame.loc[index, "所在地"] = loc.find("h4").get_text()
				if loc.find("p").get_text() == "上牌时间":
					dataFrame.loc[index, "上牌时间"] = loc.find("h4").get_text()
				if loc.find("p").get_text() == "表显里程":
					dataFrame.loc[index, "表显里程"] = loc.find("h4").get_text()

			# 再爬取车辆档案
			carPageRequiredNames = {"车辆级别": "级别", "车身颜色": "颜色"}
			carPageRequiredULs = carSoup.find("div", class_ = 'all-basic-content fn-clear').find_all("ul")
			for ul in carPageRequiredULs:  # 遍历以找出目标属性
				carPageRequiredLIs = ul.find_all("li")
				for li in carPageRequiredLIs:
					name = li.find("span").get_text()
					if name in carPageRequiredNames.keys():
						dataFrame.loc[index, carPageRequiredNames[name]] = li.get_text().replace(name, "")

			# 进入详情页爬取抬头
			priceCurr = infoSoup.find("div", class_ = 'source-info-con'). \
				find("p", class_ = 'sp-margin').find("span").get_text()
			priceOff = infoSoup.find("div", class_ = 'source-info-con'). \
				find("p", class_ = 'sp-margin').find("em", id = "newPriceHead").get_text()
			dataFrame.loc[index, "报价(万)"] = priceCurr.replace("￥", "").\
				replace("万", "")  # 获取报价
			dataFrame.loc[index, "比新车便宜(万)"] = priceOff.replace("比新车省:", "").\
				replace("万", "")  # 获取优惠价

			# 最后爬取表格
			foundTables = infoSoup.find("div", id = "configContent", class_ = "config-right-con").\
				find_all("table")
			for table in foundTables:
				TRs = table.find("tbody").find_all("tr")
				tableName = TRs[0].find("th").get_text()
				if tableName in requiredInfoDict.keys():
					# print("{0} bingo".format(tableName))
					for tr in TRs[1:]:
						infoName = tr.find("td", class_ = "table-left").get_text()
						if infoName in requiredInfoDict[tableName].keys():
							dataFrame.loc[index, requiredInfoDict[tableName][infoName]] = \
								tr.find("td", class_ = "table-right").get_text()
		except AttributeError or TypeError or ConnectionError as e:
			CarPageURLs.append(carURL)
			dataFrame = dataFrame.iloc[:-1]
			calmDown(e)
			if len(dataFrame) == 0:
				print("==爬虫中断，颗粒无收，保存URL")
				save1(fileFolder, CarPageURLs)
			else:
				print("==爬虫中断，得到数据，保存dataFrame和URL")
				save2(dataFrame, fileFolder, CarPageURLs, gotSweeper)
			return False

	save2(dataFrame, fileFolder, CarPageURLs)
	print("!!爬虫结束，保存dataFrame和URL")
	return True


def getSuffix(fileFolder, fileSuffix=None):
	if fileSuffix is None:
		Path = os.listdir("URL/{0}".format(fileFolder))
		fileSuffix = Path[-1][11:25] if len(Path) != 0 else None
	return fileSuffix

# 输入现有车辆主页URL合集的文件后缀，爬取数据并保存到CSV文件
folder = "Wide"  # 操作的文件夹，本文档仅仅适用于Large和Test两个文件夹
mode = bool(1)  # 0为合并模式; 1为爬虫模式
if mode:
	suffix = getSuffix(folder, fileSuffix = None)  # 在以上选定的文件夹中自动获取后缀，也可在fileSuffix人工传入
	result = grabInfo(folder, suffix)
	while not result:
		suffix = os.listdir("URL/{0}".format(folder))[-1][11:25]
		result = grabInfo(folder, suffix)
donePath = os.listdir("Data/{0}".format(folder))
doneSuffix = donePath[-1][4:18] if len(donePath) != 0 else None
mergeDataFrame(folder, donePath, doneSuffix)

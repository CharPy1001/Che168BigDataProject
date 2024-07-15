import mysql.connector
from mysql.connector import Error
import matplotlib.pyplot as plt
import matplotlib
import csv
import numpy as np
# 字体设置
font = {'family': 'MicroSoft YaHei',
        'weight': 'bold'}
matplotlib.rc("font", **font)

# 数据库连接参数
db_config = {
    'host': 'localhost',
    'database': 'hadoop_visualize',
    'user': 'root',
    'password': 'Lhr20030514'
}

# 创建数据库连接
try:
    connection = mysql.connector.connect(**db_config)
    if connection.is_connected():
        # ----------------------------------------------------------#
        cursor = connection.cursor()
        # 选择数据库中的所在地的集合
        cursor.execute("SELECT DISTINCT 所在地 FROM car")
        # 获取查询结果
        uni_result = cursor.fetchall()
        # 创建字典
        location_dict = {}
        for item in uni_result:
            location_dict[item[0]] = 0

        # 选择数据库中的所在地的全部信息
        cursor.execute("SELECT 所在地 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        # 将全部结果输入到字典中
        for item in result:
            if item != 'None':
                location_dict[item[0]] += 1
        location_dict = dict(sorted(location_dict.items(),
                             key=lambda item: item[1], reverse=True))
        del location_dict[None]
        # 提取键和值
        keys = list(location_dict.keys())[0:20]
        values = list(location_dict.values())[0:20]

        # 创建水平柱状图
        plt.barh(keys, values)

        # 设置图表标题和坐标轴标签
        plt.title('排名前20城市二手车市场拥有量分布图')
        plt.xlabel('数量')
        plt.ylabel('城市')
        plt.xticks(np.arange(0, 1001, 100))

        # 显示图表
        plt.show()
        # ------------------------------------------------------------------------------------#
        city_2_province_dict = {'东莞': '广东', '北京': '北京', '上海': '上海', '郑州': '河南', '杭州': '浙江', '广州': '广东', '深圳': '广东', '长沙': '湖南', '石家庄': '河北', '佛山': '广东', '合肥': '安徽', '苏州': '江苏', '沈阳': '辽宁', '西安': '陕西', '南宁': '广西', '济南': '山东',
                                '昆明': '云南', '南京': '江苏', '武汉': '湖北', '泉州': '福建', '青岛': '山东', '宁波': '浙江', '无锡': '江苏', '中山': '广东',
                                '成都': '四川', '哈尔滨': '黑龙江', '长春': '吉林', '温州': '浙江', '贵阳': '贵州', '厦门': '福建', '天津': '天津', '常州': '江苏', '太原': '山西', '大连': '辽宁', '南昌': '江西',
                                '台州': '浙江', '金华': '浙江', '徐州': '江苏', '惠州': '广东', '重庆': '重庆', '海口': '海南', '潍坊': '山东', '嘉兴': '浙江', '淄博': '山东', '乌鲁木齐': '新疆', '临沂': '山东', '兰州': '甘肃', '桂林': '广西', '唐山': '河北', '福州': '福建', '廊坊': '河北', '绍兴': '浙江', '沧州': '河北', '柳州': '广西',
                                '湖州': '浙江', '保定': '河北', '呼和浩特': '内蒙古', '邯郸': '河北', '遵义': '贵州', '赣州': '江西', '珠海': '广东',
                                '济宁': '山东', '烟台': '山东', '南通': '江苏', '菏泽': '山东', '镇江': '江苏', '包头': '内蒙古', '江门': '广东',
                                '扬州': '江苏', '邢台': '河北', '襄阳': '湖北', '漳州': '福建', '西宁': '青海', '银川': '宁夏', '汕头': '广东', '鄂尔多斯': '内蒙古', '威海': '山东',
                                '丽水': '浙江', '清远': '广东', '揭阳': '广东', '莆田': '福建', '上饶': '江西', '泰安': '山东', '晋中': '山西', '衢州': '浙江', '安阳': '河南', '三明': '福建', '赤峰': '内蒙古', '盐城': '江苏',
                                '运城': '山西', '湛江': '广东', '洛阳': '河南', '新余': '江西', '聊城': '山东', '平顶山': '河南', '南阳': '河南', '松原': '吉林', '三亚': '海南',
                                '绵阳': '四川', '衡阳': '湖南', '自贡': '四川', '芜湖': '安徽', '商丘': '河南', '信阳': '河南', '云浮': '广东', '衡水': '河北', '德州': '山东', '红河': '云南', '枣庄': '山东', '鞍山': '辽宁', '钦州': '广西',
                                '肇庆': '广东', '秦皇岛': '河北', '泰州': '江苏', '通辽': '内蒙古', '阜阳': '安徽', '池州': '安徽', '潮州': '广东', '雅安': '四川',
                                '许昌': '河南', '宜春': '江西', '日照': '山东', '曲靖': '云南', '滁州': '安徽', '淮安': '江苏', '大同': '山西', '东营': '山东', '景德镇': '江西', '河源': '广东',
                                '宁德': '福建', '梅州': '广东', '株洲': '湖南', '中卫': '宁夏', '濮阳': '河南'}
        # 初始化省份字典
        province_dict = {}
        for key, value in city_2_province_dict.items():
            if value not in province_dict:
                province_dict[value] = 0
        for key, value in location_dict.items():
            province_dict[city_2_province_dict[key]] += value

        # 从多到少进行排序
        province_dict = dict(sorted(province_dict.items(),
                             key=lambda item: item[1], reverse=True))
        # 提取键和值
        keys = list(province_dict.keys())
        values = list(province_dict.values())

        # 创建水平柱状图
        plt.barh(keys, values)

        # 设置图表标题和坐标轴标签
        plt.title('各省份二手车市场拥有量分布图')
        plt.xlabel('数量')
        plt.ylabel('城市')

        # 显示图表
        plt.show()
        # ------------------------------------------------------------------------------------#
        # 初始化省会副省字典
        important_city_dict = {"重庆": "重庆", "上海": "上海", "天津": "天津", "北京": "北京",
                               "广州": "广东",
                               "深圳": "广东",
                               "南宁": "广西",
                               "海口": "海南",
                               "福州": "福建",
                               "厦门": "福建",
                               "石家庄": "河北",
                               "郑州": "河南",
                               "呼和浩特": "内蒙古",
                               "杭州": "浙江",
                               "宁波": "浙江",
                               "南京": "江苏",
                               "南昌": "江西",
                               "武汉": "湖北",
                               "长沙": "湖南",
                               "哈尔滨": "黑龙江",
                               "沈阳": "辽宁",
                               "大连": "辽宁",
                               "长春": "吉林",
                               "西安": "陕西",
                               "合肥": "安徽",
                               "太原": "山西",
                               "济南": "山东",
                               "青岛": "山东",
                               "乌鲁木齐": "新疆",
                               "成都": "四川",
                               "贵阳": "贵州",
                               "昆明": "云南",
                               "兰州": "甘肃",
                               "银川": "宁夏",
                               "西宁": "青海"}
        important_city = {}
        for key, value in important_city_dict.items():
            important_city[value] = 0
        for key, value in location_dict.items():
            if key in important_city_dict.keys():
                important_city[important_city_dict[key]] += value
        # 根据值排序
        important_city = dict(sorted(important_city.items(),
                                          key=lambda item: item[1], reverse=True))
        # 提取键和值
        keys = list(important_city.keys())
        values = list(important_city.values())

        # 创建水平柱状图
        plt.bar(keys, values)

        # 设置图表标题和坐标轴标签
        plt.title('各省会及其副城市占全省二手车保有量图')
        plt.xlabel('省份')
        plt.ylabel('数量')
        plt.xticks(rotation=45)

        # 显示图表
        plt.show()

        important_city_rate = {}
        for key, value in important_city.items():
            important_city_rate[key] = 0
        for key, value in important_city.items():
            important_city_rate[key] = round(
                important_city[key]/province_dict[key], 2)

        # 换Key
        for key, value in important_city_dict.items():
            if value not in ["山东", "浙江", "广东", "福建", "辽宁"]:
                important_city_rate[key] = important_city_rate.pop(value)
        # 处理特殊值
        important_city_rate["广州+深圳"] = important_city_rate.pop("广东")
        important_city_rate["青岛+济南"] = important_city_rate.pop("山东")
        important_city_rate["杭州+宁波"] = important_city_rate.pop("浙江")
        important_city_rate["沈阳+大连"] = important_city_rate.pop("辽宁")
        important_city_rate["厦门+福州"] = important_city_rate.pop("福建")
        # 根据值排序
        important_city_rate = dict(sorted(important_city_rate.items(),
                                          key=lambda item: item[1], reverse=True))
        # 提取键和值
        keys = list(important_city_rate.keys())
        values = list(important_city_rate.values())

        # 创建水平柱状图
        plt.bar(keys, values)

        # 设置图表标题和坐标轴标签
        plt.title('各省会及其副城市占全省二手车比例图')
        plt.xlabel('省份')
        plt.ylabel('比例')
        plt.xticks(rotation=45)

        # 显示图表
        plt.show()
        # ------------------------------------------------------------------------------------#
        # 从多到少进行排序
        province_dict = dict(sorted(province_dict.items(),
                             key=lambda item: item[1], reverse=True))
        # 提取键和值
        keys = list(province_dict.keys())
        values = list(province_dict.values())

        # 创建水平柱状图
        plt.barh(keys, values)

        # 设置图表标题和坐标轴标签
        plt.title('各省份二手车市场拥有量分布图')
        plt.xlabel('数量')
        plt.ylabel('省份')

        # 显示图表
        plt.show()
        # ------------------------------------------------------------------------------------#

        # 选择数据库中的报价的最小值和最大值
        cursor.execute(
            "SELECT MIN(报价) AS min_quote,MAX(报价) AS max_quote FROM car;")
        # 获取查询结果
        result = cursor.fetchall()
        # 读取到数据范围约为(0,1000)万元
        price_min = result[0][0]
        price_max = result[0][1]

        # 选择数据库中的报价的全部数据
        cursor.execute(
            "SELECT 报价 FROM car;")
        # 获取查询结果
        result = cursor.fetchall()

        # 创建价段字典
        price_dict = {}
        price_labels = ['0-100万', '100-200万', '200-300万', '300-400万', '400-500万',
                        '500-600万', '600-700万', '700-800万', '800-900万', '900-1000万']
        # 初始化字典
        for item in price_labels:
            price_dict[item] = 0
        price = []
        for item in result:
            # 判断价格是否在某个价段内
            if item[0] >= 0 and item[0] < 100:
                price_dict[price_labels[0]] += 1
            elif item[0] >= 100 and item[0] < 200:
                price_dict[price_labels[1]] += 1
            elif item[0] >= 200 and item[0] < 300:
                price_dict[price_labels[2]] += 1
            elif item[0] >= 300 and item[0] < 400:
                price_dict[price_labels[3]] += 1
            elif item[0] >= 400 and item[0] < 500:
                price_dict[price_labels[4]] += 1
            elif item[0] >= 500 and item[0] < 600:
                price_dict[price_labels[5]] += 1
            elif item[0] >= 600 and item[0] < 700:
                price_dict[price_labels[6]] += 1
            elif item[0] >= 700 and item[0] < 800:
                price_dict[price_labels[7]] += 1
            elif item[0] >= 800 and item[0] < 900:
                price_dict[price_labels[8]] += 1
            elif item[0] >= 900 and item[0] < 1000:
                price_dict[price_labels[9]] += 1

        # 提取键和值
        keys = list(price_dict.keys())[0:3]
        values = list(price_dict.values())[0:3]
        # 合并占比太小的扇形
        keys.append('300万以上')
        sum = 0
        for i in range(2, len(price_dict.keys())):
            sum += 1
        values.append(sum)
        # 绘制饼图
        explode = np.random.random(4)/10
        plt.figure(figsize=(10, 10))  # 设置画布大小
        plt.pie(values, labels=keys, explode=explode,
                autopct='%1.2f%%', pctdistance=1.1, labeldistance=1.2)
        plt.title("二手车价格占比图")  # 设置标题
        # 绘制条形图
        # # 设置图表标题和坐标轴标签
        # plt.title('各个价位段二手车市场拥有额')
        # plt.xlabel('价位')
        # plt.ylabel('数量')
        # plt.xticks(rotation=0, fontsize=10)

        # 显示图表
        plt.show()

        # ------------------------------------------------------------------------------------#
        # 100万元内二手车各价段分布图
        price_dict_0_100 = {}
        price_labels_0_100 = ['0-10万', '10-20万', '20-30万', '30-40万', '40-50万',
                              '50-00万', '60-70万', '70-80万', '80-90万', '90-100万']
        for item in price_labels_0_100:
            price_dict_0_100[item] = 0
        for item in result:
            # 判断价格是否在某个价段内
            if item[0] >= 0 and item[0] < 10:
                price_dict_0_100[price_labels_0_100[0]] += 1
            elif item[0] >= 10 and item[0] < 20:
                price_dict_0_100[price_labels_0_100[1]] += 1
            elif item[0] >= 20 and item[0] < 30:
                price_dict_0_100[price_labels_0_100[2]] += 1
            elif item[0] >= 30 and item[0] < 40:
                price_dict_0_100[price_labels_0_100[3]] += 1
            elif item[0] >= 40 and item[0] < 50:
                price_dict_0_100[price_labels_0_100[4]] += 1
            elif item[0] >= 50 and item[0] < 60:
                price_dict_0_100[price_labels_0_100[5]] += 1
            elif item[0] >= 60 and item[0] < 70:
                price_dict_0_100[price_labels_0_100[6]] += 1
            elif item[0] >= 70 and item[0] < 80:
                price_dict_0_100[price_labels_0_100[7]] += 1
            elif item[0] >= 80 and item[0] < 90:
                price_dict_0_100[price_labels_0_100[8]] += 1
            elif item[0] >= 90 and item[0] < 100:
                price_dict_0_100[price_labels_0_100[9]] += 1
        # 提取键和值
        keys = list(price_dict_0_100.keys())
        values = list(price_dict_0_100.values())

        # 创建竖直柱状图
        # plt.bar(keys, values, lw=2)
        # # 设置图表标题和坐标轴标签
        # plt.title('100万元内二手车价格分布图')
        # plt.xlabel('价位')
        # plt.ylabel('数量')
        # plt.xticks(rotation=0, fontsize=10)

        # 绘制饼图
        explode = np.random.random(len(price_dict_0_100.keys()))/10
        plt.figure(figsize=(10, 10))  # 设置画布大小
        plt.pie(values, labels=keys, explode=explode,
                autopct='%1.2f%%', pctdistance=1.1, labeldistance=1.2)
        plt.title("100万元内二手车价格饼图")  # 设置标题

        # 显示图表
        plt.show()
        # ------------------------------------------------------------------------------------#
        cursor = connection.cursor()
        # 选择数据库中的所在地的集合
        cursor.execute("SELECT DISTINCT 厂商 FROM car")
        # 获取查询结果
        uni_result = cursor.fetchall()
        # 创建字典
        brand_dict = {}
        for item in uni_result:
            brand_dict[item[0]] = 0

        # 选择数据库中的所在地的全部信息
        cursor.execute("SELECT 厂商 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        # 将全部结果输入到字典中
        for item in result:
            if item != 'None':
                brand_dict[item[0]] += 1
        brand_dict = dict(sorted(brand_dict.items(),
                                 key=lambda item: item[1], reverse=True))

        # 提取键和值
        keys = list(brand_dict.keys())
        values = list(brand_dict.values())

        # 创建水平柱状图
        plt.barh(keys[0:10], values[0:10])

        # 设置图表标题和坐标轴标签
        plt.title('各品牌二手车市场拥有量分布图')
        plt.xlabel('品牌')
        plt.ylabel('数量')

        # 显示图表
        plt.show()

        # --------------------------------------------------------------#
        # SUV和普通车类型
        Normal_category = ['微型车', '小型车', '紧凑型车', '中型车', '中大型车', '大型车']
        SUV_category = ['小型SUV', '紧凑型SUV', '中型SUV', '中大型SUV', '大型SUV']

        cursor = connection.cursor()
        # 选择数据库中的所在地的集合
        cursor.execute("SELECT 级别,轴距,报价 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        # 数据格式[[级别,轴距,报价],[级别,轴距,报价]...
        SUV_dict = []
        Normal_dict = []

        # 区分SUV和轿车数据
        for item in result:
            # 清理空值
            if item[0] != None:
                if item[0] in SUV_category:
                    SUV_dict.append(item)
                elif item[0] in Normal_category:
                    Normal_dict.append(item)
        # 存储结构
        SUV_price = {item: [] for item in SUV_category}
        Normal_price = {item: [] for item in Normal_category}

        # SUV数据分类处理
        for item, wheelbase, price in SUV_dict:
            if item in SUV_category:
                SUV_price[SUV_category[SUV_category.index(item)]].append(price)
            elif wheelbase <= 2500:
                SUV_price[SUV_category[0]].append(price)
            elif wheelbase > 2500 and wheelbase <= 2700:
                SUV_price[SUV_category[1]].append(price)
            elif wheelbase > 2700 and wheelbase <= 2900:
                SUV_price[SUV_category[2]].append(price)
            elif wheelbase > 2900 and wheelbase <= 3000:
                SUV_price[SUV_category[3]].append(price)
            else:
                SUV_price[SUV_category[4]].append(price)

        # 轿车数据分类处理
        for item, wheelbase, price in Normal_dict:
            if item in Normal_category:
                Normal_price[Normal_category[Normal_category.index(item)]].append(
                    price)
            elif wheelbase > 2000 and wheelbase <= 2300:
                Normal_price[Normal_category[0]].append(price)
            elif wheelbase > 2300 and wheelbase <= 2500:
                Normal_price[Normal_category[1]].append(price)
            elif wheelbase > 2500 and wheelbase <= 2700:
                Normal_price[Normal_category[2]].append(price)
            elif wheelbase > 2700 and wheelbase <= 2900:
                Normal_price[Normal_category[3]].append(price)
            elif wheelbase > 2800 and wheelbase <= 3000:
                Normal_price[Normal_category[4]].append(price)
            else:
                Normal_price[Normal_category[5]].append(price)

        # 绘制SUV箱型图
        box_1, box_2, box_3, box_4, box_5 = SUV_price['小型SUV'], SUV_price[
            '紧凑型SUV'], SUV_price['中型SUV'], SUV_price['中大型SUV'], SUV_price['大型SUV']
        plt.subplot(221)
        labels = '小型SUV', '紧凑型SUV', '中型SUV', '中大型SUV', '大型SUV'  # 图例
        plt.boxplot([box_1, box_2, box_3, box_4, box_5], notch=False, labels=labels, patch_artist=False, boxprops={'color': 'black', 'linewidth': '2.0'},
                    capprops={'color': 'black', 'linewidth': '2.0'})
        plt.xlabel("类别", fontsize=8)
        plt.ylabel('价格', fontsize=8)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        plt.show()
        # 绘制SUV条形图

        # 绘制轿车箱型图
        box_1, box_2, box_3, box_4, box_5, box_6 = Normal_price['微型车'], Normal_price[
            '小型车'], Normal_price['紧凑型车'], Normal_price['中型车'], Normal_price['中大型车'], Normal_price['大型车']
        plt.subplot(221)
        labels = '微型车', '小型车', '紧凑型车', '中型车', '中大型车', '大型车'  # 图例
        plt.boxplot([box_1, box_2, box_3, box_4, box_5, box_6], notch=False, labels=labels, patch_artist=False, boxprops={'color': 'black', 'linewidth': '2.0'},
                    capprops={'color': 'black', 'linewidth': '2.0'})
        plt.xlabel("类别", fontsize=8)
        plt.ylabel('价格', fontsize=8)
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)

        # # 绘制轿车条形图
        # plt.bar(keys[0:10], values[0:10])

        # # 设置图表标题和坐标轴标签
        # plt.title('各品牌二手车市场拥有量分布图')
        # plt.xlabel('品牌')
        # plt.ylabel('数量')
        plt.show()
        # ------------------------------------------------------------------------------------ #
        # 时间图
        time_dict = {}
        cursor = connection.cursor()
        # 选择数据库中的时间的集合
        cursor.execute("SELECT DISTINCT 年份 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            if item[0] != None and item[0] != 0:
                # 累计总量
                time_dict[int(item[0])] = 0
        #
        cursor.execute("SELECT 年份 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            if item[0] != None and item[0] != 0:
                # 累计总量
                time_dict[int(item[0])] += 1
        # 字典按时间倒序排序
        time_dict = dict(sorted(time_dict.items(),
                                key=lambda item: item[0], reverse=True))
        # 绘制年份条形图
        # 获取X,Y轴数据
        count = list(time_dict.values())
        time = list(time_dict.keys())
        # time.append(2023)
        # count.append(0)
        plt.bar(time, count)
        # 设置X,Y轴题目
        plt.xlabel('年份')
        plt.ylabel('数量')
        # 设置X轴标签并旋转（使美观）
        plt.xticks(np.arange(2004, 2025, 1), rotation=45)
        ax = plt.gca()
        ax.invert_xaxis()
        plt.show()
        # ---------------------------------------------------------------------------------------- #
        # 环保标准
        standard_dict = {}
        cursor = connection.cursor()
        # 选择数据库中的时间的集合
        cursor.execute("SELECT DISTINCT 环保标准 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            if item[0] != None:
                # 累计总量
                standard_dict[item[0]] = 0
        # 转换列
        standard_dict["国IV"] = standard_dict.pop("国IV(国V)")
        #
        cursor.execute("SELECT 环保标准 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            if item[0] != None:
                if item[0] == '国IV(国V)':
                    standard_dict['国IV'] += 1
                # 累计总量
                else:
                    standard_dict[item[0]] += 1
        standard_dict = dict(sorted(standard_dict.items(),
                                    key=lambda item: item[1], reverse=True))
        # 提取键和值
        keys = list(standard_dict.keys())[0:6]
        values = list(standard_dict.values())[0:6]
        # 合并占比太小的扇形
        keys.append('其他')
        sum = 0
        for i in range(6, len(standard_dict.keys())):
            sum += 1
        values.append(sum)
        # 绘制饼图
        explode = np.random.random(7)/10
        plt.figure(figsize=(10, 10))  # 设置画布大小
        plt.pie(values, labels=keys, explode=explode,
                autopct='%1.2f%%', pctdistance=1.1, labeldistance=1.2)
        plt.title("二手车环保标准占比图")  # 设置标题

        plt.show()
        # ---------------------------------------- #
        # 环保标准
        standard_dict = {}
        cursor = connection.cursor()
        # 选择数据库中的时间的集合
        cursor.execute("SELECT DISTINCT 环保标准 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            if item[0] != None:
                # 累计总量
                standard_dict[item[0]] = 0
        # 转换列
        standard_dict["国IV"] = standard_dict.pop("国IV(国V)")
        #
        cursor.execute("SELECT 环保标准 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            if item[0] != None:
                if item[0] == '国IV(国V)':
                    standard_dict['国IV'] += 1
                # 累计总量
                else:
                    standard_dict[item[0]] += 1
        standard_dict = dict(sorted(standard_dict.items(),
                                    key=lambda item: item[1], reverse=True))
        # 提取键和值
        keys = list(standard_dict.keys())[0:6]
        values = list(standard_dict.values())[0:6]
        # 合并占比太小的扇形
        keys.append('其他')
        sum = 0
        for i in range(6, len(standard_dict.keys())):
            sum += 1
        values.append(sum)
        # 绘制饼图
        explode = np.random.random(7)/10
        plt.figure(figsize=(10, 10))  # 设置画布大小
        plt.pie(values, labels=keys, explode=explode,
                autopct='%1.2f%%', pctdistance=1.1, labeldistance=1.2)
        plt.title("二手车环保标准占比图")  # 设置标题

        plt.show()
        # --------------------------------------------------------------------- #
        # 贬值率-表显里程关系图
        low_price_distance_rate = {}
        low_price_rate = []
        distance = []
        cursor = connection.cursor()
        # 选择数据库中的时间的集合
        cursor.execute("SELECT 报价,比新车便宜,表显里程 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            if None not in item and item[0] < 60:
                # 计算贬值率，并且放入字典中
                # low_price_distance_rate[float(item[2].split(
                #     '万')[0])*10000] = round(item[1]/(item[0]+item[1]), 2)
                low_price_rate.append(round(item[1]/(item[0]+item[1]), 2))
                distance.append(float(item[2].split('万')[0])*10000)

        # 绘制散点图
        keys = np.array(low_price_rate)
        values = np.array(distance)

        plt.scatter(values, keys, color='green', marker='o')
        plt.title("贬值率-表显里程关系图")  # 设置标题
        # 设置X,Y轴题目
        plt.xlabel('表显里程')
        plt.ylabel('贬值率')
        plt.xticks(np.arange(0, 350001, 10000), rotation=45)
        plt.show()

        # --------------------------------------------------------------------- #
        # 颜色分布图
        color_dict = {}
        cursor = connection.cursor()
        # 选择数据库中的颜色的集合
        cursor.execute("SELECT 颜色 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            # 判断item列表中是否包含None
            if None not in item:
                # 如果包含None，则跳过此循环
                color = item[0].split('/')
                # 遍历color列表
                for i in color:
                    # 如果i不在color_dict中，则将其添加到color_dict中，并设置值为1
                    if i not in color_dict:
                        color_dict[i] = 1
                    # 如果i在color_dict中，则将其值加1
                    else:
                        color_dict[i] += 1
        # 提取键和值
        keys = (list(color_dict.keys()))
        values = (list(color_dict.values()))
        for i in keys:
            if len(i) == 1:
                keys[keys.index(i)] = i + '色'
        # 绘制饼图
        explode = np.random.random(len(color_dict.keys())) / 10
        plt.figure(figsize=(10, 10))  # 设置画布大小
        plt.pie(values, labels=keys, explode=explode,
                autopct='%1.2f%%', pctdistance=1.1, labeldistance=1.2)
        plt.title("二手车颜色占比图")  # 设置标题
        plt.show()

        # -------------------------------------------------------------------- #
        # 汽油车气缸数-进气形式散点图
        gas_cylinder_dict = {}
        cursor = connection.cursor()
        # 选择数据库中的颜色的集合
        cursor.execute("SELECT DISTINCT 进气形式 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            # 判断item列表中是否包含None
            if None not in item:
                # 如果包含None，则跳过此循环
                gas_cylinder_dict[item[0]] = []
        cursor = connection.cursor()
        # 选择数据库中的颜色的集合
        cursor.execute("SELECT 气缸数,进气形式 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            # 判断item列表中是否包含None
            if None not in item and item[0] > 0:
                # 如果包含None，则跳过此循环
                gas_cylinder_dict[item[1]].append(item[0])
                gas_cylinder_dict[item[1]] = list(
                    set(gas_cylinder_dict[item[1]]))
        # 提取键和值
        keys = np.array(list(gas_cylinder_dict.keys()))
        values = np.array(list(gas_cylinder_dict.values()))
        # print(list(gas_cylinder_dict.keys()))
        # print(gas_cylinder_dict)
        # # 绘制散点图
        # '手自一体变速箱(AT)', '自动变速箱(AT)', '湿式双离合变速箱(DCT)', '无级变速箱(CVT)', '固定齿比变速箱', '手动变速箱(MT)', '干式双离合变速箱(DCT)', '电子无级变速箱(E-CVT)', '混合动力专用变速箱(DHT)', '三离合电驱变速箱', '机械式自动变速箱(AMT)', 'ISR变速箱', 'E-CVT+自动变速箱'
        # plt.scatter(keys, values, color='red', marker='o')
        # plt.title("气缸数-进气形式关系图")  # 设置标题
        # # 设置X,Y轴题目
        # plt.xlabel('气缸数')
        # plt.ylabel('进气形式')
        # # 设置X轴范围
        # plt.yticks(np.arange(3, 9, 1))
        # plt.show()
        # -------------------------------------------------------------------- #
        # 前后悬架散点图
        front_rear_dict = {}
        cursor = connection.cursor()
        # -------------------------------------------------------------------- #
        # 变速器档位数-变速器类型散点图
        gear_transmiss_dict = {}
        cursor = connection.cursor()
        # 选择数据库中的颜色的集合
        cursor.execute("SELECT DISTINCT 变速箱类型 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            # 判断item列表中是否包含None
            if None not in item:
                # 如果包含None，则跳过此循环
                gear_transmiss_dict[item[0]] = []
        cursor.execute("SELECT 变速箱挡位数,变速箱类型 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            # 判断item列表中是否包含None
            if None not in item and item[1] != '-':
                # 如果包含None，则跳过此循环
                gear_transmiss_dict[item[1]].append(item[0])
                gear_transmiss_dict[item[1]] = list(
                    set(gear_transmiss_dict[item[1]]))
                gear_transmiss_dict[item[1]] = sorted(
                    gear_transmiss_dict[item[1]], reverse=True)
        # 提取键和值
        values = list(gear_transmiss_dict.values())
        keys = list(gear_transmiss_dict.keys())
        # print(gear_transmiss_dict)
        # -------------------------------------------------------------------- #
        # 二手车推价比-价格散点图
        push_price_dict = {}
        cursor = connection.cursor()
        # 选择数据库中的颜色的集合
        cursor.execute("SELECT 报价,最大功率 FROM car")
        # 获取查询结果
        result = cursor.fetchall()
        for item in result:
            # 数据清洗
            # 判断item列表中是否包含None
            if None not in item and item[0] <= 300:
                # 如果包含None，则跳过此循环
                push_price_dict[item[0]] = item[1]/item[0]
        # 提取键和值
        keys = np.array(list(push_price_dict.keys()))
        values = np.array(list(push_price_dict.values()))
        # 绘制散点图
        plt.scatter(keys, values, color='red', marker='.')
        plt.title("二手车推价比-价格关系图")  # 设置标题
        # 设置X,Y轴题目
        plt.xlabel('价格(万元)')
        plt.ylabel('推价比(最大功率/价格)')
        # 设置X轴范围
        plt.xticks(np.arange(0, 301, 20), rotation=45)
        plt.yticks(np.arange(0, 201, 8))

        plt.show()
        cursor.close()
        connection.close()

except Error as e:
    print("Error while connecting to MySQL", e)

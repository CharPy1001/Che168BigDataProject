from pyecharts.charts import Map
from pyecharts import options as opts
import pandas as pd
from pyecharts.faker import Faker

# 将省份和数量输出

province_list = {'广东省': 3396, '北京市': 860, '上海市': 833, '河南省': 839, '浙江省': 1843, '湖南省': 545, '河北省': 806, '安徽省': 505, '江苏省': 1621, '辽宁省': 628, '陕西省': 458, '广西壮族自治区': 554,
                 '山东省': 1211, '云南省': 416, '湖北省': 418, '福建省': 699, '四川省': 251, '黑龙江省': 232, '吉林省': 226, '贵州省': 239, '天津省': 200, '山西省': 191, '江西省': 204, '重庆市': 119,
                 '海南省': 120, '新疆维吾尔自治区': 93, '甘肃省': 81, '内蒙古自治区': 83, '青海省': 17, '宁夏回族自治区': 15}

province = list(province_list.keys())
number = list(province_list.values())

province_list = [list(z) for z in zip(province, number)]

# 省会城市数据
capital_cities = {
    '广东省': '广州', '北京市': '北京', '上海市': '上海', '河南省': '郑州', '浙江省': '杭州', '湖南省': '长沙', '河北省': '石家庄', '安徽省': '合肥',
    '江苏省': '南京', '辽宁省': '沈阳', '陕西省': '西安', '广西壮族自治区': '南宁', '山东省': '济南', '云南省': '昆明', '湖北省': '武汉',
    '福建省': '福州', '四川省': '成都', '黑龙江省': '哈尔滨', '吉林省': '长春', '贵州省': '贵阳', '天津省': '天津', '山西省': '太原',
    '江西省': '南昌', '重庆市': '重庆', '海南省': '海口', '新疆维吾尔自治区': '乌鲁木齐', '甘肃省': '兰州', '内蒙古自治区': '呼和浩特',
    '青海省': '西宁', '宁夏回族自治区': '银川', '西藏自治区': '拉萨', '南海诸岛': '', '台湾省': '台北'
}
capitals_with_positions = [(province, capital_cities[province], [
                            0, 0]) for province in province]

# 软件工程专业
c = (
    Map(init_opts=opts.InitOpts(width="1600px", height="900px"))  # 可切换主题
    .set_global_opts(
        title_opts=opts.TitleOpts(title="二手车销售数量在全国的分布"),
        visualmap_opts=opts.VisualMapOpts(
            min_=0,
            max_=4000,
            range_text=['二手车数量区间：', ''],  # 分区间
            is_piecewise=True,  # 定义图例为分段型，默认为连续的图例
            pos_top="middle",  # 分段位置
            pos_left="left",
            orient="vertical",
            split_number=8,  # 分成8个区间
        )

    )
    .add("二手车数量", province_list, maptype="china")
    .render("二手车分布.html")
)

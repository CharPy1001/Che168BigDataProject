# Editor:CharPy
# Edit time:2024/6/7 1:35

import pandas as pd

# 导入
bigFrame = pd.read_csv("Req/Avl/che168.csv") # 请将合并完成后的.csv数据集更名为che168.csv并置于Req/Avl文件夹下
bigLen = len(bigFrame)
# print(bigFrame.columns)
# for col in bigFrame.columns:
# 	print("{0}: {1}".format(col, type(bigFrame[col][0])))
'''修改为'''
bigFrame.columns = ['CID', 'Engine_type', 'Brand', 'Model', 'Class', 'Wheelbase', 'Price', 'Discount',
					'Location', 'Color', 'Indicated_mileage', 'Year', 'Registration_time', 'Warranty',
					'Cylinders_num', 'Intake_form', 'Max_power', 'Max_torque', 'Fuel_displacement',
					'Fuel_volume', 'Fuel_type', 'Emission_standard', 'Motor_type', 'Motor_location',
					'Motor_power', 'Motor_torque', 'Battery_type', 'Battery_capacity', 'Fast_charging',
					'Battery_warranty', 'Gearbox_num', 'Gearbox_type', 'Drive_mode', 'Car_box_structure',
					'Front_suspension_type', 'Rear_suspension_type']

'''------------------添加FrameID并插入到第一列----------------'''
frameID = [j for j in range(bigLen)]
bigFrame.insert(0, 'FrameID', frameID)

'''-------------------------CID----------------------------'''
bigFrame["CID"] = bigFrame["CID"].fillna(40400404).astype(int)

'''------------------常规str类型填充-----------------------'''
simple2str = ["Engine_type", "Brand", "Model",
			  "Class", "Location", "Color",
			  "Registration_time", "Warranty",
			  "Intake_form", "Fuel_type", "Emission_standard",
			  "Motor_type", "Motor_location",
			  "Battery_type", "Fast_charging", "Battery_warranty",
			  "Gearbox_type", "Drive_mode", "Car_box_structure",
			  "Front_suspension_type", "Rear_suspension_type"]
for item in simple2str:
	bigFrame[item] = bigFrame[item].fillna('-').astype(str)

'''----------------float转int，填充+转换-------------------'''
bigFrame["Price"] = bigFrame["Price"].fillna(-1).astype(float) # 报价
bigFrame["Discount"] = bigFrame["Discount"].fillna(-1).astype(float) # 比新车便宜

'''------------str转数字，填充-1，抹后缀，转换---------------'''
# 表显里程后缀特殊，转出类型也特殊，单独处理
bigFrame["Indicated_mileage"] = bigFrame["Indicated_mileage"].fillna(-1).replace('-', -1)
for i in range(bigLen):
	if bigFrame.loc[i, "Indicated_mileage"] != -1:
		bigFrame.loc[i, "Indicated_mileage"] = bigFrame.loc[i, "Indicated_mileage"].replace("万公里", "")
bigFrame["Indicated_mileage"] = bigFrame["Indicated_mileage"].astype(float)
# 其他均为str转int，批量处理
str2num = ["Wheelbase", "Year", "Cylinders_num",
		   "Max_power", "Max_torque",
		   "Fuel_displacement", "Fuel_volume",
		   "Motor_power", "Motor_torque", "Battery_capacity"]
for item in str2num:
	bigFrame[item] = bigFrame[item].fillna(-1).replace('-', -1).astype(str)  # 轴距
for i in range(bigLen):
	for item in str2num:
		if bigFrame.loc[i, item] != -1:
			bigFrame.loc[i, item] = bigFrame.loc[i, item].replace(".0", "")
for item in str2num:
	print("processing", item)
	bigFrame[item] = bigFrame[item].astype(float).astype(int)

'''------------------变速箱档位数特殊处理-----------------------'''
bigFrame["Gearbox_num"] = bigFrame["Gearbox_num"].replace('无级变速', 0).astype(str)
for i in range(bigLen):
	bigFrame.loc[i, "Gearbox_num"] = bigFrame.loc[i, "Gearbox_num"].replace(".0", "")

bigFrame.to_csv("Req/Avl/che168EngDone.csv", index=False)

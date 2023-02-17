import pandas as pd
import geopandas as gpd
import transbigdata as tbd
# tbd或geopandas使用报错，请按顺序去pythonlib源使用whl重装fiona、gdal、pyproj、numpy+MKL、scipy等

# 轨迹数据格式：
# 0,4739e016-5a88-4dd6-8dee-cf8dd5760d32,1640168896000,114.0719871043955,22.614763418999843,118.10820573921076,203.17534,2.2807097,0
# 'pid', 'tripID', 'time', 'longitude', 'latitude', 'altitude', 'bearing', 'horizontalAccM', 'activityIdType'

# 读取CSV文件
cnt = 30000
df = pd.DataFrame()
# 定义全体数据的存储
df_all = pd.DataFrame()

print('start read file...')

# 循环读取文件
for i in range(30000, 31233):
    # 读取文件
    try:
        # 见轨迹数据traj_YBDE_rep\trip_xxx.txt
        df = pd.read_csv('traj_process\\traj_YBDE_rep\\trip_' + str(i) +'.txt', header=None)

        # 为DataFrame添加列名
        df.columns = ['pid', 'tripID', 'time', 'longitude', 'latitude', 'altitude', 'bearing', 'horizontalAccM', 'activityIdType']

        # 将时间戳转换为datetime类型
        df['time'] = pd.to_datetime(df['time'])

        # 每次读取的数据添加到DataFrame中
        # df_all = df_all.append(df)
        # append函数废弃，使用concat函数
        df_all = pd.concat([df_all, df], axis=0)

        # 打印前几行数据
        # print(df.head())

    except:
        # 如果文件打开失败，打印错误信息，退出循环
        # print("open file " + "traj_YBDE_rep\\trip_"+str(i)+".txt" + " error!")
        continue

    # 打印读取的数据的数量
    # print("read file " + "traj_YBDE_rep\\trip_"+str(i)+".txt" + " success!")
    cnt += 1


# TODO
print(df_all.head())
print(df_all.__len__())

# 使用transbigdata库中的函数，基于keplergl将DataFrame的轨迹数据绘制成地图可视化 可见jupyter notebook
# 问题在于显示精度不够，太大了，需要缩小
# tbd.visualization_data(df, col=['longitude', 'latitude'])
# tbd.visualization_trip(df, col = ['longitude', 'latitude', 'tripID', 'time'])

import folium

# 使用folium对轨迹数据进行可视化
points = df_all[['latitude', 'longitude']].values.tolist() # 注意经纬度顺序
# print(points)
m = folium.Map(location=[df_all['latitude'].mean(), df_all['longitude'].mean()], zoom_start=20)
# folium.PolyLine(points, color="red", weight=1.5, opacity=0.8).add_to(m)

# 把df_all中的数据按照tripID分组
grouped = df_all.groupby('tripID')

# 每个分组都绘制一条轨迹
for name, group in grouped:
    points = group[['latitude', 'longitude']].values.tolist()
    folium.PolyLine(points, color="red", weight=1.5, opacity=0.8).add_to(m)


# 保存地图
m.save('traj_process\\traj.html')

print('save traj map end')
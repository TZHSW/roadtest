from random import randint
import numpy as np
import pandas as pd
import geopandas as gpd
import transbigdata as tbd
# tbd或geopandas使用报错，请按顺序去pythonlib源使用whl重装fiona、gdal、pyproj、numpy+MKL、scipy等；使用pycharm
# 在系统设置中添加该虚拟环境的环境3项变量 + 使用cmd作为终端而非windows powershell等
import matplotlib.pyplot as plt
import folium
import cv2

# 轨迹数据格式：
# 0,4739e016-5a88-4dd6-8dee-cf8dd5760d32,1640168896000,114.0719871043955,22.614763418999843,118.10820573921076,203.17534,2.2807097,0
# 'pid', 'tripID', 'time', 'longitude', 'latitude', 'altitude', 'bearing', 'horizontalAccM', 'activityIdType'

# 注意vscode和pycharm相对路径不同，vscode默认是相对于当前文件夹，pycharm是相对于项目根目录：traj_process\\，可修改设置

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
        df = pd.read_csv('traj_YBDE_rep\\trip_' + str(i) +'.txt', header=None)

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

# 查看对应各高度出现的次数，作为后续的颜色映射，这里对高度只取整数
df_all['altitude-int'] = df_all['altitude'].astype(int)
print(df_all['altitude-int'].value_counts())

# 根据直方图的数据，生成颜色映射，映射规则按照高度从低到高分别映射到红、黄、绿三种颜色
color_map = folium.LinearColormap(['red', 'yellow', 'green'], vmin=df_all['altitude'].min(), vmax=df_all['altitude'].max())
# 根据颜色映射，给每条轨迹添加颜色
color_map.add_to(m)

# 把df_all中的数据按照tripID分组
grouped = df_all.groupby('tripID')

# 每个分组都绘制一条轨迹（按照原始映射）
for name, group in grouped:
    points = group[['latitude', 'longitude']].values.tolist()
    # 为每条轨迹添加颜色，添加规则是轨迹的平均高度对应上面颜色表中的颜色
    colordif = color_map(group['altitude'].mean())
    folium.PolyLine(points, color=colordif, weight=1.5, opacity=0.6).add_to(m)


# 保存地图
m.save('traj.html')

print('save traj map end')


# //////////////////////////////////////////////////////////////////////


# TODO 这里可以考虑按算法进行高度频率区分，从而计算出立交桥层次关系。
# 自适应阈值分割？自动多阈值分割算法？聚类分析？3

# 生成直方图
hist, bin_edges = np.histogram(df_all['altitude-int'], bins=100)
# 可视化直方图查看分布情况
plt.hist(df_all['altitude-int'], bins=100)

# 对生成的直方图进行聚类分析，这里使用KMeans：

m_cluster = folium.Map(location=[df_all['latitude'].mean(), df_all['longitude'].mean()], zoom_start=20)

# 增加tif图层，可以在下方显示图层
img = cv2.imread("tif\\yabao_wgs.tif")
# vscode中报错raster_layers，但是可以正常运行
layers = folium.raster_layers.ImageOverlay(img,[[22.608424646,114.066964664],[22.616127950,114.074399748]])
m_cluster.add_child(layers)


# 1. 生成聚类模型
# from sklearn.cluster import KMeans

# cluster_num = 3 # 预训练聚类数量
# colors=['red', 'yellow', 'green'] #['#00ae53', '#86dc76', '#daf8aa', '#ffe6a4', '#ff9a61', '#ee0028']

# kmeans = KMeans(n_clusters=cluster_num, random_state=0).fit(hist.reshape(-1, 1))

# 聚类阈值存入列表
# cluster_threshold = []
# for i in range(0, len(kmeans.cluster_centers_)):
#     cluster_threshold.append(kmeans.cluster_centers_[i][0])
# cluster_threshold.sort()
# print(cluster_threshold)

# 2. 生成聚类结果
# cluster_result = kmeans.predict(hist.reshape(-1, 1))

# 按照聚类阈值，生成颜色映射color_map_cluster
# import branca.colormap as cm
# color_map_cluster = cm.StepColormap(colors, vmin=df_all['altitude'].min(), vmax=df_all['altitude'].max(), index=cluster_threshold)
# color_map_cluster.add_to(m_cluster)

# 引入DBSCAN聚类算法
from sklearn.cluster import DBSCAN

# 参数意义：eps：两个样本被看作邻居的最大距离；min_samples：一个样本被看作核心样本所需要的最小邻居数目
dbscan = DBSCAN(eps=0.5, min_samples=5).fit(hist.reshape(-1, 1))

# 聚类阈值存入列表
cluster_threshold = []
for i in range(0, len(dbscan.core_sample_indices_)):
    cluster_threshold.append(hist[dbscan.core_sample_indices_[i]])
cluster_threshold.sort()
print(cluster_threshold)

# 生成聚类结果
cluster_result = dbscan.labels_

# 获取聚类数量
cluster_num = len(set(cluster_result)) - (1 if -1 in cluster_result else 0)

# 3. 生成聚类结果的直方图
plt.hist(cluster_result, bins=cluster_num)
# plt展示hist直方图
plt.show()

# 按照聚类数量生成对应的颜色列表
colors = []
for i in range(0, cluster_num):
    # 生成随机颜色
    colors.append('#%06X' % randint(0, 0xFFFFFF))

# 生成
color_map_cluster = folium.LinearColormap(colors, vmin=df_all['altitude'].min(), vmax=df_all['altitude'].max())

color_map_cluster.add_to(m_cluster)

# 每个分组都绘制一条轨迹（按照聚类映射）

for name, group in grouped:
    points = group[['latitude', 'longitude']].values.tolist()
    # 为每条轨迹添加颜色，添加规则是轨迹的平均高度对应上面颜色表中的颜色
    colordif = color_map_cluster(group['altitude'].mean())
    folium.PolyLine(points, color=colordif, weight=1.5, opacity=0.6).add_to(m_cluster)

m_cluster.save('traj_cluster.html')

print('save traj cluster map + tiff end')
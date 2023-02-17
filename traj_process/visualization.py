# paddle_env 环境下运行
# 导入plt模块
import matplotlib.pyplot as plt

point_list=[]
output_point_list=[]

# 读入
# 遍历traj_YBDE文件夹内的所有轨迹数据文件
cnt = 30000 # 0-31232
# 遍历读取文件夹中的数据
for i in range(30000, 31233):
    # 读取文件
    try:
        # 见轨迹数据traj_YBDE_rep\trip_xxx.txt
        fd = open(r"traj_YBDE_rep\\trip_"+str(i)+".txt",'r')

        # 遍历文件中的每一行
        for line in fd:
            # 去除空格
            line=line.strip()
            # 读取每一行的id,longitude,latitude,altitude
            id=int(line.split(",")[0])
            longitude=float(line.split(",")[3])
            latitude=float(line.split(",")[4])
            altitude=float(line.split(",")[5])
            # 将读取的数据添加到point_list中
            point_list.append((id,longitude,latitude,altitude))
        # 关闭文件
        fd.close()
        # 将point_list中的数据添加到output_point_list中
        output_point_list.append(point_list)
        # 清空point_list
        point_list = []

    except:
        # 如果文件打开失败，打印错误信息，退出循环
        print("open file " + "traj_YBDE_rep\\trip_"+str(i)+".txt" + " error!")
        continue

    # 打印读取的数据的数量
    print(cnt)
    cnt += 1   

# 可视化
# point_list与output_point_list
trajectoryData=[[],[]]
for point in output_point_list[:]:
    trajectoryData[0].append(point[1])
    trajectoryData[1].append(point[2])

plt.plot(trajectoryData[0],trajectoryData[1],"g")
plt.xlabel("longitude")
plt.ylabel("latitude")
plt.title("trajectoryData-traj_YBDE_rep-30000-31232")
plt.show()

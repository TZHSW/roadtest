import transbigdata as tbd
import pandas as pd
import geopandas as gpd

#读取出租车GPS数据 
data = pd.read_csv('traj_YBDE_rep\\trip_30000.txt',header = None) 
data.columns = ['VehicleNum','time','lon','lat','OpenStatus','Speed'] 

#定义研究范围
bounds = [113.75, 22.4, 114.62, 22.86]
#剔除研究范围外的数据
data = tbd.clean_outofbounds(data,bounds = bounds,col = ['lon','lat'])

#获取栅格化参数
params = tbd.area_to_params(bounds,accuracy = 1000)

#将GPS数据对应至栅格
data['LONCOL'],data['LATCOL'] = tbd.GPS_to_grids(data['lon'],data['lat'],params)

#聚合集计栅格内数据量
grid_agg = data.groupby(['LONCOL','LATCOL'])['VehicleNum'].count().reset_index()
#生成栅格的几何图形
grid_agg['geometry'] = tbd.gridid_to_polygon(grid_agg['LONCOL'],grid_agg['LATCOL'],params)
#转换为GeoDataFrame
grid_agg = gpd.GeoDataFrame(grid_agg)
#绘制栅格
grid_agg.plot(column = 'VehicleNum',cmap = 'autumn_r')
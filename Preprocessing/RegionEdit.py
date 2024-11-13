'''
根据xy点构成的多边形范围，直接修改bottom网格。
生成BOTTOM2.t3s后，将原BOTTOM.t3s文件名改为BOTTOM.bak，将新文件名改为BOTTOM.t3s。
在BlueKenue的SLF文件中，移除原有BOTTOM，导入新的BOTTOM.t3s，拖动新的BOTTOM2.t3s文件进入SLF中，然后保存。
'''


import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt


def ReadMesh(filename):
    # 读取网格文件，返回文件头，节点坐标和值，网格索引
    with open(filename, 'r') as file:
        lines = file.readlines()
    node_count_line = next(line for line in lines if line.startswith(":NodeCount"))  # 寻找NodeCount
    node_count = int(node_count_line.split()[1])  # 获取节点数
    end_header_index = next(i for i, line in enumerate(lines) if line.startswith(":EndHeader"))  # 寻找EndHeader
    header = lines[:end_header_index + 1]  # 文件头内容
    ender = lines[end_header_index + 1 + node_count:]  # 文件尾内容（三角网格索引）
    node_data = []
    for line in lines[end_header_index + 1:end_header_index + 1 + node_count]:
        data = list(map(float, line.split()))
        node_data.append(data)  # 提取节点坐标和值
    node_data = pd.DataFrame(node_data, columns=['longitude', 'latitude', 'height'])
    return header, node_data, ender


def Defineregion(filename):
    # 定义区域
    region_xyz = pd.read_csv(filename, sep=' ', header=None, names=['longitude', 'latitude'])
    region_poly = Polygon(region_xyz)
    region_poly = gpd.GeoDataFrame([{'geometry': region_poly}], crs="EPSG:4326")  # 转换为GeoDataFrame，EPSG:4326为WGS84坐标系
    return region_poly


# 主程序
header, node_data, ender = ReadMesh("BOTTOM.t3s")  # 读取网格文件
geometry = gpd.GeoSeries.from_xy(node_data['longitude'], node_data['latitude'])
node_data_gdf = gpd.GeoDataFrame(node_data, geometry=geometry, crs="EPSG:4326")  # 转换为GeoDataFrame

# 第一个区域
region_area = Defineregion("input-region.xyz")  # 获取区域位置
in_region = node_data_gdf.geometry.within(region_area.unary_union)  # 获取该区域内的节点
node_data_gdf.loc[in_region, 'height'] = 10    # 区域赋值


# 输出新的网格文件
point_str = node_data_gdf.apply(lambda row: f"{row['longitude']} {row['latitude']} {row['height']}\n", axis=1).tolist()  # 格式化
header.extend(point_str)
header.extend(ender)  # 合并文件头、节点坐标和网格索引
with open('BOTTOM2.t3s', 'w') as new_file:
    new_file.writelines(header)
print('输出BOTTOM2.t3s')

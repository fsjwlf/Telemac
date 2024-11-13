'''
根据xy点构成的堤坝线和堤坝高度，直接修改bottom网格。
生成BOTTOM2.t3s后，将原BOTTOM.t3s文件名改为BOTTOM.bak，将新文件名改为BOTTOM.t3s。
在BlueKenue的SLF文件中，移除原有BOTTOM，导入新的BOTTOM.t3s，拖动新的BOTTOM2.t3s文件进入SLF中，然后保存。
'''


import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString


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


def DefineDike(filename, width):
    dike_xyz = pd.read_csv(filename, sep=' ', header=None, names=['longitude', 'latitude'])
    dike_line = LineString(dike_xyz)
    dike_line = gpd.GeoDataFrame([{'geometry': dike_line}], crs="EPSG:4326")  # EPSG:4326为WGS84坐标系，根据需要调整
    dike_area = dike_line.buffer(width)  # 创建缓冲区
    return dike_area


# 主程序
header, node_data, ender = ReadMesh("BOTTOM.t3s")  # 读取网格文件
geometry = gpd.GeoSeries.from_xy(node_data['longitude'], node_data['latitude'])
node_data_gdf = gpd.GeoDataFrame(node_data, geometry=geometry, crs="EPSG:4326")  # 转换为GeoDataFrame

# 第一个堤坝
dike_area = DefineDike("input-dike.xyz", 0.0008)  # 获取堤坝位置
in_dike_area = node_data_gdf.geometry.within(dike_area.unary_union)
node_data_gdf.loc[in_dike_area, 'height'] +=  10  # 堤坝高度

# 第二个堤坝
dike_area = DefineDike("input-dike2.xyz", 0.0008)  # 获取堤坝位置
in_dike_area = node_data_gdf.geometry.within(dike_area.unary_union)
node_data_gdf.loc[in_dike_area, 'height'] +=  10  # 堤坝高度

# 输出新的网格文件
point_str = node_data_gdf.apply(lambda row: f"{row['longitude']} {row['latitude']} {row['height']}\n", axis=1).tolist()  # 格式化
header.extend(point_str)
header.extend(ender)  # 合并文件头、节点坐标和网格索引
with open('BOTTOM2.t3s', 'w') as new_file:
    new_file.writelines(header)
print('输出BOTTOM2.t3s')

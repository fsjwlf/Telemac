# 提取点数据：
```python
import matplotlib.pyplot as plt
import sys
sys.path.append("D:/Program/Telemac/scripts/python3")
from data_manip.extraction.telemac_file import TelemacFile
from postel.plot1d import plot1d

res = TelemacFile('result.slf')
times = res.times  # 获取时间序列
points = [[121.153, 43.531], [121.152, 43.532]]  # 观测点
data = res.get_timeseries_on_points('WATER DEPTH', points)  # 获取观测点特定变量的时间变化过程

fig, ax = plt.subplots(figsize=(10,5))
for i, point in enumerate(points):
    plot1d(ax, times, data[i,:], plot_label='point {}'.format(point))
ax.set(xlabel='time (s)', ylabel='WATER DEPTH (m)')
ax.legend()
plt.savefig('a.png')
```

# 输出三角网格数据
```python
import numpy as np
import sys
sys.path.append("D:/Program/Telemac/scripts/python3")  # Telemac 安装路径
from data_manip.extraction.telemac_file import TelemacFile
from postel.plot2d import *
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon, Point

def LoadData(filename):
    # 加载slf文件
    res = TelemacFile(filename)
    res.print_info()
    return res

def ExportShp(res, epsg=4326):
    # 将节点以及三角网格，分别保存为shp点和shp线
    mesh = res.tri
    x, y, triangles = mesh.x, mesh.y, mesh.triangles
    polygons = [Polygon([(x[tri], y[tri]) for tri in triangle]) for triangle in triangles]
    gdf = gpd.GeoDataFrame(geometry=polygons)
    gdf.set_crs(epsg, inplace=True)
    gdf.to_file("triangulation.shp")
    points = [Point(xy) for xy in zip(x, y)]
    gdf = gpd.GeoDataFrame(geometry=points)
    gdf.set_crs(epsg, inplace=True)
    gdf.to_file("points.shp")

def ExportPointData(res, varname, filename):
    # 读取三角顶点的varname在所有timestep的数据
    # 将x, y, var数据保存为npz文件
    # 读取npz文件 data = np.load('data.npz')['var']
    mesh = res.tri
    x, y, triangles = mesh.x, mesh.y, mesh.triangles
    var = []
    for timeframe in range(res.ntimestep):
        varvalue = res.get_data_value(varname, timeframe)  # 每个节点的数据，一维数组
        var.append(varvalue)
    np.savez_compressed(filename, x=x, y=y, var=np.array(var))
    

def ExportPointDataT(res, varname, time, filename):
    # 读取三角顶点的varname在指定timestep的数据
    # 将顶点个数，以及index, x, y, var数据保存为txt文件
    mesh = res.tri
    x, y, triangles = mesh.x, mesh.y, mesh.triangles
    varvalue = res.get_data_value(varname, time)
    with open(filename, 'w') as f:
        print(f'{len(x)}', file=f)
        for i in range(len(x)):
            print(f'{i}\t{x[i]}\t{y[i]}\t{varvalue[i]}', file=f)


def ExportMeshDataT(res, varname, time, filename):
    # 读取三角顶点的varname在指定timestep的数据
    # 取三个顶点的均值作为三角面数据
    # 将三角顶点坐标，三角网格顶点索引，三角面数据保存为txt文件
    mesh = res.tri
    x, y, triangles = mesh.x, mesh.y, mesh.triangles
    pointvalue = res.get_data_value(varname, time)
    meshvalue = []
    # 输出顶点坐标
    f = open(filename, 'w')
    print(f'{len(x)}', file=f)
    for i in range(len(x)):
        print(f'{i}\t{x[i]}\t{y[i]}', file=f)
    # 输出三角网格顶点索引，并计算网格均值
    print(f'{len(triangles)}', file=f)
    for i in range(len(triangles)):
        print(f'{i}\t{triangles[i][0]}\t{triangles[i][1]}\t{triangles[i][2]}', file=f)
        p1, p2, p3 = pointvalue[triangles[i][0]], pointvalue[triangles[i][1]], pointvalue[triangles[i][2]]
        data = np.average([p1, p2, p3])
        meshvalue.append(data)
    meshvalue = np.array(meshvalue)
    # 输出网格值
    print(f'{len(meshvalue)}', file=f)
    for i in range(len(meshvalue)):
        print(f'{i}\t{meshvalue[i]}', file=f)
    f.close()
    # 画图
    plt.tripcolor(mesh, meshvalue)
    plt.show()

res = LoadData('in-geo.slf')
ExportShp(res, epsg=4326)
ExportPointData(res, 'BOTTOM', filename='bottom.npz')
ExportPointDataT(res, 'BOTTOM', time=0, filename='bottomp.txt')
ExportMeshDataT(res, 'BOTTOM', time=0, filename='bottomm.txt')
```

# 输出矩形网格数据
```python
import numpy as np
import sys
sys.path.append("D:/Program/Telemac/scripts/python3")
from data_manip.extraction.telemac_file import TelemacFile
from data_manip.formats.regular_grid import interpolate_on_grid
import matplotlib.pyplot as plt


def LoadData(filename):
    # 加载数据
    data = TelemacFile(filename)  # 加载文件
    data.print_info()  # 输出模型基本信息
    return data

def Regular(data, var_name, frame, resolution):
    # 三角网插值规则网
    var_value = data.get_data_value(var_name, frame)  # 获取变量数据
    grid = np.meshgrid(np.arange(np.min(data.meshx), np.max(data.meshx), resolution), np.arange(np.min(data.meshy), np.max(data.meshy), resolution))  # 生成规则网格
    var_regular, grid = interpolate_on_grid(data.tri, var_value, grid)  # 线性插值
    return var_regular, grid

def Draw(var_regular, grid):
    # 绘图
    fig, ax = plt.subplots(1, 1, figsize=(20, 5))
    c = ax.pcolormesh(grid[0], grid[1], var_regular, vmin=0, vmax=1, shading='auto')
    fig.colorbar(c, ax=ax)
    plt.savefig('result.png')

def ExportASC(data, filename, var_regular, resolution, nodata_value=-999):
    # 转GIS-ASC
    var_regular_asc = np.flipud(var_regular)  # 低纬度由第一行放到最后一行
    var_regular_asc = var_regular_asc.filled(nodata_value)  # 填充nan值
    header = f"NCOLS {var_regular.shape[1]}\nNROWS {var_regular.shape[0]}\nXLLCORNER {np.min(data.meshx)}\nYLLCORNER {np.min(data.meshy)}\nCELLSIZE {resolution}\nNODATA_VALUE {nodata_value}"  # 生成文件头
    np.savetxt(filename, var_regular_asc, fmt='%.2f', encoding='utf-8', header=header, comments='')  # 保存文件

def ExportNPZ(data, filename, resolution, var_name):
    # 输出npz
    var = []
    grid = np.meshgrid(np.arange(np.min(data.meshx), np.max(data.meshx), resolution), np.arange(np.min(data.meshy), np.max(data.meshy), resolution))  # 规则网格
    for frame in range(data.ntimestep):  # 逐帧
        var_value = data.get_data_value(var_name, frame)  # 获取变量数据
        var_regular, _ = interpolate_on_grid(data.tri, var_value, grid)  # 线性插值
        var.append(var_regular)
    var = np.array(var)
    np.savez_compressed(filename, var)

if __name__ == '__main__':
    data = LoadData('result.slf')
    var_regular, grid = Regular(data, var_name='WATER DEPTH', frame=15, resolution=0.0005)
    Draw(var_regular, grid)
    ExportASC(data, filename='depth.asc', var_regular=var_regular, resolution=0.0005, nodata_value=-999)
    ExportNPZ(data, filename='Teleresult.npz', resolution=0.0005, var_name='WATER DEPTH')
```

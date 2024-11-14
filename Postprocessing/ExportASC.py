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

def ExportASC(data, filename, var_regular, resolution, nodata_value=-999):
    # 转GIS-ASC
    var_regular_asc = np.flipud(var_regular)  # 低纬度由第一行放到最后一行
    var_regular_asc = var_regular_asc.filled(nodata_value)  # 填充nan值
    header = f"NCOLS {var_regular.shape[1]}\nNROWS {var_regular.shape[0]}\nXLLCORNER {np.min(data.meshx)}\nYLLCORNER {np.min(data.meshy)}\nCELLSIZE {resolution}\nNODATA_VALUE {nodata_value}"  # 生成文件头
    np.savetxt(filename, var_regular_asc, fmt='%.2f', encoding='utf-8', header=header, comments='')  # 保存文件

if __name__ == '__main__':
    data = LoadData('out-result.slf')
    var_regular, grid = Regular(data, var_name='WATER DEPTH', frame=15, resolution=0.0005)
    ExportASC(data, filename='depth.asc', var_regular=var_regular, resolution=0.0005, nodata_value=-999)

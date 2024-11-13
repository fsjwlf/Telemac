'''
计算断面流量
Telemac模型需要输出I, J
注意，断面两端尽可能接近河道
'''
import sys
sys.path.append("D:/Program/Telemac/scripts/python3")  # 根据Telemac安装位置调整
from data_manip.extraction.telemac_file import TelemacFile
import numpy as np

def CartesianDischarge(filename, xy, timesteps):
    # 投影坐标系（米）
    res = TelemacFile(filename)
    x1, y1, x2, y2 = xy  # 断面端点坐标
    vx, vy = x2-x1, y2-y1
    poly_points, poly_number = [[x1, y1], [x2, y2]], [200]  # 断面分为200份
    poly_coord, abs_curv,u = res.get_timeseries_on_polyline('FLOWRATE ALONG X', poly_points, poly_number)
    poly_coord, abs_curv,v = res.get_timeseries_on_polyline('FLOWRATE ALONG Y', poly_points, poly_number)
    u[np.abs(u)<0.01] = 0
    v[np.abs(v)<0.01] = 0
    d = (-u*vy+v*vx) / ((vx**2+vy**2)**0.5)
    l = ((vx/poly_number[0])**2 + (vy/poly_number[0])**2)**0.5
    for time in range(timesteps):
        print(time, np.sum(d[:,time])*l)
        
def GeographicDischarge(filename, xy, timesteps):
    # 地理坐标系（经纬度）
    res = TelemacFile(filename)
    x1, y1, x2, y2 = xy
    vx, vy = (x2-x1)*100000*np.cos(y2/180*np.pi), (y2-y1)*100000
    poly_points, poly_number = [[x1, y1], [x2, y2]], [200]
    poly_coord, abs_curv,u = res.get_timeseries_on_polyline('FLOWRATE ALONG X', poly_points, poly_number)
    poly_coord, abs_curv,v = res.get_timeseries_on_polyline('FLOWRATE ALONG Y', poly_points, poly_number)
    u[np.abs(u)<0.01] = 0
    v[np.abs(v)<0.01] = 0
    d = (-u*vy+v*vx) / ((vx**2+vy**2)**0.5)
    l = ((vx/poly_number[0])**2 + (vy/poly_number[0])**2)**0.5
    for time in range(timesteps):
        print(time, np.sum(d[:,time])*l)


CartesianDischarge('result.slf', [100, 20, 100, 30], 100)

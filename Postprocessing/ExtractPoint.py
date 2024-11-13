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

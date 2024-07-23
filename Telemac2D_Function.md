## 经纬度坐标
当模拟范围比较大时（大江大河、近海），模型可以采用经纬度坐标系。
在CAS中添加以下关键词：
```
SPHERICAL COORDINATES = YES
SPATIAL PROJECTION TYPE = 3
```

## 变时间步长
Telemac2d支持变时间步长，提高模型的稳定性，同时提高模型计算效率。（此时模拟时长要用DURATION而不能用NUMBER OF TIME STEPS）
```
VARIABLE TIME-STEP = YES
DESIRED COURANT NUMBER = 0.9
```

## 点源流量
如果入流只在一两个网格的范围，或者流量边界很容易崩溃，可以尝试把流量边界，改为某一个或某几个点的点源流量，例如
```
GLOBAL NUMBERS OF SOURCE NODES = 10; 20
WATER DISCHARGE OF SOURCES = 0; 0
SOURCES FILE = sourcefile.txt
TYPE OF SOURCES = 2
```

sourcefile.txt 里面的Q，从1开始编号，与边界无关

## 降水蒸发
采用下面的关键词，正值降水，负值蒸发。
```
RAIN OR EVAPORATION = YES
RAIN OR EVAPORATION IN MM PER DAY = 10
```

## 水位流量关系边界
出口边界设置为水位流量关系的方法，参考手册 4.2.6 Stage-discharge curves

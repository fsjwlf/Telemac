# 边界条件：
1. 绘制模型边界时，应该先仔细观察一下地形数据，上边界和下边界附近的地形如何，别盲目地在地形数据最外侧画边界，等到跑模型时才发现边界处有一个坝，直接挡住了水流。
2. 边界条件，尽量超过5个网格，否则模型很容易崩溃
3. 下游边界，不要用4 4 4。有时候我们不知道出口的流量、水位、甚至水位流量关系，于是有些人就尝试把边界设置为4 4 4，即水位流量都是自由的。这种设置有时候会有合理的结果，但大部分情况下模型都会一团糟，水位流量会变得异常。强烈不建议用444。如果真的没有数据，可以尝试给下游设置一个恒定的水位边界，水位就取长时间平均值即可。

# 初始条件：
1. 初始条件设置'CONSTANT DEPTH'，是给所有网格赋予了水深，因此模型运行时需要预留一个预热期，让两岸的水流到河流中，让上游的水流到下游，让河道里的水位趋于正常，让水流具有流速。
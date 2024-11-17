![](https://cdn.nlark.com/yuque/0/2024/png/35942365/1731630575605-aa5e8cba-714d-4322-82fd-c811187d3d93.png)

# Telemac-Mascaret 介绍
Telemac2D 二维水动力学模型，是Telemac-Mascaret水利模型套装的一部分。

Telemac-Mascaret模型最初由法国电力集团（EDF）的法国国立水利与环境实验室开发，2010年模型开源。模型包括1、2、3维水动力学模型、水质污染物扩散模型、波浪模型、泥沙模型等。可以应用于洪水模拟、湖库水动力水质模拟、近海模拟等。

# 模型特点
## Telemac2D优点
1. **开源免费模型**  
Telemac2D模型源代码可公开获取。可以在Windows和Linux系统，Intel处理器和国产处理器上编译，降低断供风险。但网站偶尔不稳定。
2. **支持CPU并行计算**  
利用现代多核处理器和计算集群的并行计算能力，大幅提升了模拟的速度和效率
3. **支持Python、Fortran二次开发**  
首先，Telemac2D模型本身由Fortran编写，既可以直接改源代码，也可以在建模时插入简单的Fortran代码块；  
其次，官方为模型提供了强大的、基于Python的框架，前处理、模型执行、模型后处理均有大量Python脚本支撑
4. **对接系统**  
基于上述两点原因，Telemac2D模型很适合用于系统开发，通过Python语言与前端结合。
5. **工业支撑，历史悠久**  
Telemac2D模型由法国电力集团（EDF）的法国国立水利与环境实验室开发，有几十年的工业应用积累。
6. **官方提供大量案例**  
模型安装后，在安装文件夹内有大量应用案例（example），还有实用python脚本（notebooks）。‘
7. **应用广泛**  
Telemac套装除了2D水动力，还包括1D水动力（MASCARET）、3D水动力模型、波浪模型、泥沙模型、水质模型……

![](https://cdn.nlark.com/yuque/0/2024/png/35942365/1731630490898-c5c9fa58-ce03-4686-89a6-44b72164ebea.png)

## Telemac2D缺点
1. **开源时间较短，模型存在bug**  
查看官网源代码的更新日志，能看到模型依然存在一些bug
2. **不支持GPU并行计算**。
3. **教程较少，官方用户手册不够详细，论文较少**。

# 应用场景
| 溃坝分析 | 防洪减灾 | 港口海岸 |
| :---: | :---: | :---: |
| ![](https://cdn.nlark.com/yuque/0/2024/png/35942365/1731653794753-3f50d438-f2c3-4b9b-8385-8debf9b07140.png) | ![](https://cdn.nlark.com/yuque/0/2024/png/35942365/1731653921441-a20175bb-3412-4604-80af-c357405b7cb0.png) | ![](https://cdn.nlark.com/yuque/0/2024/png/35942365/1731653874384-6e2cfe1c-3f16-4160-9f75-3fb82e98dffd.png) |
| 潮流分析 | 水质分析 | 泥沙输运 |
| ![](https://cdn.nlark.com/yuque/0/2024/png/35942365/1731653996460-a8b558d4-95ed-4cfb-8abf-e0dc5009bb88.png) | ![](https://cdn.nlark.com/yuque/0/2024/png/35942365/1731654028504-043bdee6-16a0-433c-b196-cfe16d80a80f.png) | ![](https://cdn.nlark.com/yuque/0/2024/png/35942365/1731654049482-4870d6af-fbd4-49d6-b7e6-5207b8149c15.png) |


# 学习资源
1. [Hydro-Informatics](https://hydro-informatics.com/numerics/telemac/telemac.html)
2. [官方论坛](https://www.opentelemac.org/index.php/kunena/index)（可能会有回复）


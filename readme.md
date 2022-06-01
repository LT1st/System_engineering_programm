# == 本项目用于2022春季学期课程设计 ==

- 算法实现语言：*python*
- 写作：LaTex
- 论文编译器：overleaf
- 思维导图笔记：Xmind
- 文献管理：Zeotero

# BUG

- [x]  i=j时候计算距离应该是 inf 需要定义一个很大值
- [ ]  加入直接可视化 networkx
- [ ]  ATSP转换TSP后，需要内部状态改变
# 代码说明
- 算法设计阶段使用了jupyter notenook，请开启服务后打开文件。同时也提供线上运行环境，论文中会给出colab连接。
- 工程化实现使用python类和包结构
- 🚀 所有代码存放在 code 文件夹下
## dataloader 
### Dataloader_for_TSP(ATSP)_datasets 好用的数据集的加载器
- 提供了用于TSP数据集的加载器*TSP_DATA*，能适用于大多数TSP测试样例。  
- 目前网络上代码仅能适用于固定长度的测试样例，非常原始。本项目中的TSP_DATA类能根据数据表头自动获取数据类型、计算方式等信息。  
- 可同时根据数据集变化，动态需求计算*邻接矩阵和邻接表*，保存在类内变量中
- 可自动访问网络，获取各测试样例当前最优值，比较算法精度
- 通过全局变量和修饰器获取数据加载、计算耗时
- 自动数据集下载脚本，运行既获取

### Visualization_for_TSP(ATSP)_datasets 提供了数据可视化
- 利用networkx库，解决了大多数TSP测试样例未提供坐标，无法可视化的问题
- 根据加载器类*TSP_DATA*返回可视化数据，数据接口无需调整

## collection_from_web 算法合集
- 存放网络上找到的TSP求解算法。由于时间有限，又想测试尽可能多的算法，因此使用了部分网络开源代码

## 🌟my_algorithm 算法合集
- 存放我写的算法代码
## TSP_dataloader_package 开源的py-pi库
### 使用方法
```bash
::在控制台输入安装
pip install -i https://test.pypi.org/simple/ TSP-dataloader
```

### 维护方法
0. 改版本号，维护setup.py
1. 打包
```bash
::在控制台输入
python setup.py sdist bdist_wheel
```
2. 上传到测试环境
```bash
::在控制台输入 当前文件夹路径与setpy.py一致
python3 -m twine upload --repository testpypi dist/*

::使用测试环境
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-pkg-YOUR-USERNAME #其中 example-pkg-YOUR-USERNAME 即自己指定的包名
```
3. 发布正式包
python -m twine upload --repository testpypi dist/* -u __token__  -p pypi-密码在qq收藏备份 --verbose


# 其他文件夹
- 记录课程的开题、中期、答辩。使用$Latex$编写。
- 存放数据集
- 记录加载报错的测试样例（主要是由于维度过高，内存溢出）

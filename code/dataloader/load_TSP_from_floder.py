import glob
import pandas as pd



file_tsp = []
# 获取tsp数据
for filename in glob.glob(r'D:\0latex\System_engineering_programm\TSP_tst_data\*.tsp.gz'):
    file_tsp.append(filename)
    
print(file_tsp)

file_atsp = []
# 获取atsp数据
for filename in glob.glob(r'D:\0latex\System_engineering_programm\TSP_tst_data\*.atsp.gz'):
    file_atsp.append(filename)
    
print(file_atsp)

data_tsp = [] # 【【名字，数据】，下一条，。。。。】
for tsp in file_tsp:
    df = pd.read_csv(tsp, sep=" ", skiprows=6, header=None)
    
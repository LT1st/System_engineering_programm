import sys
import os
import glob
sys.path.append('..')
from dataloader.Dataloader_for_TSP_datasets import TSP_DATA


def get_all_TSP_and_ATSP_in_floder(floder_path = r'D:\0latex\System_engineering_programm\TSP_tst_data'):
    """
    floder_path:
        windows系统路径
    return:
        file_tsp
            TSP的文件路径list
        file_atsp
            ATSP文家路径list
    """
    # 自动切换网上平台或者本地路径
    import platform
    check_sys = platform.system()
    if check_sys == 'Linux':   # colab address
        # 从GoogLe Drive获取数据集，更换本地，需要data使用本地路径
        from google.colab import drive
        drive.mount('/content/drive/')
        # GoogLe Drive 路径
        data_folder = 'drive/MyDrive/现代优化计算方法/'
    elif check_sys == 'Windows': # local address 
        # 本地路径
        data_folder = floder_path
    else:
        raise EnvironmentError

    # 文件路径拼接
    tsp_data_path = os.path.join(data_folder,'*.tsp.gz')
    atsp_data_path = os.path.join(data_folder,'*.atsp.gz')
    tsp_data_path

    # 获取目标文件夹下的测试样例
    file_tsp = []
    # 获取tsp数据
    for filename in glob.glob(tsp_data_path):
        file_tsp.append(filename)
        
    print(file_tsp)

    file_atsp = []
    # 获取atsp数据
    for filename in glob.glob(atsp_data_path):
        file_atsp.append(filename)
        
    print(file_atsp)

    return file_tsp,file_atsp



"""def get_all_TSP_and_ATSP_in_floder(floder_path = r'D:\0latex\System_engineering_programm\TSP_tst_data'):
    stp_ass = os.path.join(floder_path, )
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
    df = pd.read_csv(tsp, sep=" ", skiprows=6, header=None)"""
    
# -*- coding: utf-8 -*-
"""
Created on Tue May 31 11:32:51 2022

@author: lt
"""

import requests 
from bs4 import BeautifulSoup

def get_best_result_from_web(url = 'http://elib.zib.de/pub/mp-testdata/tsp/tsplib/stsp-sol.html'):
    resp = requests.get(url = url)
    html = resp.text
    soup = BeautifulSoup(html,"html.parser")
    try:
        title_url_Date=soup.find_all('li')
        #a=title_url_Date[0]
        best_res_dict={}
        for i in title_url_Date:
            txt_content = i.text
            # 有的数据解有两个。。。
            # ValueError: invalid literal for int() with base 10: '[468942,469935]'
            try:
                best_res_dict[txt_content.split(':')[0].strip()] = int(txt_content.split(':')[1].strip())
            except:
                print("网页抓到异常数据")
        print(best_res_dict)
            
            
    except:
    	print("未发现目标元素")

if __name__ == "__main__":
    get_best_result_from_web()


import setuptools #瀵煎叆setuptools鎵撳寘宸ュ叿
 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="TSP-dataloader", # 鐢ㄨ嚜宸辩殑鍚嶆浛鎹㈠叾涓?鐨刌OUR_USERNAME_
    version="0.0.2",    #鍖呯増鏈?鍙凤紝渚夸簬缁存姢鐗堟湰
    author="github@LT1st",    #浣滆€咃紝鍙?浠ュ啓鑷?宸辩殑濮撳悕
    author_email="1417274896@qq.com",    #浣滆€呰仈绯绘柟寮忥紝鍙?鍐欒嚜宸辩殑閭?绠卞湴鍧€
    description="Load all kinds of TSP test samples; Visualize routs; DEMO solusion", #鍖呯殑绠€杩?
    long_description=long_description,    #鍖呯殑璇︾粏浠嬬粛锛屼竴鑸?鍦≧EADME.md鏂囦欢鍐?
    long_description_content_type="text/markdown",
    url="https://github.com/LT1st/System_engineering_programm/tree/master",    #鑷?宸遍」鐩?鍦板潃锛屾瘮濡俫ithub鐨勯」鐩?鍦板潃
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',    #瀵筽ython鐨勬渶浣庣増鏈?瑕佹眰
)
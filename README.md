# 南华大学校园网自动登录项目

## 如何使用
1.安装python

2.下载仓库文件

3.修改usc_login_v2.py的username和password为你的校园网登录账号密码

~~~
username = "你的学号"
password = "你的密码"
~~~

4.将src文件夹下的文件放至同一目录下

5.编写bat文件
~~~
@echo off
python usc_login_v2.py文件的路径
pause
~~~

6.将bat文件放置在 C:\Users\用户名\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup 目录下

7.开机自动登录

## 原帖地址 
我在此基础上修改成适合我们学校的代码

感谢 https://blog.csdn.net/qq_41797946/article/details/89417722

## 结语
欢迎补充！

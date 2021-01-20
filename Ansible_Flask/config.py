# @Time    : 2021/1/15 15:01 
# @Author  : Rainbird
# @Email   : 731465297@qq.com
# @File    : config.py
# @Describe: Flask配置文件

# 配置文件，先定义默认主类，配置项全部大写
class Config(object):
    DEBUG = False
    SECRET_KEY = 'abcde'

# 定义不同的类来改变配置，继承自默认类
class MyConfig(Config):
    DEBUG = True


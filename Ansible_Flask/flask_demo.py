# @Time    : 2021/1/19 17:11 
# @Author  : Rainbird
# @Email   : 731465297@qq.com
# @File    : flask_demo.py
# @Describe: 

from flask import Flask, render_template, request, redirect, session, url_for
from myansible import *
import json

app = Flask(__name__)  # 实例化Flask对象
# 初始配置写进配置文件，再进行导入
# app.config.from_pyfile("xxx.py")  # 同级目录下的py文件，里面写配置，直接键值对，非主流
app.config.from_object("config.Config")  # 建议的写法，从同目录下config.py的Config类中读取配置
# app.debug = True
# app.secret_key = 'secret'  # 不建议这种写法，建议都写入配置文件中

# ansible的配置
host_group = ['server', ]
host_ips = {'server': ['139.155.89.83', '139.155.71.3', '139.155.75.245', '139.155.87.22', '139.155.75.143', '139.155.89.124']}

bak = {'waiting': 'waiting', }
USER = {'root': ['root', 'Tcdn@2020']}
result = {}

# 路由除了装饰器写法，也可以使用原始的写法：
# def login():
#     return 'Login'
# 这样分开写也可以实现装饰器的效果
# app.add_url_rule('/login', 'test_url', login, methods=['GET', 'POST'])  # 参数顺序：路由、url别名、调用的方法、其他参数

# 对ansible输出结果处理
def handle_result(result):
    machine = {
        '139.155.89.83': '',
        '139.155.71.3': '',
        '139.155.75.245': '',
        '139.155.87.22': '',
        '139.155.75.143': '',
        '139.155.89.124': ''
    }
    success = list(result['success'].keys())
    failed = list(result['failed'].keys())
    unreachable = list(result['unreachable'].keys())
    for i in success:
        machine[i] = 'success'
    for i in failed:
        machine[i] = 'failed'
    for i in unreachable:
        machine[i] = 'unreachable'
    return machine



@app.route('/index', methods=['GET', 'POST'], endpoint='l0')  # 路由写法，支持方法和url别名，如果endpoint不写，默认是函数名
def index():
    global result
    user = session.get('user_info')
    if not user:  # 无session则返回至登录界面
        url = url_for('l1', error="请先登录！")  # 反向生成url，后面跟参数
        return redirect(url)
    if request.method == 'GET':
        return render_template('index.html', info=bak)
    elif request.method == 'POST':
        command = request.form['command']
        myansible = MyAnsible2(connection='smart', host_group=host_group, host_ips=host_ips)  # 初始化ansible
        myansible.run(hosts='server', module='shell', args=command)
        result = myansible.get_result()
        print(result)
        myansible.check_ssh(result)
        machine = handle_result(result)  # 处理数据
        return render_template('index.html', info=machine)

@app.route('/detail/<nid>', methods=['GET'])  # 返回每个用户的个人信息
def detail(nid):
    nid = str(nid)
    # result = myansible.get_result()
    machine = handle_result(result)
    # test = json.dumps(result, indent=4)
    detail_info = {nid: result[machine[nid]][nid]}
    detail_info = json.dumps(detail_info, indent=4)
    return render_template('detail.html', info=detail_info)

@app.route('/login', methods=['GET', 'POST'], endpoint='l1')  # endpoint给url起别名，再通过url_for反向生成
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = request.form['user']
        pwd = request.form.get('pwd')
        if user == USER['root'][0] and pwd == USER['root'][1]:
            session['user_info'] = pwd  # 登陆成功返回session值
            print(session['user_info'])
            return render_template('index.html', info=bak)
            # return redirect('http://xbrainbird.cn')  # 重定向
        return render_template('login.html', error='用户名或密码错误！')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

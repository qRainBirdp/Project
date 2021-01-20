from myansible import *
import json

host_group = ['server', ]
host_ips = {'server': ['172.27.0.129', '172.27.0.133'], }

def get_last(result):
    msg = {}
    for i in host_ips['server']:
        num = result['success'][i]['stdout_lines'][0]
        if int(num) > 7:
            msg[i] = num
    return msg

def get_command_check(result):
    # msg = {}
    # for i in host_ips['server']:
    #    content = result
    #    msg[i] = content
    msg = json.dumps(result, indent=4)
    return msg


if __name__ == '__main__':
    last_check = MyAnsible2(connection='smart', host_group=host_group, host_ips=host_ips)
    last_check.run(hosts='server', module='shell', args='last|grep -v 49.234.105.202|wc -l')
    result_1 = last_check.get_result()
    last_check.check_ssh(result_1)
    print(result_1)
    





    

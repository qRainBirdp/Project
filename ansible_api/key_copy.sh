#!/bin/bash

vm=$1

# 执行清除脚本
sed -i "/^${vm}/d" ~/.ssh/known_hosts

expect <<-EOF 
set timeout 5
spawn ssh-copy-id $vm
expect {  
"(yes/no)" {send "yes\n"; exp_continue}
"password:" {send "Tcdn@2020\n"}
}
expect eof
EOF
sleep 1

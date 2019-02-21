#!/bin/bash

echo "使用全局变量"$ABC

echo -e "\n执行对象: $0"
echo -e "\n参数数量: $#"

# 脚本自身的参数
echo -e "\n通过序号取参数"
echo $1
echo $2
echo $3

echo -e "\n遍历所有参数"
for a in $@
do
echo $a
done

#!/bin/bash

# 变量定义: 等号前后没有空格
a=12345678

# 使用变量: 变量名前面加上 $ 符
echo "----$a----"
printf "===>$a<===\n"

# 定义当前Shell下的全局变量
export ABC=9876543210123456789
# 定义完后, 在终端里用 source 加载脚本
# source ./test.sh

echo "常用的系统环境变量"
echo -e "PATH:\n    $PATH\n"
echo -e "PWD:\n    $PWD\n"
echo -e "HOME:\n    $HOME\n"


# 分支控制语句: if
if [[ $a == "12345678" ]]; then
    echo 'this is a arg'
elif [ -d $0 ]; then
    echo 'this is a dir'
elif [ -f $0 ]; then
    echo 'this is a file'
else
    echo '98765432'
fi


# 循环控制语句: for
# 从1到10显示数字
for i in $(seq 1 10)
do
    echo "num: $i"
done


# 函数
foo() {
    echo "Hello BJ-1813"
    for f in `ls ../`
    do
        echo $f
    done
}


# 函数中使用参数
bar() {
    echo "执行者是 $0"
    echo "参数数量是 $#"

    if [ -d $1 ]; then  # 检查传入的第一个参数是否是文件夹
        for f in `ls $1`
        do
            echo $f
        done
    elif [ -f $1 ]; then
        echo 'This is a file: $1'  # 单引号内的变量不会被识别
        echo "This is a file: $1"  # 如果不是文件夹，直接显示文件名
    else
        echo 'not valid'  # 前面都不匹配显示默认语句
    fi
}

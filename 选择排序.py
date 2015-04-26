# coding=utf-8
__author__ = '陈文达'

# 输入数组

a = raw_input('请输入一串数字 用空格进行隔开').split(' ')
for j in range(len(a)):
    a[j] = int(a[j])
print "你输入的数为：", a

# 开始进行排序
for i in range(len(a)):
    c = a.index(min(a[i::])) # 获取最小值的索引号
    temp = a[i]
    a[i] = min(a[i::])
    a[c] = temp             #将第一个数与最小数进行交换

print '从小到大排序：',a


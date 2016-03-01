#coding=utf8
__author__ = 'Eric_Chan'
'''广外机考模拟考'''

import xlrd
import xlwt
from random import randint

def LodeTestdata(filename,SJJG = True):
    data = xlrd.open_workbook(filename)#打开xlsx
    table = data.sheet_by_index(0) #打开sheet1
    all_data = table._cell_values #将所有数据 以二元列表进行构造
    nrows = table.nrows #获得列表的行数
    ncols = table.ncols #获得列表的列数
    data_dic = {}
    if SJJG:
        for i in range(1,nrows):
            data_dic[i] = []
            for j in range(ncols):

                temp = all_data[i][j]
                data_dic[i].append(temp)
    else:

        for i in range(1,nrows):
            data_dic[i] = []
            for j in range(ncols):

                temp = all_data[i][j]
                data_dic[i].append(temp)

    ram = [randint(1,nrows-1) for i in range(32)] #产生随机32个题号
    return data_dic,ram

def Writexls(P,X,PDT_Data,XZT_Data,FileName):
    file1 = xlwt.Workbook()
    table1 = file1.add_sheet('判断错题集')#
    table2 = file1.add_sheet('选择错题集')#
    for i in range(len(P)):
        for j in range(len(PDT_Data[P[i]])):
            table1.write(i,j,PDT_Data[P[i]][j])

    for i in range(len(X)):
        for j in range(len(XZT_Data[X[i]])):
            table2.write(i,j,XZT_Data[X[i]][j])

    # table1.write(0,0,'test')#写入数据table.write(行,列,value)
    # file1.save('demo.xlsx')
    # for i in range(1,nrows):
    #     table1.write(i,0,all_data[i][1].encode('utf-8'))#写入数据table.write(行,列,value)
    file1.save(FileName)


def StartTest():
    print '                                                 广外机考模拟考试                                            '
    print '**************************************************************************************************************************'
    switch = raw_input('请选择科目：a  数据结构 ; b  离散数学')
    print '\n'
    switch.lower()
    while (switch!='a')&(switch!='b'):
        print '输入有误,请重新输入:'
        switch = raw_input()
    if switch == 'a':
        XZT_Data,ram_32 = LodeTestdata('bank/Sxzt.xls')
        PDT_Data,ram_18 = LodeTestdata('bank/Spdt.xls')
        fileName = '数据结构错题集.xls'
        print '现在开始进行 数据结构 模拟考'
        print '\n'
    elif switch == 'b':
        XZT_Data,ram_32 = LodeTestdata('bank/Lxzt.xls',False)
        PDT_Data,ram_18 = LodeTestdata('bank/Lpdt.xls',False)
        fileName = '离散数学错题集.xls'
        print '现在开始进行 离散数学 模拟考'
        print '\n'
    XZTrightanswer = 0
    PDTrightanswer = 0
    P = []#记录判断题错题号
    X = []#记录选择题错题号



    print '判断题'
    print '请回答 Y or N'
    for i in range(18):
        print '\n',i+1,PDT_Data[ram_18[i]][1]
        answer = raw_input("请判断正误(Y/N)：")
        answer = answer.upper()
        while (answer!='Y')&(answer!='N'):
            print '输入有误,请重新输入:'
            answer = raw_input()
            answer = answer.upper()
        if answer == PDT_Data[ram_18[i]][2]:
            PDTrightanswer = PDTrightanswer + 1
        else:
            P.append(ram_18[i])
    print '\n'
    print '**************************************************************************************************************************'
    print '选择题'
    print '请回答 ABCD'
    for i in range(32):
        print '\n',i+1,XZT_Data[ram_32[i]][1]
        print 'A',XZT_Data[ram_32[i]][2],'\n','B',XZT_Data[ram_32[i]][3],'\n','C',XZT_Data[ram_32[i]][4],'\n','D',XZT_Data[ram_32[i]][5],'\n'
        answer = raw_input("请输入答案：")
        answer = answer.upper()
        while (answer!='A')&(answer!='B')&(answer!='C')&(answer!='D'):
            print '输入有误,请重新输入:'
            answer = raw_input()
            answer = answer.upper()
        if answer == XZT_Data[ram_32[i]][8]:
            XZTrightanswer = XZTrightanswer + 1
        else:
            X.append(ram_32[i])

    P_zdl = float(PDTrightanswer)/18
    P_zdl = '%.2f'%P_zdl
    X_zdl = float(XZTrightanswer)/32
    X_zdl = '%.2f'%X_zdl
    zdl = float(PDTrightanswer + XZTrightanswer)/50
    zdl = '%.2f'%zdl
    score = (PDTrightanswer + XZTrightanswer) * 2
    print '\n'
    print '****************************'
    print '模拟考结束'
    print '判断题正答率:',P_zdl
    print '选择题正答率:',X_zdl
    print '正确率:',zdl
    print '分数:',score
    print '****************************'
    print '本次考试的错题已导出,请注意复习'
    print '\n','\n','                                by Eric Chan'
    Writexls(P,X,PDT_Data,XZT_Data,fileName)


StartTest()
#coding=utf8
__author__ = 'Eric_Chan'
'''广外机考模拟考'''

import xlrd
import xlwt
from random import randint

def LodeTestdata(filename):
    data = xlrd.open_workbook(filename)#打开xlsx
    table = data.sheet_by_index(0) #打开sheet1
    all_data = table._cell_values #将所有数据 以二元列表进行构造
    nrows = table.nrows #获得列表的行数
    ncols = table.ncols #获得列表的列数
    data_dic = {}
    for i in range(1,nrows):
        data_dic[i] = []
        for j in range(ncols):
            temp = all_data[i][j]
            # try:
            #     temp = temp.encode('utf-8')
            # except:
            #     temp = temp.encode('utf-8')
            #     continue
            data_dic[i].append(temp)

    ram = [randint(1,nrows-1) for i in range(50)] #产生随机50个题号
    return data_dic,ram,nrows

def Writexls(X,XZT_Data,FileName):
    file1 = xlwt.Workbook(encoding = 'utf-8')

    table2 = file1.add_sheet('sheet1')

    for i in range(len(X)):
        for j in range(len(XZT_Data[X[i]])):
            table2.write(i,j,XZT_Data[X[i]][j])

    # table1.write(0,0,'test')#写入数据table.write(行,列,value)
    # file1.save('demo.xlsx')
    # for i in range(1,nrows):
    #     table1.write(i,0,all_data[i][1].encode('utf-8'))#写入数据table.write(行,列,value)
    file1.save(FileName)


def StartTest():
    print u'                                                 广外机考模拟考试                                            '.encode('gbk')
    print '**************************************************************************************************************************'
    filename = raw_input('导入题库\n'.decode('utf-8').encode('gbk'))
    # while (switch!='a')&(switch!='b'):
    #     print u'输入有误,请重新输入:'.encode('gbk')
    #     switch = raw_input()
    # if switch == 'a':
    #     XZT_Data,ram_50 = LodeTestdata('bank/Sxzt.xls')
    #     PDT_Data,ram_18 = LodeTestdata('bank/Spdt.xls')
    #     fileName = '数据结构错题集.xls'.decode('utf-8').encode('gbk')
    #     print u'现在开始进行 数据结构 模拟考'.encode('gbk')
    #     print '\n'
    # elif switch == 'b':
    #     XZT_Data,ram_32 = LodeTestdata('bank/Lxzt.xls',False)
    #     PDT_Data,ram_18 = LodeTestdata('bank/Lpdt.xls',False)
    #     fileName = '离散数学错题集.xls'.decode('utf-8').encode('gbk')
    #     print u'现在开始进行 离散数学 模拟考'.encode('gbk')
    #     print '\n'
    while True:
        try:
            XZT_Data,ram_32,rows = LodeTestdata('bank/%s.xls'%filename)
            break
        except:
            print u'输入有误,请重新输入:'.encode('gbk')
            filename = raw_input()


    XZTrightanswer = 0
    X = []#记录选择题错题号



    # print u'判断题'.encode('gbk')
    # print u'请回答 Y or N'.encode('gbk')
    # for i in range(18):
    #     print '\n',i+1,PDT_Data[ram_18[i]][1].decode('utf-8').encode('gbk')
    #     answer = raw_input(u"请判断正误(Y/N)：".encode('gbk'))
    #     answer = answer.upper()
    #     while (answer!='Y')&(answer!='N'):
    #         print u'输入有误,请重新输入:'.encode('gbk')
    #         answer = raw_input()
    #         answer = answer.upper()
    #     if answer == PDT_Data[ram_18[i]][2]:
    #         PDTrightanswer = PDTrightanswer + 1
    #     else:
    #         P.append(ram_18[i])
    # print '\n'
    print '**************************************************************************************************************************'
    print u'选择题'.encode('gbk')
    print u'请回答 ABCD,不确定则回答N'.encode('gbk')
    # ram_32 = range(1,rows)
    for i in range(50):
    # for i in range(rows-1):
        try:
            print '\n',i+1,XZT_Data[ram_32[i]][1]
            print 'A',XZT_Data[ram_32[i]][2],'\n',\
                'B',XZT_Data[ram_32[i]][3],'\n',\
                'C',XZT_Data[ram_32[i]][4],'\n',\
                'D',XZT_Data[ram_32[i]][5],'\n'
            answer = raw_input("请输入答案：".decode('utf-8').encode('gbk'))
            answer = answer.upper()
            while (answer!='A')&(answer!='B')&(answer!='C')&(answer!='D')&(answer!='N'):
                print '输入有误,请重新输入:'.decode('utf-8').encode('gbk')
                answer = raw_input()
                answer = answer.upper()
            if answer == XZT_Data[ram_32[i]][8]:
                XZTrightanswer = XZTrightanswer + 1
            else:
                X.append(ram_32[i])
        except:
            X.append(ram_32[i])
            continue


    X_zdl = float(XZTrightanswer)/50
    X_zdl = '%.2f'%X_zdl
    score = XZTrightanswer
    print '\n'
    print '****************************'
    print '模拟考结束'.decode('utf-8').encode('gbk')
    print '选择题正答率:'.decode('utf-8').encode('gbk'),X_zdl
    print '分数:'.decode('utf-8').encode('gbk'),score
    print '****************************'
    print '\n','\n'
    try:
        Writexls(X,XZT_Data,"错题集.xls".decode("utf-8").encode('gbk'))
        print '本次考试的错题已导出,请注意复习'.decode('utf-8').encode('gbk')
    except:
        print u"错题导出失败，请关闭已打开的xls".encode('gbk')



StartTest()
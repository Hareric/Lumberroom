# coding=utf-8
#        ┏┓　　　┏┓+ +
# 　　　┏┛┻━━━┛┻┓ + +
# 　　　┃　　　　　　 ┃ 　
# 　　　┃　　　━　　　┃ ++ + + +
# 　　 ████━████ ┃+
# 　　　┃　　　　　　 ┃ +
# 　　　┃　　　┻　　　┃
# 　　　┃　　　　　　 ┃ + +
# 　　　┗━┓　　　┏━┛
# 　　　　　┃　　　┃　　　　　　　　　　　
# 　　　　　┃　　　┃ + + + +
# 　　　　　┃　　　┃　　　　Codes are far away from bugs with the animal protecting　　　
# 　　　　　┃　　　┃ + 　　　　神兽保佑,代码无bug　　
# 　　　　　┃　　　┃
# 　　　　　┃　　　┃　　+　　　　　　　　　
# 　　　　　┃　 　　┗━━━┓ + +
# 　　　　　┃ 　　　　　　　┣┓
# 　　　　　┃ 　　　　　　　┏┛
# 　　　　　┗┓┓┏━┳┓┏┛ + + + +
# 　　　　　　┃┫┫　┃┫┫
# 　　　　　　┗┻┛　┗┻┛+ + + +
"""
Author = Eric_Chan
Create_Time = 2016/09/03

"""

import MySQLdb
import xlrd


def load_data(file_name, sheet_index=None, include_header=True):
    """
    读取xls文件,获得矩阵.
    :param file_name: xls文件路径
    :param sheet_index: xls 打开的sheet序号
    :param include_header: Boolean  是否包含表头
    :return: 二元列表
    """
    if sheet_index is None:
        sheet_index = 0
    data = xlrd.open_workbook(file_name)  # 打开xls
    table = data.sheet_by_index(sheet_index)  # 打开sheet1
    all_data = table._cell_values  # 将所有数据 以二元列表进行构造
    if not include_header:
        all_data = all_data[1:]  # 除去表头
    for i in range(all_data.__len__()):  # 将表中数据的整数转化为int类型
        for j in range(all_data[0].__len__()):

            try:
                if all_data[i][j] == int(all_data[i][j]):
                    all_data[i][j] = int(all_data[i][j])
            except ValueError:
                continue
    return all_data


def write_db(ip='localhost', user='root', pwd='', database=None, data_in=None, table_name=None):
    """

    :param ip:
    :param user:
    :param pwd:
    :param database:
    :param data_in
    :return:
    """
    db = MySQLdb.connect(ip, user, pwd, database)
    cursor = db.cursor()

    for d in data_in:
        sql = "INSERT INTO %s VALUES " % table_name
        sql += '('
        for t in d:
            sql += "'%s', " % t
        sql = sql[:-2]
        sql += ');'
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            try:
                sql = "INSERT INTO %s VALUES " % table_name
                sql += '('
                for t in d:
                    try:
                        t = str(t)
                    except UnicodeEncodeError:
                        t = t.encode('utf-8')
                    t = t.replace('\'', '\\\'')
                    sql += "'%s', " % t
                sql = sql[:-2]
                sql += ');'
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
                print sql

    db.close()


if __name__ == '__main__':
    all_data = load_data('test.xlsx', include_header=False)
    write_db(pwd='', database='ExaminationSystem', table_name='choice', data_in=all_data)

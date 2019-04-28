
# -*- coding:utf-8 -*-
import pandas as pd
import os
#定义xls文件转csv的方法
def xls2csv(xls_file, csv_file):
    data = pd.read_excel(xls_file, '1、人工成本拆解表', index_col = 0)
    data.to_csv(csv_file, encoding="utf-8")

#读取一个文件夹的所有文件

def read_path(file_path):
    dirs = os.listdir(file_path)
    return dirs

def main():
    source = 'D:\\Users\\User\\Desktop\\北京首创\\报表数据\\污水-分析、拆解'
    ob = r"D:\\Users\\User\\Desktop\\北京首创\\报表数据\\污水-分析、拆解csv"
    list = read_path(source)
    for i in list:
        xls_file = source + '/' + i
        csv_file = ob + '/'+ i.replace('xls', 'csv')
        xls2csv(xls_file, csv_file)

if __name__ == '__main__':
    main()










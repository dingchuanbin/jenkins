#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ding
import argparse
import xlrd
import json
import sys
import subprocess


class Exceldb(object):
    def __init__(self,filename):
        self.filename = filename

    def book(self):
        try:
            book = xlrd.open_workbook(self.filename)
            return book
        except Exception as e:
            print(str(e))

    def t_sheets(self):
        book = self.book()
        s_names = book.sheet_names()
        ws = {}
        for i in s_names:
            ws[i] = book.sheet_by_name(i)
        return ws

class Ex_table(object):

    def __init__(self,filename,t_name):
        self.filename = filename
        self.t_name = t_name
        self.t_table = Exceldb(self.filename).t_sheets()[self.t_name]

    def col_field(self):
        column_hash = {}
        for i in range(self.t_table.ncols):
            column_hash[self.t_table.cell_value(0, i)] = i
        return column_hash

    def col_field(self):
        column_hash = {}
        for i in range(self.t_table.ncols):
            column_hash[self.t_table.cell_value(0, i)] = i
        return column_hash

    def f_v_dict(self,f_index):
        f_v_list = []
        f_v_dict = {}
        for i in range(1, self.t_table.nrows):
            f_v_list.append(self.t_table.cell_value(i, self.col_field()[f_index]))
            f_v_dict[f_index] = f_v_list
        return f_v_dict

    def f_v_k_dict(self,f_index):
        k_v_k_dict = {}
        ifmulti = {}
        # 初始化模块出现次数字典
        for i in range(1,self.t_table.nrows):
            ifmulti[self.t_table.cell_value(i, self.col_field()[f_index])] = 0
        for i in range(1,self.t_table.nrows):
            f_vk_dict = {}
            if ifmulti[self.t_table.cell_value(i, self.col_field()[f_index])] != 0:    #判断模块是否第一次循环，模块字典列表取值
                f_vk_list = k_v_k_dict[self.t_table.cell_value(i, self.col_field()[f_index])]
            else:
                f_vk_list = []
            for n in range(self.t_table.ncols):
                if n not in [self.col_field()[f_index],]:
                    if self.t_table.cell_value(i,n):   #单元格是否为空
                        f_vk_dict[self.t_table.cell_value(0, n)] = self.t_table.cell_value(i, n)
                    else:
                        #值为空即为合并单元格，倒叙循环到前面有值的行
                        for m in range(i,1,-1):
                            if self.t_table.cell_value(m,n):
                                f_vk_dict[self.t_table.cell_value(0, n)] = self.t_table.cell_value(m, n)
                                break
            f_vk_list.append(f_vk_dict)
            ifmulti[self.t_table.cell_value(i, self.col_field()[f_index])] += 1
            k_v_k_dict[self.t_table.cell_value(i, self.col_field()[f_index])]=f_vk_list
        return k_v_k_dict



extable = Ex_table('BBST.xlsx','bitbullexRea')
print(extable.f_v_k_dict('appname')['tradefront'])
print(extable.f_v_dict('appname'))
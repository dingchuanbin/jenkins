#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:ding
import argparse
import xlrd
import json

def open_file(filename):
    try:
        data = xlrd.open_workbook(filename)
        return data
    except Exception as e:
        print(str(e))

def inventory(filename,sheetbyname='',group_index='',host_index=''):
    wb = open_file(filename)
    ws = wb.sheet_by_name(sheetbyname)
    column_hash = {}
    for i in range(ws.ncols):
        column_hash[ws.cell_value(0, i)] = i
    group_column_name = column_hash[group_index]
    host_column_name = column_hash[host_index]
    group_hash = {}
    multiapp = None
    for i in range(1,ws.nrows):
        appname = ws.cell_value(i, group_column_name)
        if  multiapp == appname:
            hostlist = hostlist
        else:
            hostlist = []
        varsdict = {}
        group_hash[ws.cell_value(i, group_column_name)] = {'hosts':[],'vars':{}}
        hostlist.append(ws.cell_value(i,host_column_name))
        for n in  range(ws.ncols):
            if n not in [0,group_column_name,host_column_name]:
                varsdict[ws.cell_value(0,n)]=ws.cell_value(i,n)
        group_hash[ws.cell_value(i, group_column_name)]['hosts'] = hostlist
        group_hash[ws.cell_value(i, group_column_name)]['vars'] = varsdict
        multiapp = ws.cell_value(i, group_column_name)
    return json.dumps(group_hash,indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', help='hosts list', action='store_true')
    args = vars(parser.parse_args())
    if args['list']:
        print(inventory('BBST.xlsx','bitbullexRea','appname','ip'))



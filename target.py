import os

import numpy as np

from util import *


def extra_target(project, release):
    data_all = readData(path=code_path + project + '/', file=release + '/used_node_data.csv')
    df_sorted = data_all.sort_values(by='max_suspicious', ascending=False)  
    method_data = df_sorted.drop_duplicates('method_name', keep='first')
    sort_data = data_all.drop_duplicates('method_name', keep='first')

    method_sorted = []
    method_label = []
    method_name = []
    sort = 1
    for method_index in method_data.index:
        method = method_data.loc[method_index, 'method_name']
        sort_data.loc[sort_data['method_name'] == method, 'method_sort'] = sort
        # method_sorted.append(method)
        sort += 1

    for method_index in sort_data.index:  
        # method_name.append(sort_data.loc[method_index, 'method_name'])
        rank = sort_data.loc[method_index, 'method_sort'] 
        if sort_data.loc[method_index, 'max_suspicious'] >= 0.9:
            method_label.append(1)
        else:
            method_label.append(0)
        method_sorted.append(int(rank))

    n_dim_list = np.array(method_sorted).reshape(-1, 1)
    n_dim_list1 = np.array(method_label).reshape(-1, 1)

    forder = code_path + project + '/' + release
    np.savetxt(forder+'/method_target.txt', n_dim_list, fmt='%d')  
    np.savetxt(forder + '/method_label.txt', n_dim_list1, fmt='%d')


if __name__ == '__main__':
    for project in my_project.keys():
        for release in my_project[project]:
            extra_target(project, release)

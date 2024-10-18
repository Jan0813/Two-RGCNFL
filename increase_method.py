import os
import re

import numpy as np
import pandas as pd
from util import *


def increase_method(project, release):
    data_all = readData(path=code_path + project + '/', file=release + '/all_data.csv')
    data = data_all.drop_duplicates('filename', keep='first')
    data_all['method_name'] = None
    for index in data.index: 
        file_name = str(data.loc[index, 'filename'])  
        java_name = file_name.split('.')[-1] 
        # pdg_path = code_path + project + '/' + release + '/PDG/' + java_name
        pdg_path = 'G:\\defects4j\\{}\\{}_{}_buggy\\source\\org\\PDG\\{}'.format(project, project, release, java_name)
        methods_name = []
        try:
            with open(pdg_path + '_pdg.dot', encoding='utf-8') as f:
                contents = f.read().split('\n') 
                for i in range(len(contents)):  
                    content = contents[i]

                    if ('label = "' in content) & ('...' in content) & (content.endswith('>";')):  
                        results = re.findall(r'"(.*?)"', content)[0]
                        methods = results.split(' ') 
                        method_name = methods[0]

                        index = 1
                        while method_name in methods_name:
                            method_name = method_name + str(index) 
                            index += 1
                        methods_name.append(method_name)

                        method_name = file_name + '.' + method_name
                        lines = get_line_num(content) 

                        begin = data_all.loc[
                                (data_all['filename'] == file_name) & (data_all['line_number'] == lines[0]), :].index

                        end = data_all.loc[
                                (data_all['filename'] == file_name) & (data_all['line_number'] == lines[-1]), :].index
                        max_index = data_all.loc[begin.tolist()[0]:end.tolist()[0], 'suspicious'].idxmax()  
                        max_suspicious = data_all.loc[max_index, 'suspicious']
                        for line in lines: 
                            data_all.loc[(data_all['filename'] == file_name) & (
                                    data_all['line_number'] == line), 'method_name'] = method_name
                            data_all.loc[(data_all['filename'] == file_name) & (
                                    data_all['line_number'] == line), 'max_suspicious'] = max_suspicious 

        except:
            with open(pdg_path + '_pdg.dot', encoding='ansi') as f:
                contents = f.read().split('\n')
                for i in range(len(contents)):
                    content = contents[i]
                    if ('label = "' in content) & ('...' in content) & (content.endswith('>";')):
                        results = re.findall(r'"(.*?)"', content)[0]
                        methods = results.split(' ')  
                        method_name = methods[0]

                        index = 1
                        while method_name in methods_name:
                            method_name = method_name + str(index)
                            index += 1
                        methods_name.append(method_name)

                        lines = get_line_num(content) 
                        begin = data_all.loc[
                                (data_all['filename'] == file_name) & (data_all['line_number'] == lines[0]), :].index
                        end = data_all.loc[
                              (data_all['filename'] == file_name) & (data_all['line_number'] == lines[-1]), :].index
                        max_index = data_all.loc[begin.tolist()[0]:end.tolist()[0], 'suspicious'].idxmax()  
                        max_suspicious = data_all.loc[max_index, 'suspicious']
                        for line in lines:
                            data_all.loc[(data_all['filename'] == file_name) & (
                                    data_all['line_number'] == line), 'method_name'] = method_name 
                            data_all.loc[(data_all['filename'] == file_name) & (
                                    data_all[
                                        'line_number'] == line), 'max_suspicious'] = max_suspicious 

        f.close()
    data_all.loc[:, 'method_name'].fillna('None', axis=0, inplace=True)
    data_all.loc[:, 'max_suspicious'].fillna(0, axis=0, inplace=True)
    #
    # for index, row in data_all.iterrows():
    #     if (data_all.loc[index, 'method_name']) == 'None':
    #         data_all.drop(index, inplace=True)
    #
    data_all.to_csv(code_path + project + '/' + release + '/used_method_data.csv',
                    encoding='latin', index=False)


if __name__ == '__main__':
    for project in my_project.keys():
        for release in my_project[project]:
            increase_method(project, release)

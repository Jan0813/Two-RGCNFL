import os

import numpy as np
import pydot

from util import *


def distinguish(method_str):
    digit = []
    name = []

    for char in method_str:
        if char.isdigit():  
            digit.append(char)
        elif char.isalpha():  
            name.append(char)
    return ''.join(name), ''.join(digit)


def get_allMethod_pdg(project, release):
    data_all = readData(path=code_path + project + '/', file=release + '/reduce_method_data.csv')
    file_data = data_all.drop_duplicates('filename', keep='first')  

    for file_index in file_data.index:  
        file_name = str(file_data.loc[file_index, 'filename']).replace('.', '/')  
        java_name = file_name.split('/')[-1]  
        folder = code_path + project + '/' + release + '/node&edge/' + file_name
        # pdg_path = code_path + project + '/' + release + '/PDG/' + java_name
        pdg_path = 'G:\\defects4j\\{}\\{}_{}_buggy\\source\\org\\PDG\\{}'.format(project, project, release, java_name)
        print(pdg_path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        file_df = data_all.loc[data_all['filename'] == file_name.replace('/', '.'), :]
        method_data = file_df.drop_duplicates('method_name', keep='first')

        node_lines = {}  
        edges = []
        for method_index in method_data.index:  
            method_name = str(method_data.loc[method_index, 'method_name'])  
            method_name = method_name.split('.')[-1]
            method_name, method_digit = distinguish(method_name) 
            print(method_name, method_digit)
            try:
                with open(pdg_path + '_pdg.dot', encoding='utf-8') as f:
                    contents = f.read().split('\n') 
                    index = 1
                    for i in range(len(contents)):  
                        content = contents[i]
                        if (method_name in content) & content.endswith('>";'):  

                            if method_digit == '' or (method_digit != '' and index == int(method_digit) % 10):
                                for j in range(i + 1, len(contents)):  
                                    content = contents[j]
                                    if '}' in content:  
                                        break
                                    if ('style = ' in content) & ('label = ' in content) \
                                            & ('fillcolor = aquamarine' not in content) & (' -> ' not in content):

                                        while ('fillcolor' not in content) | ('shape' not in content) | (
                                                not content.endswith('];')):
                                            i += 1
                                            if i >= len(contents):
                                                break
                                            content = content + '' + contents[i]
                                        node = content.split(' ')[0]  
                                        lines = get_line_num(content)  
                                        node_lines[node] = lines
                                        if 'shape = box' in content:
                                            node_label = 1
                                        elif 'shape = ellipse' in content:
                                            node_label = 2
                                        elif 'shape = diamond' in content:
                                            node_label = 3
                                        else:
                                            node_label = 4
                                        for line in lines: 
                                            data_all.loc[(data_all['filename'] == file_name.replace('/', '.')) & (
                                                    data_all['line_number'] == line), 'node_label'] = node_label

                                    if ('->' in content) & ('[style =' in content) & ('label=' in content) & (
                                            content.endswith('"];')):
                                        edge_source = content.split(' ')[0]  
                                        edge_target = content.split(' ')[2]  
                                        if 'style = dotted' in content:
                                            edge_label_flag = 1
                                        elif 'style = solid' in content:
                                            edge_label_flag = 2
                                        elif 'style = bold' in content:
                                            edge_label_flag = 3
                                        else:
                                            edge_label_flag = 4
                                        edges.append([edge_source, edge_target, edge_label_flag])  
                            else:  
                                index += 1

            except:
                with open(pdg_path + '_pdg.dot', encoding='ansi') as f:
                    contents = f.read().split('\n') 
                    index = 1
                    for i in range(len(contents)): 
                        content = contents[i]
                        if (method_name in content) & content.endswith('>";'):  

                            if method_digit == '' or (method_digit != '' and index == int(method_digit) % 10):
                                for j in range(i + 1, len(contents)):  
                                    content = contents[j]
                                    if '}' in content:  
                                        break
                                    if ('style = ' in content) & ('label = ' in content) \
                                            & ('fillcolor = aquamarine' not in content) & (' -> ' not in content):

                                        while ('fillcolor' not in content) | ('shape' not in content) | (
                                                not content.endswith('];')):
                                            i += 1
                                            if i >= len(contents):
                                                break
                                            content = content + '' + contents[i]
                                        node = content.split(' ')[0] 
                                        lines = get_line_num(content) 
                                        node_lines[node] = lines
                                        if 'shape = box' in content:
                                            node_label = 1
                                        elif 'shape = ellipse' in content:
                                            node_label = 2
                                        elif 'shape = diamond' in content:
                                            node_label = 3
                                        else:
                                            node_label = 4
                                        for line in lines: 
                                            data_all.loc[(data_all['filename'] == file_name.replace('/', '.')) & (
                                                    data_all['line_number'] == line), 'node_label'] = node_label

                                    if ('->' in content) & ('[style =' in content) & ('label=' in content) & (
                                            content.endswith('"];')):
                                        edge_source = content.split(' ')[0] 
                                        edge_target = content.split(' ')[2] 
                                        if 'style = dotted' in content:
                                            edge_label_flag = 1
                                        elif 'style = solid' in content:
                                            edge_label_flag = 2
                                        elif 'style = bold' in content:
                                            edge_label_flag = 3
                                        else:
                                            edge_label_flag = 4
                                        edges.append([edge_source, edge_target, edge_label_flag])  # 出边、入边、边类型
                            else:
                                index += 1

        source = []
        target = []
        edge_label = []  
        # print(edges) 
        # print(node_lines)
        for edge in edges: 

            if (edge[0] in node_lines.keys()) & (edge[1] in node_lines.keys()): 

                for i in node_lines.get(edge[0]):
                    for j in node_lines.get(edge[1]):
                        # print(file_name, i, j)
                        source_id = data_all.loc[(data_all['filename'] == file_name.replace('/', '.')) & (
                                data_all['line_number'] == i)]['node_id'].values + 1
                        target_id = data_all.loc[(data_all['filename'] == file_name.replace('/', '.')) & (
                                data_all['line_number'] == j)]['node_id'].values + 1
                        if (source_id.size != 0) & (target_id.size != 0):
                            source.append(source_id[0])
                            target.append(target_id[0])
                            edge_label.append(edge[2]) 
                        # print(source, target)
        pdg = np.vstack((source, target)).T 
        print(pdg)
        print(len(pdg))
        np.savetxt(folder + '/' + java_name + '_pdg.txt', pdg, fmt='%d')  
        np.savetxt(folder + '/' + java_name + '_edge_label.txt', edge_label, fmt='%d')

       data_all.loc[:, 'node_label'].fillna(4, axis=0, inplace=True)
    data_all.to_csv(code_path + project + '/' + release + '/used_node_data.csv', encoding='latin', index=False)


if __name__ == '__main__':
    for project in my_project.keys():
        for release in my_project[project]:
            get_allMethod_pdg(project, release)

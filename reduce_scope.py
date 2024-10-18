import numpy as np

from util import *


def reduce_scope(project, release):
    data_all = readData(path=code_path + project + '/', file=release + '/used_method_data.csv')
    for index, row in data_all.iterrows():
        if data_all.loc[index, 'max_suspicious'] == 0 or data_all.loc[index, 'is_comment'] == np.bool_(True):
            data_all.drop(index, inplace=True)

    data = data_all.drop_duplicates('filename', keep='first')
    for index in data.index: 
        file_name = str(data.loc[index, 'filename'])
        df = data_all.loc[data_all['filename'] == file_name, :]
        node_id = 0
        for i in df.index:
            line_number = df.loc[i, 'line_number']
            data_all.loc[
                (data_all['filename'] == file_name) & (data_all['line_number'] == line_number), 'node_id'] = node_id
            node_id += 1

    data_all.to_csv(code_path + project + '/' + release + '/reduce_method_data.csv',
                    encoding='latin', index=False)


if __name__ == '__main__':
    for project in my_project.keys():
        for release in my_project[project]:
            reduce_scope(project, release)

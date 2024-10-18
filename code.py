import os
import re

import numpy as np
import pandas as pd
from util import *


def is_comment_line(code_line, comments_list): 
    code_line = code_line.strip()

    if len(code_line) == 0:
        return False
    elif code_line.startswith('//'):  
        return True
    elif code_line in comments_list:
        return True

    return False


def is_empty_line(code_line):  

    if len(code_line.strip()) == 0:
        return True

    return False


def extra_java_code(filepath_list, project, release):
    code_df_list = []

    for filepath in filepath_list:

        df = pd.DataFrame()  

        # filepaths = code_path + project + '/' + release + '/' + filepath.replace('.', '/') + '.java'  
        filepaths = 'G:\\defects4j\\{}\\{}_{}_buggy\\source'.format(project, project, release) + '/' + \
                    filepath.replace('.', '/') + '.java '

        with open(filepaths, encoding="utf-8", mode="r") as f:
            code_str = f.read()
            code_lines = code_str.splitlines()  

            source_code_lines = []
            is_comments = []  
            is_blank_line = []  

            comments = re.findall(r'(/\*[\s\S]*?\*/)', code_str, re.DOTALL)  
            comments_str = '\n'.join(comments)  
            comments_list = comments_str.split('\n') 
            comments_list = [x.strip() for x in comments_list]

            for l in code_lines:
                l = l.strip()  # str.strip(): 
                is_comment = is_comment_line(l, comments_list)
                is_comments.append(is_comment)  

                is_blank_line.append(is_empty_line(l))  
                source_code_lines.append(l) 

        df['filename'] = [filepath] * len(code_lines)  
        df['code_line'] = source_code_lines  
        df['line_number'] = np.arange(1, len(code_lines) + 1)  
        df['is_comment'] = is_comments  
        df['is_blank'] = is_blank_line  

        if len(df) > 0:
            code_df_list.append(df)
    all_df = pd.concat(code_df_list)  
    return all_df


def extra_java_file(project, release):
    with open(suspicious_path + project + '/' + release + '/' + 'spectra.txt', encoding="utf-8", mode="r") as f:
        file = f.read().splitlines()
        filename = []
        for line in file:
            content = line.split('#')
            if (float(content[-1]) > 0.5):  
                filename.append(content[0])
        filename = set(filename)  
        all_df = extra_java_code(filename, project, release)
        for line in file:
            content = line.split('#')
            if (float(content[-1]) > 0.5):
                all_df.loc[
                    (all_df['filename'] == content[0]) & (all_df['line_number'] == int(content[1])), 'suspicious'] \
                    = float(content[-1])
        all_df['suspicious'] = all_df['suspicious'].fillna(0)

        if not os.path.exists(code_path + project + '/' + release):
            os.makedirs(code_path + project + '/' + release)

        all_df.to_csv(code_path + project + '/' + release + '/all_data.csv', index=False)


if __name__ == '__main__':
    for project in my_project.keys():
        # for release in my_project[project]:
        for release in range(26, 27):
            extra_java_file(project, str(release))

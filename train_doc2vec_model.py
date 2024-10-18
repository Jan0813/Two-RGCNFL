import os.path
import time
from util import *
from gensim.models import Doc2Vec
from gensim.models.doc2vec import TaggedDocument
import pandas as pd
import random
import warnings

warnings.filterwarnings('ignore')

model_path = 'defects4jData/model/'


class DocumentDataset(object):
    def __init__(self, data: pd.DataFrame, column):
        document = data[column].apply(self.preprocess)  
        print(type(document), column, type(data))
        self.documents = [TaggedDocument(text, [index]) for index, text in document.items()]

    def preprocess(self, document):
        # return preprocess_string(remove_stopwords(document))
        return document

    def __iter__(self):
        for document in self.documents:
            yield document

    def tagged_documents(self, shuffle=False):
        if shuffle:
            random.shuffle(self.documents)
        return self.documents


# read data
def readData(path, file):
    data = pd.read_csv(path + file, encoding='latin')
    return data


def train_doc2vec(project, release, method='lineflow'):  # method='noflow'
    if method =='lineflow':
        data = readData(stream_path+project+'/', release + '_line_flow.csv')
    elif method =='noflow':
        data = readData(stream_path+project+'/', release + '_noflow.csv')
    elif method == 'linenoflow':
        data = readData(stream_path+project+'/', release + '_linenoflow.csv')
    data['code_line'] = data['code_line'].astype(str) 
    document_dataset = DocumentDataset(data, 'code_line')
    docVecModel = Doc2Vec(min_count=1,
                          window=5,
                          vector_size=100,
                          sample=1e-4,
                          negative=5,
                          workers=2,
                          )
    docVecModel.build_vocab(document_dataset.tagged_documents())
    print('training......')
    docVecModel.train(document_dataset.tagged_documents(shuffle=False),  
                      total_examples=docVecModel.corpus_count,
                      epochs=20)

    if not os.path.exists(model_path + project):
        os.mkdir(model_path + project)

    if method == 'lineflow':
        docVecModel.save(model_path + project + '/' + release + '_lineflow.d2v')
    elif method == 'linenoflow':
        docVecModel.save(model_path + project + '/' + release + '_linenoflow.d2v')
    elif method == 'noflow':
        docVecModel.save(model_path + project + '/' + release + '_noflow.d2v')
    print('done!')


def main():
    total_time = 0
    count = 0
    for project in my_project.keys():
        for release in my_project[project]:
            start_time = time.time()
            train_doc2vec(project=project, release=release, method='lineflow')
            end_time = time.time()
            elapsed_time = end_time - start_time
            total_time += elapsed_time
            count += 1
            print(f"Project: {project}, Time: {elapsed_time} seconds")

    # average_time = total_time / count
    # print(f"Average Time: {average_time} seconds")


if __name__ == '__main__':
    main()

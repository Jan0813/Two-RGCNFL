from util import *

data_path = './data/'


def tudataset(project, version):
    dataset_train = MYDataset(root=(code_path + project), name=version, use_node_attr=True)
    return dataset_train


if __name__ == '__main__':
    for project in my_project.keys():
        cur_releases = my_project[project]
        for release in cur_releases:
            tudataset(project=project, version=release)
            print(release, 'done')

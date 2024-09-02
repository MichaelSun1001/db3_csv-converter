from converter import read_bag
import os
import sys

argvs = sys.argv
argc = len(argvs)


def main():
    # if (argc != 2):
    #     print('Usage: #ros2bag-convert xxx.db3')
    #     quit()
    # file_url = argvs[1]
    file_url = 'rosbag2_2023_10_14-21_41_09_0.db3'
    read_bag.read_write_from_all_topics(file_url, True)


if __name__ == '__main__':
    main()

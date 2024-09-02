import csv
import json
import time
import numpy as np
import math


def save_csv_file(data, csv_file_name, version=0, print_out=False):
    """ 保存数据到 CSV 文件（在 'read_from_all_topics' 之后使用）。"""
    frame_num = 0
    Time_ms_first = 0
    point_dic = {}
    camera_h264 = {}

    # 创建 CSV 文件
    with open(csv_file_name, mode='w', newline='') as csv_file:
        field_names = []
        writer = None
        nt, line_datas = data[0], data[1]
        Time_ms_first = '{}.{}'.format(
            int(nt[0] / 1000 / 1000), nt[0] % (1000 * 1000))
        Time_ms_first = float(Time_ms_first)

        for index in range(len(line_datas)):
            row_time, row_data = nt[index], line_datas[index]
            row_time_sec = int(row_time / 1000 / 1000)
            row_time_nsec = row_time % (1000 * 1000)
            row_time = '{}.{}'.format(row_time_sec, row_time_nsec)
            f_row_time = float(row_time)

            if csv_file_name.endswith('camera_h264.csv'):
                if writer is None:
                    field_names = ['time'] + list(row_data.keys())
                    writer = csv.DictWriter(csv_file, fieldnames=field_names)
                    writer.writeheader()  # 写入表头
                row_data["time"] = row_time
                writer.writerow(row_data)  # 写入数据行

            if csv_file_name.endswith('radar_points.csv'):
                point_dic['Frame_Number'] = index + 1
                Time_ms = f_row_time - Time_ms_first
                points = row_data['point_clouds']
                for points_index in range(len(points)):
                    point_dic['Point_Number'] = points_index + 1
                    point = points[points_index]

                    point_dic['X_m'] = math.cos(point['elevation']) * \
                        point['range'] * math.cos(point['azimuth'])
                    point_dic['Y_m'] = math.cos(point['elevation']) * \
                        point['range'] * math.sin(point['azimuth'])
                    point_dic['Vx_ms'] = point['velocity']
                    point_dic['Z_m'] = math.sin(
                        point['elevation']) * point['range']
                    point_dic['RCS_dbm2'] = point['rcs']
                    point_dic['Time_ms'] = Time_ms
                    point_dic['probability'] = point['probability']
                    point_dic['snr'] = point['snr']
                    if writer is None:
                        field_names = list(point_dic.keys())
                        writer = csv.DictWriter(
                            csv_file, fieldnames=field_names)
                        writer.writeheader()  # 写入表头
                    writer.writerow(point_dic)  # 写入数据行

    print('Saving', csv_file_name)


# import csv
# import json
# import time
# import numpy as np
# import math


# def save_csv_file(data, csv_file_name, version=0, print_out=False):
#     """ Save data to a csv_file_name (use it after 'read_from_all_topics').
#     """
#     frame_num = 0
#     Time_ms_first = 0
#     point_dic = {}
#     camera_h264 = {}

#     # print('123456789' + csv_file_name)

#     # Create csv file
#     with open(csv_file_name, mode='w') as csv_file:
#         # csv_file.write(str("topic_names = %s \n" %len(data)))
#         # Create csv header
#         field_names = []
#         writer = None
#         # print("-------------------------------")
#         nt, line_datas = data[0], data[1]  # data[1]是列表，列表里面是字典对应每一帧的msg数据；
#         Time_ms_first = '{}.{}'.format(
#             int(nt[0]/1000/1000), nt[0] % (1000 * 1000))
#         Time_ms_first = float(Time_ms_first)
#         for index in range(len(line_datas)):
#             # line_datas是字典；每一帧的数据
#             row_time, row_data = nt[index], line_datas[index]
#             # row_time = '{}.{}'.format(time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(
#             #     row_time / 1000 / 1000 / 1000)), row_time % (1000 * 1000 * 1000))
#             row_time_sec = int(row_time / 1000 / 1000)
#             row_time_nsec = row_time % (1000 * 1000)
#             row_time = '{}.{}'.format(row_time_sec, row_time_nsec)
#             f_row_time = float(row_time)

#             # if writer is None:
#             #     field_names = ['time']+list(row_data.keys())
#             #     writer = csv.DictWriter(csv_file, fieldnames=field_names)
#             #     # 完成csv表头的写入
#             #     writer.writeheader()
#             # row_data["time"] = row_time
#             # writer.writerow(row_data)  # 写入所有键值对的值

#             if csv_file_name == 'db3/camera_h264.csv':
#                 # row_data = [row_time]+list(row_data.values())
#                 # 时间戳为纳秒级别时间戳
#                 if writer is None:
#                     field_names = ['time']+list(row_data.keys())
#                     writer = csv.DictWriter(csv_file, fieldnames=field_names)
#                     writer.writeheader()
#                     # 完成csv表头的写入
#                 row_data["time"] = row_time
#                 writer.writerow(row_data)  # 写入所有键值对的值
#             if csv_file_name == 'db3/radar_points.csv':
#                 point_dic['Frame_Number'] = index + 1

#                 Time_ms = f_row_time - \
#                     Time_ms_first  # 第一帧的时间戳为0没有解决
#                 points = row_data['point_clouds']
#                 # 转换点云的数据变成xyz坐标值
#                 for points_index in range(len(points)):
#                     point_dic['Point_Number'] = points_index + 1
#                     point = points[points_index]

#                     point_dic['X_m'] = math.cos(point['elevation']) * \
#                         point['range'] * math.cos(point['azimuth'])

#                     point_dic['Y_m'] = math.cos(point['elevation']) * \
#                         point['range'] * math.sin(point['azimuth'])

#                     point_dic['Vx_ms'] = point['velocity']

#                     point_dic['Z_m'] = math.sin(
#                         point['elevation']) * point['range']

#                     point_dic['RCS_dbm2'] = point['rcs']
#                     point_dic['Time_ms'] = Time_ms
#                     # 点云不重要参数
#                     point_dic['probability'] = point['probability']
#                     point_dic['snr'] = point['snr']
#                     # 逐行写入
#                     if writer is None:
#                         field_names = list(point_dic.keys())
#                         writer = csv.DictWriter(
#                             csv_file, fieldnames=field_names)
#                         writer.writeheader()
#                     writer.writerow(point_dic)

#             # 完成csv表头的写入

#             # 在这里开始修改成自己想要的格式，而不是全部输出所有键值对的值

#             # print(row_time,row_data)

#             # print("-------------------------------")
#             # print(line)
#         #     if flag:
#         #         # 获取属性列表
#         #         keys = list(line.keys())
#         #         print(keys)
#         #         writer.writerow(keys) # 将属性列表写入csv中
#         #         flag = False
#         # # 读取json数据的每一行，将values数据一次一行的写入csv中
#         # writer.writerow(list(line.values()))

#         # Save data
#         # for i in range(len(data)):
#         #     topic_name = data[i][0]
#         #     topic_type = data[i][1]

#         #     for j in range(len(data[i][2])):
#         #         writer.writerow({   'topic_name': topic_name,
#         #                             'topic_type': topic_type,
#         #                             'time_stamp': data[i][2][j],
#         #                             'message': data[i][3][j] })

#     # if print_out:
#     print('Saving', csv_file_name)

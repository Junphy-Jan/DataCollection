import os
import time

import matplotlib.pyplot as plt
import json

from CommonUtils.constant import COLLECT_INTERVAL

relative_dir = "../collected_data/hot_search/"
prefix_file_name = "hot_search_"
for hs_file in os.listdir(relative_dir):
    hs_time = hs_file.split(".")[0].replace(prefix_file_name, "")
    hs_yyyy, hs_mm, hs_d = hs_time.split("_")
    print(hs_time)
    with open(os.path.join(relative_dir, hs_file), encoding="utf-8") as f:
        hs = json.load(f)
        for j in range(10):
            note = hs[j]["note"]
            hot_num_y = hs[j]["hot_num"]
            hot_num_x = [i for i in range(len(hot_num_y))]
            # hot_num_x = [i for i in range(len(hot_num_y))]
            onboard_time = hs[j]["onboard_time"]
            mid = hs[j]["mid"]
            raw_hot = hs[j]["raw_hot"]
            if onboard_time == "" or mid == "" or raw_hot == -1:
                print("广告热搜：{}".format(note))
                continue
            # 先转换为时间数组
            time_array = time.strptime(onboard_time, "%Y-%m-%d %H:%M:%S")
            # 转换为时间戳
            onboard_timestamp = int(time.mktime(time_array))
            end_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                     time.localtime(onboard_timestamp+len(hot_num_x)*COLLECT_INTERVAL))
            # hot_num_x[0] = onboard_time.split(" ")[1]
            # # 先转换为时间数组
            # onboard_time = time.strptime(onboard_time, "%Y-%m-%d %H:%M:%S")
            # # 转换为时间戳
            # onboard_time = int(time.mktime(onboard_time))
            # for i in range(len(hot_num_y)):
            #     hot_num_x.append(time.strftime("%H:%M:%S", time.localtime(onboard_time+i*COLLECT_INTERVAL)))
            fig, ax = plt.subplots()
            # plt.stem(hot_num_x, hot_num_y, label=note)
            ax.plot(hot_num_x, hot_num_y)
            ax.set_ylabel("热度")
            ax.set_xlabel("起始时间：{}, 结束时间：{}, 采样间隔：{}s".format(onboard_time, end_time, COLLECT_INTERVAL))
            ax.set_title("热搜:【{}】热度曲线图".format(note))
            # ax.ticklabel_format(style="plain")
            # ax.legend()
            plt.show()

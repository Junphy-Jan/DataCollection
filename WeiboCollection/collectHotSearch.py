"""
获取微博热搜，微博实时热搜每分钟更新一次
API：https://weibo.com/ajax/statuses/hot_band
每天凌晨3点保存一次到数据库
"""
import json
import time

import ray
import requests

from Collector import Collector
from CommonUtils.constant import HOT_SEARCH_URL
from CommonUtils.loggerHelper import get_logger
from WeiboCollection.HotSearchEntity import HotSearch

main_logger = get_logger("data_collection.log")


@ray.remote
def get_hot_search():
    logger = get_logger("async_weibo_collection.log")
    logger.info("进入get_hot_search。。。")
    print("进入get_hot_search。。。")
    hot_search_list = []
    while True:
        try:
            ret = requests.get(HOT_SEARCH_URL)
            ret_dict: dict = json.loads(ret.text)
            for hs_dict in ret_dict["data"]["band_list"]:
                exist_flag = False
                if len(hot_search_list) > 0:
                    for i in range(len(hot_search_list)):
                        if hs_dict.get("note", "") == hot_search_list[i].note and \
                                hs_dict.get("onboard_time", -1) == hot_search_list[i].onboard_time:
                            hot_search_list[i].set_hot_num(hs_dict.get("num", -1))
                            exist_flag = True
                            break
                if not exist_flag:
                    hs = HotSearch(hs_dict["note"], channel_type=hs_dict.get("channel_type", ""),
                                   category=hs_dict.get("category", ""), rank=hs_dict.get("rank", -1),
                                   link=hs_dict.get("mblog", ""), onboard_time=hs_dict.get("onboard_time", -1),
                                   raw_hot=hs_dict.get("raw_hot", -1), hot_num=hs_dict.get("num", -1),
                                   ad_info=hs_dict.get("ad_info", ""))
                    hot_search_list.append(hs)
        except Exception as e:
            print(e)
        time.sleep(10)
        hs_title = [hs.note + "热度：" + str(hs.hot_num) for hs in hot_search_list]
        logger.info("当前热搜：{}".format(hs_title))


class HotSearchCollector(Collector):
    def __init__(self, name, save_strategy):
        super().__init__(name, save_strategy)

    def run(self):
        main_logger.info("start run:{}".format(self.name))
        get_hot_search.remote()


if __name__ == '__main__':
    hs_c = HotSearchCollector("weibo", "1")
    hs_c.run()
    # hs_c.get_hot_search()
    while True:
        print("running...")
        time.sleep(30)
        break

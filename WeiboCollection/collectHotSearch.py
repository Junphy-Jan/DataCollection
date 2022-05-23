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
from CommonUtils.constant import HOT_SEARCH_URL, WEIBO_SAVED_PATH, WHEN_SAVE2DB
from CommonUtils.loggerHelper import get_logger
from CommonUtils.supportFunc import is_xx_time
from WeiboCollection.HotSearchEntity import HotSearch

main_logger = get_logger("data_collection.log")


@ray.remote
def get_hot_search():
    logger = get_logger("async_weibo_collection.log")
    logger.info("进入get_hot_search。。。")
    print("进入get_hot_search。。。")
    hot_search_list = []
    total_sce = 0
    saved = False
    while True:
        try:
            ret = requests.get(HOT_SEARCH_URL)
            ret_dict: dict = json.loads(ret.text)
            for hs_dict in ret_dict["data"]["band_list"]:
                onboard_time = hs_dict.get("onboard_time", "")
                link = hs_dict.get("mblog", "")
                if onboard_time != "":
                    onboard_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(onboard_time))
                if link != "":
                    link = link["text"]
                
                exist_flag = False
                if len(hot_search_list) > 0:
                    for i in range(len(hot_search_list)):
                        if hs_dict.get("note", "") == hot_search_list[i].note and \
                                hs_dict.get("mid", "") == hot_search_list[i].mid:
                            hot_search_list[i].set_hot_num(hs_dict.get("num", -1))
                            exist_flag = True
                            break
                if not exist_flag:
                    hs = HotSearch(hs_dict.get("mid", ""), hs_dict["note"], channel_type=hs_dict.get("channel_type", ""),
                                   category=hs_dict.get("category", ""), rank=hs_dict.get("rank", -1),
                                   link=link, onboard_time=onboard_time,
                                   raw_hot=hs_dict.get("raw_hot", -1), hot_num=hs_dict.get("num", -1),
                                   ad_info=hs_dict.get("ad_info", ""))
                    hot_search_list.append(hs)
        except Exception as e:
            print(e)
        time.sleep(15)
        total_sce += 15
        hs_title = [hs.note + "热度：" + str(hs.hot_num[:-1]) for hs in hot_search_list]
        if total_sce % 600 == 0:
            logger.info("当前热搜：{}".format(hs_title))
        if is_xx_time(WHEN_SAVE2DB) and not saved:
            saved = True
            with open(WEIBO_SAVED_PATH, "w", encoding="utf-8") as f:
                json.dump([hs.__dict__ for hs in hot_search_list], f, ensure_ascii=False)
            hot_search_list = []
        if not is_xx_time(WHEN_SAVE2DB):
            saved = False
            
            


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

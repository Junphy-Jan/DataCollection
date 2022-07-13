"""
获取微博热搜，微博实时热搜每分钟更新一次
API：https://weibo.com/ajax/statuses/hot_band
每天凌晨3点保存一次到数据库
"""
from curses import raw
import json
import time

import ray
import requests

from Collector import Collector
from CommonUtils.constant import HOT_SEARCH_URL, WEIBO_SAVED_PATH, WHEN_SAVE2DB, COLLECT_INTERVAL
from CommonUtils.loggerHelper import get_logger
from CommonUtils.supportFunc import is_xx_time, get_today_format
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
                mid = hs_dict.get("mid", "")
                onboard_time = hs_dict.get("onboard_time", "")
                link = hs_dict.get("mblog", "")
                raw_hot = hs_dict.get("raw_hot", -1)
                if onboard_time != "":
                    onboard_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(onboard_time))
                # else:
                #     onboard_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                if link != "":
                    link = link["text"]
                
                exist_flag = False
                if len(hot_search_list) > 0:
                    for i in range(len(hot_search_list)):
                        # 热搜存在判断逻辑：如果上榜时间存在，则以note + onboard_time 视为同一个，
                        #                  如果raw_hot存在，以note + raw_hot为准
                        if hs_dict.get("note", "") == hot_search_list[i].note:
                            if onboard_time != "":
                                if onboard_time == hot_search_list[i].onboard_time:
                                    hot_search_list[i].set_hot_num(hs_dict.get("num", -1))
                                    hot_search_list[i].last_update_time = int(time.time())
                                    exist_flag = True
                                    break
                            if raw_hot != -1:
                                if raw_hot == hot_search_list[i].raw_hot:
                                    hot_search_list[i].set_hot_num(hs_dict.get("num", -1))
                                    hot_search_list[i].last_update_time = int(time.time())
                                    exist_flag = True
                                    break
                            # 一般是广告
                            if mid == "" or raw_hot == -1:
                                exist_flag = True
                                break
                                
                if not exist_flag:
                    hs = HotSearch(mid, hs_dict["note"], channel_type=hs_dict.get("channel_type", ""),
                                   category=hs_dict.get("category", ""), rank=hs_dict.get("rank", -1),
                                   link=link, onboard_time=onboard_time,
                                   raw_hot=raw_hot, hot_num=hs_dict.get("num", -1),
                                   ad_info=hs_dict.get("ad_info", ""))
                    hot_search_list.append(hs)
        except Exception as e:
            print(e)
            logger.error("请求热搜异常，e:{}".format(e))
        time.sleep(COLLECT_INTERVAL)
        total_sce += COLLECT_INTERVAL
        hs_title = [hs.note + "-热度：" + str(hs.hot_num[-1]) +
                    "-更新时间：{} || ".format(time.strftime("%Y_%m_%d", time.localtime(hs.last_update_time)))
                    for hs in hot_search_list]
        # 每过10分钟记录一次日志
        if total_sce % 600 == 0:
            logger.info("当前热搜：{}".format(hs_title))
        if is_xx_time(WHEN_SAVE2DB) and not saved:
            saved = True
            cur_hot_search_length = len(hot_search_list)
            now = int(time.time())
            need_save_hs = []
            # 热搜最后更新时间在一天之前的，保存到文件中
            for hs_idx in range(cur_hot_search_length-1, -1, -1):
                if now - hot_search_list[hs_idx].last_update_time >= 60*60*24:
                    need_save_hs.append(hot_search_list[hs_idx])
                    hot_search_list.pop(hs_idx)
            logger.info("当前热搜条数：{}，已保存热搜条数：{}".format(len(hot_search_list), len(need_save_hs)))
            with open(WEIBO_SAVED_PATH.format(get_today_format()), "w", encoding="utf-8") as f:
                json.dump([hs.__dict__ for hs in need_save_hs], f, ensure_ascii=False)
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

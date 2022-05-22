import time

from Collector import Collector
from WeiboCollection.collectHotSearch import HotSearchCollector

collector = Collector()
weibo_hs_collector = HotSearchCollector(name="微博热搜收集器", save_strategy="每天04:00入库")
collector.set_collector(weibo_hs_collector)
while True:
    print("running...")
    collector.run_collect()
    # 1 day
    time.sleep(43200)

# if __name__ == '__main__':
#     collector = Collector()
#     weibo_hs_collector = HotSearchCollector(name="微博热搜收集器", save_strategy="每天04:00入库")
#     collector.set_collector(weibo_hs_collector)
#     collector.run_collect()

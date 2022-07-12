import time

from Collector import Collector
from WeiboCollection.collectHotSearch import HotSearchCollector

collector = Collector()
weibo_hs_collector = HotSearchCollector(name="微博热搜收集器", save_strategy="每天23:59保存")
collector.set_collector(weibo_hs_collector)
while True:
    print("running...")
    collector.run_collect()
    # 1 year
    year = 60*60*24*365
    time.sleep(year)

# if __name__ == '__main__':
#     collector = Collector()
#     weibo_hs_collector = HotSearchCollector(name="微博热搜收集器", save_strategy="每天04:00入库")
#     collector.set_collector(weibo_hs_collector)
#     collector.run_collect()

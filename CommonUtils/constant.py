import os

HOT_SEARCH_URL = "https://weibo.com/ajax/statuses/hot_band"
WHEN_SAVE2DB = "23:59"
# 采集间隔时间(second)
COLLECT_INTERVAL = 30
HOT_SEARCH_FILE_NAME = "hot_search_{}.json"
HOME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEIBO_SAVED_PATH = os.path.join(HOME_DIR, "collected_data/{}".format(HOT_SEARCH_FILE_NAME))

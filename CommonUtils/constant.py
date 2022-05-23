import os

HOT_SEARCH_URL = "https://weibo.com/ajax/statuses/hot_band"
WHEN_SAVE2DB = "00:00"
HOME_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEIBO_SAVED_PATH = os.path.join(HOME_DIR, "collected_data/hot_search.json")

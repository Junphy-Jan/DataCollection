import uuid


class HotSearch:
    def __init__(self, mid, note, channel_type, category, rank, link, onboard_time, raw_hot,
                 hot_num, ad_info):
        self.mid = mid
        self.note = note
        self.channel_type = channel_type
        self.category = category
        self.rank = rank
        self.link = link
        self.onboard_time = onboard_time
        self.raw_hot = raw_hot
        self.hot_num = []
        self.set_hot_num(hot_num)
        self.ad_info = ad_info

    def __eq__(self, other):
        if self.note == other.note and self.mid == other.mid:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.note + self.mid)

    def set_hot_num(self, hot_num):
        self.hot_num.append(hot_num)

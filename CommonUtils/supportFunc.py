import time


def is_xx_time(xx: str):
    """
    判断当前时间是否是 xx 时间，精确到分钟

    :param xx: "%H:%M",e.g. 02:00
    :return:
    """
    time_now = int(time.time())
    time_local = time.localtime(time_now)
    dt = time.strftime("%H:%M", time_local)
    return dt == xx


def get_today_format():
    today = time.strftime("%Y_%m_%d", time.localtime(int(time.time())))
    print(today)
    return today


if __name__ == '__main__':
    print(is_xx_time("19:18"))
    get_today_format()

import abc
import ray


class Collector(object):
    def __init__(self, name=None, save_strategy=None):
        self.name = name
        self.save_strategy = save_strategy
        self.collectors = []

    @abc.abstractmethod
    def run(self):
        return

    def set_collector(self, c):
        self.collectors.append(c)

    def run_collect(self):
        """
        为每个收集器创建一个进程

        :return:
        """
        for c in self.collectors:
            c.run()

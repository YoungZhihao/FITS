from numpy import inf

class Settings:
    def __init__(self):
        self.bandwidth = 1000 # 带宽，单位是bits/μs，换算为1Gbits/s
        self.timeslot = 125 # 设置固定的timeslot
        self.depth_CQF = 16000 # CQF队列深度
        self.linknum = 17 # 链路总数
        self.flownum = 1000 # 流总数
        self.casenum = 2 # 使用的流实例序号
        self.sortmode = ('naive','up') # 排序顺序


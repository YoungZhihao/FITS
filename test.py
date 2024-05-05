""" 测试接口文件 """

from settings import Settings
from main import FITS
from excel import ReadData, WriteRslt

#!-------------------------------------------------
#! 测试函数代码
#!-------------------------------------------------
settings = Settings()

path = './Data/Linear/Linear_{0}_{1}.xls'.format(settings.flownum,settings.casenum)
Length, Period, Bsl, Route, Hops, Deadline = ReadData(path)

print("-"*31+"Data"+"-"*31)
# print("Length: ", Length)
# print("Deadline: ", Deadline)
# print("Period: ", Period)
# print("Baseline: ", Bsl)
# print("Route: ", Route)

Flows = [i for i in range(settings.flownum)]
FITS(Flows, Length, Period, Bsl, Route, Deadline)

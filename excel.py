""" excel文件到python的接口函数 """
import xlrd, xlwt


#!-------------------------------------------------
#!  Read函数代码
#!-------------------------------------------------
def ReadData(path):
    # 从path文件中读取数据
    workbook = xlrd.open_workbook(path)
    sheet = workbook.sheet_by_index(0)
    for i in range(1, sheet.nrows):
        # 获取一组实例数据
        Length, Period, Bsl, Route, Hops, Deadline = sheet.row_values(i, 0, 6)
        Length, Period, Bsl, Route, Hops, Deadline = eval(Length), eval(Period), eval(Bsl), eval(Route), eval(Hops), eval(Deadline)
    return Length, Period, Bsl, Route, Hops, Deadline

#!-------------------------------------------------
#!  Write函数代码，待维护
#!-------------------------------------------------
def WriteRslt(path):
    pass


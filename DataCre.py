""" 流实例生成模块 """
import xlwt
import random
from settings import Settings

settings = Settings()


#!-------------------------------------------------
#! 数据设置区
#! 须同步修改settings.py文件中的self.linknum
#!-------------------------------------------------
file_repeat_num = 5 #重复生成文件数
sample_repeat_num = 1 # 同一个文件中重复样例组数
# flow_num_scale = [10,20,30,40,50,60,100,200,300,400,500,1000] # 每一个样例中流数量种类
flow_num_scale = [1000] # 每一个样例中流数量种类


# 路径设置
L = [ 
    [0,1,2],
    [1,2,3],
    [2,3,4],
    [3,4,5],
    [4,5,6],
    [5,6,7],
    [6,7,8],
    [7,8,9],
    [8,9,10],
    [9,10,11],
    [10,11,12],
    [11,12,13],
    [12,13,14],
    [13,14,15],
    [14,15,16]] # 线性拓扑实例路径
R = [
    [0,1,2],
    [1,2,3],
    [2,3,4],
    [3,4,5],
    [4,5,6],
    [5,6,7],
    [6,7,8],
    [7,8,9],
    [8,9,10],
    [9,10,11],
    [10,11,12],
    [11,12,13],
    [12,13,14],
    [13,14,0],
    [14,0,1]] # 环形拓扑实例路径
T =[
    [0,4,6],
    [1,4,6],
    [2,5,6],
    [3,5,6],
    [7,11,13],
    [8,11,13],
    [9,12,13],
    [10,12,13],
    [14,18,20],
    [15,18,20],
    [16,19,20],
    [17,19,20],
    [21,25,27],
    [22,25,27],
    [23,26,27],
    [24,26,27],
    [28,32,34],
    [29,32,34],
    [30,33,34],
    [31,33,34]] # 树状拓扑实例路径
M = [
    [0, 1, 3],
    [0, 4, 5],
    [1, 2, 3],
    [2, 3, 8],
    [3, 8, 10],
    [4, 5, 1],
    [4, 5, 6],
    [5, 1, 2],
    [5, 6, 2],
    [5, 6, 7],
    [6, 2, 2],
    [6, 7, 3],
    [6, 7, 9],
    [7, 3, 8],
    [7, 9, 10],
    [7, 9, 8],
    [9, 8, 10]] # 混合拓扑实例路径



#!-------------------------------------------------
#! 实例生成代码
#!-------------------------------------------------
for flownum in flow_num_scale:
    for re in range(file_repeat_num):
        path = './Data/Linear/Linear_{0}_{1}.xls'.format(flownum,re)
        book = xlwt.Workbook() # 创建工作簿
        header = [ 'Length', 'Period', 'Bsl', 'Route', 'Hops', 'Deadline' ] # 创建表头
        sheet1 = book.add_sheet(u'%.3d'%(flownum), cell_overwrite_ok = True) # 创建表单
        for j in range(len(header)): # 插入表头
            sheet1.write(0, j, header[j])
        for r in range(1, sample_repeat_num+1): # 按i行j列顺序依次存入表格
            # 生成被测数据集
            Length = [ random.randint(64,1500) for i in range (flownum) ]
            Period = [ int(random.choice([2000,4000,6000,8000,10000])) for i in range(flownum) ]
            Bsl = [ int(random.randint(0, Period[i]))//100 for i in range(flownum) ]
            Hops = [ 3 for i in range(flownum) ]
            Deadline = [ random.randint((Hops[i]+1)*125, (Hops[i]+1)*125+Period[i]) for i in range(flownum) ]
            Route = [ L[i%len(L)] for i in range(flownum) ] # 边(link) ID
            # 写入Excel表格
            data = [Length, Period, Bsl, Route, Hops, Deadline]
            for j in range(len(data)):
                sheet1.write(r, j, str(data[j]))
        book.save(path) #保存文件

        # path = './RingTT/Ring_%s_%s.xls'%(flownum, re)
        # for r in range(1, 1+sample_repeat_num):
        #     Route = [ R[i%15] for i in range(flownum) ] # 边(link) ID
        #     sheet1.write(r, 3, str(Route))
        # book.save(path)

        # path = './TreeTT/Tree_%s_%s.xls'%(flownum, re)
        # for r in range(1, 1+sample_repeat_num):
        #     Route = [ T[i%20] for i in range(flownum) ] # 边(link) ID
        #     sheet1.write(r, 3, str(Route))
        # book.save(path)

        # path = './MeshTT/Mesh_%s_%s.xls'%(flownum, re)
        # for r in range(1, 1+sample_repeat_num):
        #     Route = [ M[i%17] for i in range(flownum) ] # 边(link) ID
        #     sheet1.write(r, 3, str(Route))
        # book.save(path)
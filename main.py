""" FITS代码 """
import time

from functions import GCD, LCM, latency, Resource, UpdateRes, Sort
from settings import Settings


#!-------------------------------------------------
#!  FITS主函数代码
#!-------------------------------------------------
settings = Settings() # 导入配置

def FITS(Flows, Length, Period, Bsl, Route, Deadline):
    Flows = Sort(settings.sortmode, Flows, Length, Period, Deadline) 
    print("Sorting Mode: ", settings.sortmode)
    start_time = time.perf_counter()  # 开始计时

    OFT =[-1 for i in range(len(Flows))]
    Flows_sch = [] # 已经调度的流
    # C_span = GCD(Period) # time_slot大小
    C_span = settings.timeslot
    print("C_span: ", C_span)
    P_span = LCM(Period) # hyper-period大小
    print("P_span: ", P_span)
    print("-"*30+"Result"+"-"*30)
    if C_span==-1 or P_span==-1:
        print("Data Wronging! No data input.")
        exit(0)
    resource = [[0 for i in range(int(P_span/C_span))] for i in range(settings.linknum) ] # 资源列表，表示不同链路上不同时隙中的占用资源

    for flow in Flows:
        oft = -1 # 当前流flow的偏置
        oft_bound = Period[flow]//C_span # 搜索偏置上界，由不超过一个流周期给出
        # print("Offset bound: ", oft_bound)
        max_queue_ocp = settings.depth_CQF+1 # 当前调度流情况下时隙资源最小占用量，随不同偏置改变

        for oft in range(oft_bound):
            # print("deadline: ", Deadline[flow])
            if latency(oft,C_span,Bsl[flow],Route[flow])<=Deadline[flow]:
                max_queue_ocp_temp = Resource(flow,Flows_sch,Length,Period,Bsl,Route,OFT,C_span,P_span,oft,settings.linknum)
                # print("max_queue_ocp_temp: ", max_queue_ocp_temp)
                if max_queue_ocp_temp < max_queue_ocp:
                    OFT[flow] = oft
                    max_queue_ocp = max_queue_ocp_temp
                    if max_queue_ocp > min(settings.depth_CQF, settings.bandwidth*settings.timeslot): # 溢出
                        print("Queues/Bandwidth Overflow!")
                        max_queue_ocp = -1
                        break
            elif OFT[flow] == -1: # 未调度直接时延溢出
                max_queue_ocp = -1 # 调度失败，最大占用量记为-1
                break # 均无法调度，调度失败
            else: # 已经调度过进入时延要求的偏置范围外
                break
        # print("max_queue_ocp: ", max_queue_ocp)
        if max_queue_ocp == -1: # 因为CQF队列溢出或者有流不满足时延要求，无法调度
            break
        else:
            resource = UpdateRes(resource,Length[flow],Period[flow],Bsl[flow],Route[flow],OFT[flow],C_span,P_span)
            # print("resource: ", resource)
            Flows_sch.append(flow) # 更新已调度流
            print("Flow {} scheduled successfully!".format(flow))
            # print("OFT[]: ", OFT)
    
    end_time = time.perf_counter()  # 终止计时
    Runtime = end_time - start_time

    if max_queue_ocp == -1:
        print("Scheduled Failed!")
    else:
        print("Runtime:      "+str(Runtime))
        print("MaxSlot:      "+str(max_queue_ocp))
        # print("resource: ", resource)
        # print("Load Balance: "+str(max_queue_ocp/(settings.bandwidth*C_span)))


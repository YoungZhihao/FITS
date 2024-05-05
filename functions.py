""" 所有用到的functions """
from math import lcm, gcd



#!-------------------------------------------------
#!  GCD函数代码
#!-------------------------------------------------
def GCD(sample_list):
    # 返回一个数值列表中所有元素的gcd
    if len(sample_list) == 0:
        gcd_value = -1
    elif len(sample_list) == 1:
        gcd_value = sample_list[0]
    else:
        gcd_value = sample_list[0]
        for sample_ele in sample_list[1:]:
            gcd_value = gcd(gcd_value,sample_ele)
    return gcd_value

#!-------------------------------------------------
#!  LCM函数代码
#!-------------------------------------------------
def LCM(sample_list):
    # 返回一个数值列表中所有元素的gcd
    if len(sample_list) == 0:
        lcm_value = -1
    elif len(sample_list) == 1:
        lcm_value = sample_list[0]
    else:
        lcm_value = sample_list[0]
        for sample_ele in sample_list[1:]:
            lcm_value = lcm(lcm_value,sample_ele)
    return lcm_value

#!-------------------------------------------------
#!  latency函数代码
#!-------------------------------------------------
def latency(oft,C_span,bsl,route):
    # 计算当前偏置下最坏总时延
    latency_value = bsl + (len(route)+oft)*C_span
    # print("latency: ", latency_value)
    return latency_value

#!-------------------------------------------------
#!  Resource函数代码
#!-------------------------------------------------
def Resource(flow_now,Flows_sch,Length,Period,Bsl,Route,OFT,C_span,P_span,oft,link_num):
    # 计算当前时隙资源占用量最大值
    resource = [[0 for i in range(P_span//C_span)] for j in range(link_num) ]
    max_queue_ocp = 0 # 最大占用量
    for flow in Flows_sch:
        cycle_num = (P_span-Bsl[flow]-OFT[flow]*C_span-len(Route[flow])*C_span)//Period[flow]+1 # 一个hyper-period里可容纳的周期数
        for num,route in enumerate(Route[flow]):
            for cycle in range(cycle_num):
                resource[route][(cycle*Period[flow]+Bsl[flow])//C_span+OFT[flow]+num] += Length[flow]
    for num,route in enumerate(Route[flow_now]):
        cycle_num = (P_span-Bsl[flow_now]-oft*C_span-len(Route[flow_now])*C_span)//Period[flow_now]+1 # 一个hyper-period里可容纳的周期数
        for cycle in range(cycle_num):
            resource[route][(cycle*Period[flow_now]+Bsl[flow_now])//C_span+oft+num] += Length[flow_now]
    # print("resource: ", resource)
    max_queue_ocp = max(map(max,resource)) # 找到所有链路在所有时隙中的最大值
    
    return max_queue_ocp

#!-------------------------------------------------
#!  UpdateRes函数代码
#!-------------------------------------------------
def UpdateRes(resource,length,period,bsl,route,oft,C_span,P_span):
    # 针对流flow进行时隙资源列表resource的更新
    cycle_num = (P_span-bsl-oft*C_span-len(route)*C_span)//period+1 # 一个hyper-period里可容纳的周期数
    for num,link in enumerate(route):    
        for cycle in range(cycle_num):
            resource[link][cycle*period//C_span+oft+num+bsl//C_span] += length
    return resource

#!-------------------------------------------------
#!  Sort函数代码
#!-------------------------------------------------
def Sort(sortmode, sample_list, Length, Period, Deadline):
    if sortmode[0] == 'naive':
        queue = [[sample_list[i], None] for i in range(len(sample_list))]
    elif sortmode[0] == 'length':
        queue = [[sample_list[i], Length[i]] for i in range(len(sample_list))]
        if sortmode[1] == 'up': # 正序
            queue.sort(key=lambda x:x[1])
        elif sortmode[1] == 'down':
            queue.sort(key=lambda x:x[1],reverse=True)
    elif sortmode[0] == 'period':
        queue = [[sample_list[i], Period[i]] for i in range(len(sample_list))]
        if sortmode[1] == 'up': # 正序
            queue.sort(key=lambda x:x[1])
        elif sortmode[1] == 'down':
            queue.sort(key=lambda x:x[1],reverse=True)
    elif sortmode[0] == 'deadline':
        queue = [[sample_list[i], Deadline[i]] for i in range(len(sample_list))]
        if sortmode[1] == 'up': # 正序
            queue.sort(key=lambda x:x[1])
        elif sortmode[1] == 'down':
            queue.sort(key=lambda x:x[1],reverse=True)
    else:
        print("Sortmode Wrong! No choice named "+ str(sortmode))
        exit(0)

    return [queue[i][0] for i in range(len(queue))]
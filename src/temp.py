#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
##-------- [PPC]  Jobshop Scheduling ---------
# * Author: Colin, Lee
# * Date: Apr 30th, 2020
# * Description:
#       Using the event-driven scheuling method
#       to solve the JSS prob. Here is a sample
#       code with the style of OOP. Feel free to
#       modify it as you like.
##--------------------------------------------
#

import os
import numpy as np
import pandas as pd
from gantt_plot import Gantt

#entity
class Order:
    def __init__(self, ID, AT, DD, routing, PT):
        self.ID   = ID
        self.AT    = AT         #AT: arrival time
        self.DD    = DD         #DD: due date

        self.PT       = PT      #PT: processing time
        self.routing  = routing
        self.progress = 0

#resource in factory
class Source:
    def __init__(self, order_info):
        self.order_info = order_info
        self.output = 0

    def arrival_event(self, fac):
        raise NotImplementedError

class Machine:
    def __init__(self, ID, DP_rule):
        self.ID     = ID
        self.state  = 'idle'
        self.buffer = []
        self.wspace = [] #wspace: working space
        self.DP_rule = DP_rule

    def start_processing(self, fac):
        raise NotImplementedError

    def end_process_event(self, fac):
        raise NotImplementedError

class Factory:
    def __init__(self, order_info, DP_rule):
        self.order_info = order_info
        self.DP_rule    = DP_rule
        self.event_lst = pd.DataFrame(columns=["event_type", "time"])

        #statistics
        self.throughput = 0
        self.order_statistic = pd.DataFrame(columns = ["ID", "release_time",
                                                       "complete_time", "due_date",
                                                       "flow_time", "lateness",
                                                       "tardiness"])
        #[Plug in] tool of gantt plotting
        self.gantt_plot = Gantt()

        #build ur custom factory
        self.__build__()

    def __build__(self):
        raise NotImplementedError

    def initialize(self, order_info):
        raise NotImplementedError

    def next_event(self, stop_time):
        raise NotImplementedError

    def event(self, event_type):
        raise NotImplementedError

    def update_order_statistic(self, order):
        raise NotImplementedError

# some parameters
M = float('inf')
LOG = True
stop_time = 500

if __name__ == '__main__':
    #read the input data sheet
    data_dir = os.getcwd() + "/data/"
    order_info = pd.read_excel(data_dir + "order_information.xlsx")

    #data preprocessing
    order_info = order_info.sort_values(['arrival_time']).reset_index(drop=True)

    DP_rule = 'SPT' #'EDD'

    #build the factory
    fac = Factory(order_info, DP_rule)
    fac.build()

    #start the simulation
    fac.next_event(stop_time)

    #output result
    print(fac.order_statistic)
    fac.gantt_plot.draw_gantt()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
##------ [PPC] Simple Jobshop Scheduling ----
# * Author: Colin, Lee
# * Date: Apr 20th, 2020
##-------------------------------------------
#

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from gantt_plot import gantt

#entity
class Order:
    def __init__(self, ID, jtype, AT, DD, routing, PT):
        self.ID   = ID
        self.jype = jtype
        self.AT    = AT    #AT: arrival time
        self.DD    = DD    #DD: due date
        self.CT    = None    #CT: complete time

        self.PT       = PT
        self.routing  = routing
        self.progress = 0

#resource in factory
class Buffer:
    def __init__(self, ID, DP_rule):
        self.ID      = ID
        self.space   = []
        self.DP_rule = DP_rule

class Machine:
    def __init__(self, ID):
        self.ID     = ID
        self.state  = 'idle'
        self.buffer = []
        self.wspace = [] #wspace: working space

    def job_arrival(self):
        raise NotImplementedError
        
    def start_process(self):
        raise NotImplementedError

    def end_process(self):
        raise NotImplementedError

class Factory:
    def __init__(self, job_info):
        self.job_info = job_info
        self.output = 0

    def job_arrival():
        raise NotImplementedError


if __name__ == '__main__':

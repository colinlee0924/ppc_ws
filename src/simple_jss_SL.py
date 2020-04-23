#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
##------ [PPC] Simple JSS simulation  -------
# * Author: Colin, Lee
# * Date: Apr 20th, 2020
##-------------------------------------------
#

def arrival_event():
    raise NotImplementedError

def start_process_event():
    raise NotImplementedError

def end_process_event():
    raise NotImplementedError

def event(event_type):
    if event_type == 'A':
        arrival_event()
    else:
        end_process_event()
    print_trace()

def print_trace():
    raise NotImplementedError



if __name__ == '__main__':
    T_NOW = 0
    TOA = None #time of arrival
    TOPC = None #time of processing complete

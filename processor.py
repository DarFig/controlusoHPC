# -*- coding: utf-8 -*-

from utils import work_data

def get_group_usage(group:str, data:list)->dict:
    group_jobduration = 0.0
    uc = 0.0
    uch = 0.0
    for work in data:
        work = work_data(work)
        if __get_group(work) == group:
            group_jobduration += __get_jobduration(work)
            uc += __get_requestcpus(work)
    
    hours = __s_h(group_jobduration)
    uch = hours * uc
    return {"time":hours, "uc":uc, "uch":uch}


## priv

def __get_jobduration(work:list)->float:
    return work["JobDuration"]

def __get_group(work:list)->str:
    return work["group"]

def __get_requestcpus(work:list)->int:
    return work["RequestCpus"]

def __get_startdname(work:list)->str:
    return work["StartdName"]

def __s_h(jobduration:float)->float:
    """
    seconds to hours
    """
    return jobduration/3600

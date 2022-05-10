# -*- coding: utf-8 -*-

from utils import work_data, load_uc_json
from loadconfig import get_use_uc_conversion


def get_group_usage(group:str, data:list)->dict:
    """
    group,data[works] -> return {"time":hours, "uc":uc, "uch":uch}
    """
    group_jobduration = 0.0
    uc = 0.0
    uch = 0.0
    for work in data:
        work = work_data(work)
        if __get_group(work) == group:
            group_jobduration += __get_jobduration(work)
            uc += __get_uc(work)
    
    hours = __s_h(group_jobduration)
    uch = hours * uc
    return {"time":hours, "uc":uc, "uch":uch}

def get_user_usage(user:str, data:list)->dict:
    """
    user,data[works] -> return {"time":hours, "uc":uc, "uch":uch}
    """
    user_jobduration = 0.0
    uc = 0.0
    uch = 0.0
    for work in data:
        work = work_data(work)
        if __get_owner(work) == user:
            user_jobduration += __get_jobduration(work)
            uc += __get_uc(work)
    hours = __s_h(user_jobduration)
    uch = hours * uc
    return {"time":hours, "uc":uc, "uch":uch}


def get_groups(data:list)->set:
    groups = set()
    for work in data:
        work = work_data(work)
        groups.add(__get_group(work))

    return groups



## priv

def __get_jobduration(work:list)->float:
    return work["JobDuration"]

def __get_group(work:list)->str:
    return work["group"]

def __get_owner(work:list)->str:
    return work["Owner"]

def __get_uc(work:list)->float:
    cpus = __get_requestcpus(work)
    return cpus * __uc_conversion(__get_startdname(work))


def __get_requestcpus(work:list)->int:
    return work["RequestCpus"]

def __get_startdname(work:list)->str:
    return work["StartdName"]

def __s_h(jobduration:float)->float:
    """
    seconds to hours
    """
    return jobduration/3600

def __uc_conversion(node:str)->float:
    conversion = load_uc_json()
    if get_use_uc_conversion() != 0:
        for key in conversion:
            if key in node:
                return conversion[key]
    return 1.0


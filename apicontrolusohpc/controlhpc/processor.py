# -*- coding: utf-8 -*-

from apicontrolusohpc.controlhpc.utils import work_data, load_uc_json
from apicontrolusohpc.controlhpc.loadconfig import get_use_uc_conversion



def get_groups_usages(data:list)->list:
    groups = get_groups(data)
    groups_usages = {}
    for group in groups:
        groups_usages[group] = get_group_usage(group,data)
    return groups_usages

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

def get_group_users_usage(group:str, data:list)->list:
    usuarios = {}
    for work in data:
        work = work_data(work)
        if __get_group(work) == group:
            owner = __get_owner(work)
            if owner not in usuarios:
                usuarios[owner] = get_user_usage(owner,data)

    return usuarios 



def get_groups(data:list)->set:
    groups = set()
    for work in data:
        work = work_data(work)
        groups.add(__get_group(work))

    return groups



## priv

def __get_jobduration(work:list)->float:
    try:
        return work["JobDuration"]
    except:
        return 0.0

def __get_group(work:list)->str:
    return work["group"]

def __get_owner(work:list)->str:
    return work["Owner"]

def __get_uc(work:list)->float:
    # si es más que 2 machacamos con el valor que viene
    uc = __uc_conversion(__get_startdname(work))
    if uc > 2:
        return uc
    cpus = __get_requestcpus(work)
    return cpus * uc


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
                #print("1-",key," ",node," = ",conversion[key])
                return conversion[key]
    return 1.0


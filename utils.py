# -*- coding: utf-8 -*-

from datetime import datetime

def get_timestamp(date:str)->int:
    """
    from date return timestamp
    input: date string format %d/%m/%Y 
    output: timestamp int 
    """
    date = datetime.strptime(date, "%d/%m/%Y")
    timestamp = datetime.timestamp(date)
    return int(timestamp)

def data_hits(data:dict)->list:
    return data["hits"]["hits"]

def work_data(work:list)->list:
    return work["_source"]



# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from apicontrolusohpc.controlhpc.loadconfig import * 
from apicontrolusohpc.controlhpc.utils import get_timestamp, data_hits
import threading

class Controller:
    def __init__(self):
        self.__CONFIGFILE="service.config"
        self.__HOST = "http://"+ get_hostname()+ ":" + get_port()
        self.__INDEX = get_index()
        self.client = Elasticsearch(self.__HOST)
        self.groups_data = {}
    
    def match_all(self):
        return self.client.search(index=self.__INDEX, query={"match_all": {} })

    def match_date_range(self,initial_date:str, final_date:str,group:str)->dict:
        """
        input:
            initial_date: string format %d/%m/%Y
            final_date: string format %d/%m/%Y
            group: string group name
        output: dict data-json 
        """
        all_data = []
        data = self.client.search(index=self.__INDEX,size=10000,scroll="2m",_source=["group","Owner","JobDuration","RemoteWallClockTime","UserLog","RequestCpus","StartdName"],query={"bool":{"must":[{"match":{"group":group}},{"match":{"Status":"Completed"}},{"range":{"RecordTime":{"gte":get_timestamp(initial_date),"lte":get_timestamp(final_date)}}}]}})
        scroll_id = data['_scroll_id']
        data = data_hits(data)
        scroll_size = len(data)
        all_data = all_data + data
        while scroll_size > 0:
            data = self.client.scroll(scroll_id=scroll_id,scroll="2m")
            scroll_id = data['_scroll_id']
            data = data_hits(data)
            scroll_size = len(data)
            all_data = all_data + data
        self.client.clear_scroll(scroll_id=scroll_id)
        return all_data
    
    def get_groups_names(self)->set:
        _groups = self.client.search(index=self.__INDEX,query={"match_all":{}},aggs={"must" : {"terms" : { "field" : "group", "size":100000 }}},size=0)["aggregations"]["must"]["buckets"]
        groups = set()
        for element in _groups:
            if element["key"] != "ROOT":
                groups.add(element["key"])
        return groups

    def get_group_users(self, group)->set:
        _users = self.client.search(index=self.__INDEX,query={"bool":{"must":[{"match":{"group":group}}]}},aggs={"must" : {"terms" : { "field" : "Owner", "size":100000}}},size=0)["aggregations"]["must"]["buckets"]
        users = set()
        for element in _users:
            users.add(element["key"])
        return users

    def match_all_groups_date_range(self,initial_date:str, final_date:str, groups:set)->dict:
        """
        input:
            initial_date: string format %d/%m/%Y
            final_date: string format %d/%m/%Y
            groups: set strings
        output: dict data-json
        """
        # busco los grupos que existen
        self.groups_data = {}
        
        # vamos a separar las busquedas en hilos
        def hilo(initial_date, final_date,group):
            data_hilo = self.match_date_range(initial_date, final_date, group)
            self.groups_data[group] = data_hilo
        
        hilos = list()
        for group in groups:
            # cada hilo busca un grupo
            t = threading.Thread(target=hilo,args=(initial_date, final_date,group))
            hilos.append(t)
            t.start()
        
        for i in hilos:
            i.join()
        
        return self.groups_data    

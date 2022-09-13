# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from apicontrolusohpc.controlhpc.loadconfig import * 
from apicontrolusohpc.controlhpc.utils import get_timestamp, data_hits


class Controller:
    def __init__(self):
        self.__CONFIGFILE="service.config"
        self.__HOST = "http://"+ get_hostname()+ ":" + get_port()
        self.__INDEX = get_index()
        self.client = Elasticsearch(self.__HOST)
    
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
        #return data_hits(self.client.search(index=self.__INDEX,size=100000,scroll="1m",query={"range":{"RecordTime":{"gte":get_timestamp(initial_date),"lte":get_timestamp(final_date)}}}))
        return data_hits(self.client.search(index=self.__INDEX,size=100000,scroll="1m",query={"bool":{"must":[{"match":{"group":group}},{"range":{"RecordTime":{"gte":get_timestamp(initial_date),"lte":get_timestamp(final_date)}}}]}}))
    
    def match_all_groups_date_range(self,initial_date:str, final_date:str)->dict:
        """
        input:
            initial_date: string format %d/%m/%Y
            final_date: string format %d/%m/%Y
        output: dict data-json
        """
        groups = self.client.search(index=self.__INDEX,query={"match_all":{}},aggs={"must" : {"terms" : { "field" : "group", "size":100000 }}},size=0)["aggregations"]["must"]["buckets"]
        groups_data = []
        for element in groups:
            group = element["key"]
            if group != "ROOT":
                groups_data = groups_data + self.match_date_range(initial_date, final_date, group)
        #print(groups_data)
        return groups_data    

# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from loadconfig import * 
from utils import get_timestamp, data_hits


class Controller:
    def __init__(self):
        self.__HOST = "http://"+ get_hostname()+ ":" + get_port()
        self.__INDEX = get_index()
        self.client = Elasticsearch(self.__HOST)
    
    def match_all(self):
        return self.client.search(index=self.__INDEX, query={"match_all": {} })

    def match_date_range(self,initial_date:str, final_date:str)->dict:
        """
        input:
            initial_date: string format %d/%m/%Y
            final_date: string format %d/%m/%Y
        output: dict data-json 
        """
        return data_hits(self.client.search(index=self.__INDEX,query={"range":{"RecordTime":{"gte":get_timestamp(initial_date),"lte":get_timestamp(final_date)}}}))

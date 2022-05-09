# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from loadconfig import * 



class Controller:
    def __init__(self):
        self.__HOST = "http://"+ get_hostname()+ ":" + get_port() 
        self.client = Elasticsearch(self.__HOST)

    def match_all(self):
        return client.search(index=get_index(), query={"match_all": {} })



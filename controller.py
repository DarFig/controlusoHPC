# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from loadconfig import * 

__HOST = "http://"+ get_hostname()+ ":" + get_port() 

client = Elasticsearch(__HOST)

res = client.search(index=get_index(), query={"match_all": {} })

print(res)

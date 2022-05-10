# -*- coding: utf-8 -*-

from controller import Controller
from processor import *
from utils import load_uc_json

import pprint

pp = pprint.PrettyPrinter(indent=4)

if __name__ == "__main__":
    new_controller = Controller()

    #print(new_controller.match_all())
    data = new_controller.match_date_range("09/05/2022","10/05/2022")
    #pp.pprint(data[0])
    

    #total_JobDuration = 0.0
    #groups = get_groups(data)
    #for group in groups:
    #    print("|||---------------------|||")
    #    pp.pprint(get_group_usage(group,data)) 
    #    print("-----------------")
    #    pp.pprint(get_group_users_usage(group,data))


    pp.pprint(get_groups_usages(data))

            

# -*- coding: utf-8 -*-

import ldap, re

from apicontrolusohpc.controlhpc.loadconfig import get_ldap_server, get_base_dn, get_user_dn




def authentication(username:str, password:str)->str:
    ldap_server = get_ldap_server()
    print(ldap_server) 
    user_dn = "uid="+username+get_user_dn()
    print(user_dn)
    base_dn = get_base_dn()
    print(base_dn)
    connect = ldap.initialize(ldap_server)
    search_filter = "uid="+username
 
    try:
        connect.bind_s(user_dn, password)
        result = connect.search_s(base_dn,ldap.SCOPE_SUBTREE,search_filter)
        connect.unbind_s()
        return result
   
    except:
        connect.unbind_s()
        return "error"


def search_group(user_data:str)->str:
    #return user_data[0][1]["ou"][0]
    #group = re.split("-", str(user_data[0][1]["ou"][0]))[1].strip("\'").strip()
    group = ""
    if not group:
        group = re.split("/", str(user_data[0][1]["homeDirectory"][0]))[2].strip("\'").strip().upper()
        #re.search("home\/*\/", user_data)
    
    return group

def get_messages():
    import json
    try:
        f = open('messages.config', "r")
        data = json.loads(f.read())
        f.close()
        return data
    except:
        return None


def fix_group(group:str)->str:
    import json
    try:
        f = open('fixedgroups.config', "r")
        data = json.loads(f.read())
        f.close()
        if group in data:
            print(group, " - ", data)
            group = data[group]
            print(group)
        return group
    except:
        return group


def normalize_group(group:str)->str:
    import json
    try:
        f = open('normalizedgroups.config', "r")
        data = json.loads(f.read())
        f.close()
        if group in data:
            print(group, " x ", data)
            group = data[group]
            print(group)
        return group
    except:
        return group

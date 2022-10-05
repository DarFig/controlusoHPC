# -*- coding: utf-8 -*-

import ldap, re

from apicontrolusohpc.controlhpc.loadconfig import get_ldap_server, get_base_dn, get_user_dn





def authentication(username:str, password:str)->str:
    ldap_server = get_ldap_server()
    user_dn = "uid="+username+get_user_dn()
    base_dn = get_base_dn()
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
    group = re.split("-", str(user_data[0][1]["ou"][0]))[1].strip("\'").strip()
    if not group:
        group = re.split("/", str(user_data[0][1]["homeDirectory"][0]))[2].strip("\'").strip().upper() 
    return group

def get_messages():
    return messages

def fix_group(group:str)->str:
    if group in fixedgroups:
        return fixedgroups[group]
    return group

def normalize_group(group:str)->str:
    if group in normalizedgroups:
        return normalizedgroups[group]
    
    return group

def __get_messages():
    import json
    try:
        f = open('messages.config', "r")
        data = json.loads(f.read())
        f.close()
        return data
    except:
        return None


def __fix_group():
    import json
    try:
        f = open('fixedgroups.config', "r")
        data = json.loads(f.read())
        f.close()
        #if group in data:
        #    group = data[group]
        #return group
        return data
    except:
        #return group
        return data


def __normalize_group():
    import json
    try:
        f = open('normalizedgroups.config', "r")
        data = json.loads(f.read())
        f.close()
        #if group in data:
        #    group = data[group]
        #return group
        return data
    except:
        #return group
        return data

messages = __get_messages()
fixedgroups = __fix_group()
normalizedgroups = __normalize_group()

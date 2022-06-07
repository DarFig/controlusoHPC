# -*- coding: utf-8 -*-
from apicontrolusohpc.utils import *

user_data = authentication("", "")

if user_data == "error":
    print(user_data)


group = search_group(user_data)

print(group)

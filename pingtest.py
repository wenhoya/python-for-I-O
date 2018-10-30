# -*- coding: utf-8 -*-
import time, re, sys, os, subprocess,inspect
from my_tool import *
ping_check_host = "192.168.1.1"
ping_fail=is_ping_fail(ping_check_host)
if ping_fail :
    print(ping_check_host,"Ping Fail")

print("=============")
os.system("ipconfig/flushdns ")
p = subprocess.Popen("ping "+ ping_check_host, stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
print (output.decode("unicode_escape"))

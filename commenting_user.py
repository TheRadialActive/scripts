#!/usr/bin/python
#        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#                    Version 2, December 2004 
#
# Copyright (C) 2015 Rune Albut <etwas@runealbut.de> 
#
# Everyone is permitted to copy and distribute verbatim or modified 
# copies of this license document, and changing it is allowed as long 
# as the name is changed. 
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.

import json
import requests
import socket
import sys
import datetime

# install
# pip install requests
# use
# python commenting_user.py | sort -u

if sys.argv[1]:
    url_d = sys.argv[1]
else:
    print("Error: Please enter a valid url as argument for the script!")

try:
    print("Get post link on author's pod")
    url_d_post = url_d + ".json"

    r_post = requests.get(url_d_post, verify=True)  

    users_list = []
    
    post_author = r_post.json()['author']['diaspora_id']
    main_pod = post_author[post_author.find("@")+1:]
    post_guid = r_post.json()['guid']
    main_pod_link = "https://" + main_pod + '/posts/' + post_guid

    print("Get the comments from the main pod")
    url_d_comments = main_pod_link + "/comments.json"
    r_comment = requests.get(url_d_comments, verify=True)

    for item in r_comment.json():
        users_list.append("* ["+item['author']['name'] +" "+item['author']['diaspora_id'] +"](/people/"+ item['author']['guid'] +")"  + "    ")

    users_list = list(set(users_list))
    users_list.sort()

    print("--- Markdown-Code ---")
    for user in users_list:
        print(user)
    
    print(str(len(users_list)) + " contacts")
    print(datetime.date.today())

except requests.exceptions.Timeout:

    print("Time out ")

except socket.timeout:

    print("socket Time out ")

except socket.error:

    print("socket error ")

except requests.exceptions.ConnectionError:

    print("Connection Error ")

except requests.exceptions.HTTPError:

    print ("HTTP Error ")

except requests.exceptions.RequestException:

    print("requests.exceptions.RequestException ")

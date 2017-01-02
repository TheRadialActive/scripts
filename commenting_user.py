#!/usr/bin/python

import json
import requests
import socket
import sys
from datetime import datetime

# install
# pip install requests
# use
# python commenting_user.py | sort -u

# Usage:
# run the script and define the post link 

if len(sys.argv) == 2:
    url_d = sys.argv[1]
else:
    sys.exit("ERROR: Please enter a valid diaspora* post link in quotation marks.")

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
    users_list.sort(key=str.lower)

    print("--- Markdown-Code ---")
    for user in users_list:
        print(user)

    users_list_len = str(len(users_list))
    ex_date = datetime.now().strftime('%d.%m.%Y %H:%M')
    print(users_list_len + " contacts commented until " + ex_date)

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

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
    post_request = requests.get(url_d_post, verify=True)  
    
    post_author = post_request.json()['author']['diaspora_id']
    main_pod = post_author[post_author.find("@")+1:]
    post_guid = post_request.json()['guid']
    main_pod_link = "https://" + main_pod + '/posts/' + post_guid

    print("Get the comments from the main pod")
    print("For url: " + main_pod_link)
    url_d_comments = main_pod_link + "/comments.json"
    comment_request = requests.get(url_d_comments, verify=True)

    users_list_name = []
    for item in comment_request.json():
        users_list_name.append("["+item['author']['name'] +" ("+item['author']['diaspora_id'] +")](/people/"+ item['author']['guid'] +")")
    
    print("\n--- Comment Top List ---\n")
    user_num = []
    sum_comments = 0
    for user in set(users_list_name):
        user_num.append([user, users_list_name.count(user)])
    user_num.sort(key=lambda tup: tup[1], reverse=True)

    comments_list_md = []
    for item in user_num:
        item_comment_number = str(item[1])
        item_discussion_share = str(round(float(item[1])/len(users_list_name)*100, 2))
        item_user = str(item[0])
        comments_list_md.append("|" + item_comment_number + "|" + item_discussion_share + "%|" + item_user + "|")
        sum_comments += item[1]

    user_sum = str(len(user_num))
    print("|Number of Comments (" + str(sum_comments) + ") |Share of Discussion (100%) |User (" + user_sum + ") |\n| ---:| ---:|--|")
    for line in comments_list_md:
        print(line)

    users_list_len = str(len(users_list_name))
    execution_date = datetime.now().strftime('%d.%m.%Y %H:%M')
    print("As at " +  execution_date)

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

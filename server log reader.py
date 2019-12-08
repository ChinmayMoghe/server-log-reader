import os.path
from collections import OrderedDict
from operator import getitem
good_path_array = []
blacklisted_ip_list = []
ip_request_map = {}

def create_good_path_filter():
    try:
        good_paths = open("goodPaths.txt")
        for path in good_paths:
            good_path_array.append(path.rstrip('\n'))
        good_paths.close()
    except Exception as e:
        print(e)

def create_blacklist_ip_filter():
    try:
        blacklisted_ip = open('blacklisted_ip.txt','r')
        for ip in blacklisted_ip:
            blacklisted_ip_list.append(ip.rstrip('\n'))
        blacklisted_ip.close()
    except Exception as e:
        print(e)

def create_ip_request_map(log_arr):
    ip = log_arr[0]
    path = log_arr[2]
    request_time = log_arr[3].rstrip('ms')
    if log_arr[0] in ip_request_map:
        ip_obj = ip_request_map[ip]
        ip_obj['count'] += 1
        if(path not in ip_obj['requests']):
            ip_obj['requests'].append(path)
        if(request_time not in ip_obj['request_times']):
            ip_obj['request_times'].append(request_time)
            ip_obj['max_request_time'] = max(ip_obj['request_times'])
    else:
        ip_request_map[ip] = {'count':1,'requests':[path],'request_times':[request_time],'max_request_time':request_time}

def find_top_ten_requesters():
    ordered_request_map = OrderedDict(sorted(ip_request_map.items(),key=lambda x:getitem(x[1],'count'),reverse=True))
    print("\n----Top 10 requester IPs----")
    print("{0} {1}".format("IP".rjust(6),"Request counts".rjust(30)))
    for i,(key,value) in enumerate(ordered_request_map.items()):
            if(i<=9):
                print("{2:2}. {0:15} {1:4}".format(key,value['count'],i))
            else:
                return

def add_to_blacklist(ip):
    ip = ip +'\n';
    if(os.path.exists('blacklisted_ip.txt')):
        blacklist = open('blacklisted_ip.txt','r+')
        if ip in blacklist.read():
            blacklist.close()
        else:
            blacklist.write(ip)
    else:
        blacklist = open('blacklisted_ip.txt','w')
        blacklist.write(ip)
        blacklist.close()

def check_path_requests(ip,path):
    if(path not in good_path_array):
        add_to_blacklist(ip)

def print_blacklist_ip():
    print('\n----Blacklisted IP list----')
    for ip in blacklisted_ip_list:
        print(ip)

def process_log(log):
    log_arr = log.rstrip('\n').split(' ');
    # 0 - ip address , 1- method ,2 - path, 3- request completion time
    ip = log_arr[0]
    path = log_arr[2]
    request_time = log_arr[3].rstrip('ms')
    if(float(request_time)>= 50):
        add_to_blacklist(log_arr[0])
    elif(ip not in blacklisted_ip_list):
        create_ip_request_map(log_arr)
    check_path_requests(ip,path)

def process_server_log():
    try:
        create_good_path_filter()
        if(os.path.exists('blacklisted_ip.txt')):
            create_blacklist_ip_filter()
        server_log = open("log.txt","r")
        for log in server_log:
            process_log(log)
        server_log.close()
    except Exception as e:
        print(e)

process_server_log()
find_top_ten_requesters()
print_blacklist_ip()
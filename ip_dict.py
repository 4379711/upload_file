# -*- coding:utf-8 -*-
import os
import re

clear_hosts = re.compile("\n| |,|")
DEFAULT_PATH_00 = r"C:\file_uploads"
DEFAULT_PATH_01 = r"D:\file_uploads"
DEFAULT_PATH_02 = r"D:\file_uploads\Dist"
DEFAULT_PATH_dict = {"us": DEFAULT_PATH_00, "uk": DEFAULT_PATH_01, "jp": DEFAULT_PATH_02}

# 特殊的ip/域名,指定特殊的路径,就放在这里
special_path = {
    # "127.0.0.1": DEFAULT_PATH_dict,
}


# 清理文件中的特殊符号
def replace_(host_str):
    tmp = clear_hosts.sub('', host_str)
    return tmp


# 读取hosts.txt中配置的域名
file_host = []
if os.path.exists("hosts.txt"):
    with open("hosts.txt", 'r') as f:
        file_host = f.readlines()

ips_dict = {}.fromkeys(map(replace_, file_host), DEFAULT_PATH_dict)
ips_dict.update(special_path)
# print(ips_dict)

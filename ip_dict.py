# -*- coding:utf-8 -*-

DEFAULT_PATH = r"C:\file_uploads"
DEFAULT_PATH_dict = {"us": DEFAULT_PATH, "uk": DEFAULT_PATH, "jp": DEFAULT_PATH}

special_path = {
    # "127.0.0.1": DEFAULT_PATH_dict,
}

all_hosts_by_default_path = {"elecsport.amzbsr.top", 'b', 'c'}

ips_dict = {}.fromkeys(all_hosts_by_default_path, DEFAULT_PATH_dict)
ips_dict.update(special_path)

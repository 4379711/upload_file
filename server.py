# -*- coding:utf-8 -*-
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
import os


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass


# 供客户端上传文件
def file_put(get_file_name, data):
    path = os.path.dirname(get_file_name)
    os.makedirs(path, exist_ok=True)
    with open(get_file_name, 'wb') as handle:
        handle.write(data.data)


if __name__ == '__main__':
    server = ThreadXMLRPCServer(('0.0.0.0', 8888), allow_none=True)  # 初始化
    server.register_function(file_put, 'file_put')
    print("Listening for Client")
    server.serve_forever()  # 保持等待调用状态

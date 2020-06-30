@echo off
rem nssm install servername //创建servername服务    
rem nssm start servername //启动服务
rem nssm stop servername //暂停服务
rem nssm restart servername //重新启动服务
rem nssm remove servername //删除创建的servername服务

nssm stop UploadFile
nssm remove UploadFile confirm
rem pause
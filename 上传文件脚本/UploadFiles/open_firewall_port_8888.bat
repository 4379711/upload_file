@echo off  


echo   . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
echo             开始创建防火墙出站入站规则
echo;
echo;
netsh advfirewall firewall show rule name="FileSystem" >nul
if not ERRORLEVEL 1 (
    echo 规则 FileSystem 已经存在,无需创建
) else (
   	netsh advfirewall firewall add rule name="FileSystem" dir=in action=allow protocol=TCP localport="8888" >nul
   	netsh advfirewall firewall add rule name="FileSystem" dir=out action=allow protocol=TCP localport="8888" >nul
    echo 规则 FileSystem 创建成功
)
echo;



rem 删除规则
rem netsh advfirewall firewall delete rule name="FileSystem" >nul

rem pause
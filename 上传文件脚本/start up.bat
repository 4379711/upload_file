@echo off
cd /d "%~dp0"
cacls.exe "%SystemDrive%\System Volume Information" >nul 2>nul
if %errorlevel%==0 goto Admin
if exist "%temp%\getadmin.vbs" del /f /q "%temp%\getadmin.vbs"
echo Set RequestUAC = CreateObject^("Shell.Application"^)>"%temp%\getadmin.vbs"
echo RequestUAC.ShellExecute "%~s0","","","runas",1 >>"%temp%\getadmin.vbs"
echo WScript.Quit >>"%temp%\getadmin.vbs"
"%temp%\getadmin.vbs" /f
if exist "%temp%\getadmin.vbs" del /f /q "%temp%\getadmin.vbs"
exit

:Admin




cd ./UploadFiles
echo   . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
echo   .    Auto create service and open filewall port 8888    .
echo   . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
echo;
echo;

call open_firewall_port_8888.bat

call create_service.bat
echo;
echo;
echo;
echo;
pause
@echo off  


echo   . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
echo             ��ʼ��������ǽ��վ��վ����
echo;
echo;
netsh advfirewall firewall show rule name="FileSystem" >nul
if not ERRORLEVEL 1 (
    echo ���� FileSystem �Ѿ�����,���贴��
) else (
   	netsh advfirewall firewall add rule name="FileSystem" dir=in action=allow protocol=TCP localport="8888" >nul
   	netsh advfirewall firewall add rule name="FileSystem" dir=out action=allow protocol=TCP localport="8888" >nul
    echo ���� FileSystem �����ɹ�
)
echo;



rem ɾ������
rem netsh advfirewall firewall delete rule name="FileSystem" >nul

rem pause
Set WshShell = CreateObject("WScript.Shell") 
WshShell.Run "cmd /c cd /d C:\DEEP_Assistant\ && python deep_assistant.py", 0, False 

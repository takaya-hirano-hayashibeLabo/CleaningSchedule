@echo off

set "bat_path=%~dp0"
cd %bat_path%
cd ../

set "app_path=%cd%\src\send_mail.py"

python %app_path%

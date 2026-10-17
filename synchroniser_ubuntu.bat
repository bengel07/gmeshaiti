@echo off
title Synchronisation Windows vers Ubuntu - GMES Haiti
powershell -ExecutionPolicy Bypass -File "%~dp0synchroniser_ubuntu.ps1" -Appliquer
echo.
pause
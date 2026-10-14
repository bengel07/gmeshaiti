
@echo off
setlocal
title Deploiement automatique GMES Haiti

cd /d "C:\Users\conta\Desktop\GMEShaiti"

echo ========================================
echo       DEPLOIEMENT GMES HAITI
echo ========================================

echo.
echo [1/3] Verification du depot Git...
git status
if errorlevel 1 goto erreur

echo.
set /p MESSAGE="Description de la modification : "
if "%MESSAGE%"=="" set MESSAGE=Mise a jour GMES

echo.
echo [2/3] Envoi des modifications sur GitHub...
git add -A
if errorlevel 1 goto erreur

git diff --cached --quiet
if not errorlevel 1 (
    echo Aucune modification a envoyer.
    goto serveur
)

git commit -m "%MESSAGE%"
if errorlevel 1 goto erreur

git push origin main
if errorlevel 1 goto erreur

:serveur
echo.
echo [3/3] Mise a jour du serveur Ubuntu...

ssh gmes@10.0.0.77 "cd ~/gmeshaiti && git pull --ff-only origin main && .venv/bin/python -m py_compile app.py && sudo systemctl restart gmes.service && sudo systemctl is-active gmes.service"
if errorlevel 1 goto erreur

echo.
echo ========================================
echo DEPLOIEMENT TERMINE
echo Verifie le site GMES Haiti.
echo ========================================
pause
exit /b 0

:erreur
echo.
echo ECHEC DU DEPLOIEMENT.
echo Lis le message d'erreur ci-dessus.
pause
exit /b 1

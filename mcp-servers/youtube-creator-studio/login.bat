@echo off
title YouTube Studio MCP - Login Unico
color 0c
echo =======================================================
echo          YOUTUBE MCP - AUTENTICACAO PLAYWRIGHT         
echo =======================================================
echo.
echo Uma janela do navegador vai se abrir no YouTube Studio.
echo Faca login com a conta Google do seu canal.
echo Apos logar e visualizar o painel, volte aqui e aperte ENTER.
echo.
echo =======================================================
cd /d "%~dp0"
python browser.py login
echo.
echo Pressione qualquer tecla para fechar esta janela...
pause >nul

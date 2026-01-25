@echo off
cd /d "%~dp0"
title NEXUS VANGUARD - LAUNCHER
echo [AVVIO] Attivazione protocolli di sicurezza...
call venv\Scripts\activate
echo [CONNESSO] Ambiente virtuale attivo.
echo [START] Lancio interfaccia tattica...
streamlit run app.py
pause
@echo off
echo [NEXUS VANGUARD] Caricamento TOTALE ordini e audio...
:: Aggiunge TUTTI i file modificati o nuovi (inclusi mp3, json, py)
git add .
git commit -m "Upload Intelligence e Audio"
git push
echo.
echo [OK] Tutto il materiale e' stato spedito nel Cloud.
echo Premi un tasto per chiudere.
pause
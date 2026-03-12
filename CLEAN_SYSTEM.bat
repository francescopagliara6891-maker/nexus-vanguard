@echo off
echo [NEXUS VANGUARD] Inizio protocollo di pulizia post-missione...
echo.

:: Cancella tutti i file MP3
if exist *.mp3 (
    del *.mp3
    echo [OK] File audio eliminati.
) else (
    echo [INFO] Nessun file audio trovato.
)

:: Cancella il registro delle missioni
if exist mission_orders.json (
    del mission_orders.json
    echo [OK] Registro missioni azzerato (Wipe).
) else (
    echo [INFO] Nessun registro missioni trovato.
)

echo.
echo [COMPLETATO] Sistema pulito e pronto per la prossima lezione.
echo Premi un tasto per chiudere.
pause
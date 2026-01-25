import json
import os
import requests
from datetime import datetime
import sys

# --- CONFIGURAZIONE ---
HISTORY_FILE = "mission_orders.json"
TG_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    if not TG_TOKEN or not TG_CHAT_ID:
        print("❌ Errore: Token o Chat ID mancanti nei Secrets.")
        return False
    
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown" # Usiamo Markdown per grassetti e format
    }
    
    try:
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            print("✅ Messaggio inviato con successo.")
            return True
        else:
            print(f"❌ Errore API Telegram: {r.text}")
            return False
    except Exception as e:
        print(f"❌ Errore connessione: {e}")
        return False

def main():
    print("🕵️ NEXUS DELIVERY AGENT - Avvio scansione...")
    
    if not os.path.exists(HISTORY_FILE):
        print("⚠️ Nessun ordine di missione trovato (file json assente).")
        return

    with open(HISTORY_FILE, "r") as f:
        missions = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📅 Data odierna: {today}")

    mission_found = False

    for mission in missions:
        # Se la data coincide E lo stato è ARMED
        if mission.get("target_date") == today:
            print(f"🚀 TROVATA MISSIONE ATTIVA PER OGGI! ID: {mission.get('id')}")
            
            header = f"⚡ **NEXUS VANGUARD INTELLIGENCE** ⚡\n📅 Target: {today}\n\n"
            content = mission.get("payload", "Nessun contenuto.")
            
            full_msg = header + content
            
            # Invio (spezziamo se troppo lungo, Telegram ha limite 4096 car)
            if len(full_msg) > 4000:
                # Invio in due parti se serve
                send_telegram(full_msg[:4000])
                send_telegram(full_msg[4000:])
            else:
                send_telegram(full_msg)
            
            mission_found = True
        
    if not mission_found:
        print("💤 Nessuna missione programmata per oggi. Standby.")

if __name__ == "__main__":
    main()
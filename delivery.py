import json
import os
import requests
from datetime import datetime
import glob

# --- CONFIGURAZIONE ---
HISTORY_FILE = "mission_orders.json"
TG_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TG_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_msg(message):
    if not TG_TOKEN or not TG_CHAT_ID: return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": TG_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    r = requests.post(url, json=payload)
    if r.status_code == 400:
        payload["parse_mode"] = None
        requests.post(url, json=payload)

def send_telegram_audio(audio_path):
    if not TG_TOKEN or not TG_CHAT_ID: return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendAudio"
    
    print(f"   [DEBUG] Sto provando a inviare il file: {audio_path}")
    print(f"   [DEBUG] Dimensione file: {os.path.getsize(audio_path)} bytes")

    try:
        with open(audio_path, 'rb') as audio:
            files = {"audio": audio}
            data = {"chat_id": TG_CHAT_ID}
            r = requests.post(url, data=data, files=files)
            if r.status_code == 200:
                print("   ✅ AUDIO INVIATO CON SUCCESSO!")
            else:
                print(f"   ❌ Errore Telegram Audio: {r.text}")
    except Exception as e:
        print(f"   ❌ Crash durante invio audio: {e}")

def main():
    print("🕵️ NEXUS DELIVERY AGENT - DIAGNOSTIC MODE")
    
    # DIAGNOSI FILESYSTEM
    print("📂 FILE PRESENTI NEL SERVER GITHUB:")
    files = glob.glob("*.*")
    for f in files:
        print(f"   - {f}")
    print("-----------------------------------")

    if not os.path.exists(HISTORY_FILE):
        print("❌ CRITICO: File mission_orders.json NON trovato.")
        return

    with open(HISTORY_FILE, "r") as f:
        missions = json.load(f)

    today = datetime.now().strftime("%Y-%m-%d")
    todays_missions = [m for m in missions if m.get("target_date") == today]
    
    if not todays_missions:
        print("💤 Nessuna missione per oggi.")
        return

    # PRENDIAMO L'ULTIMA
    todays_missions.sort(key=lambda x: x['id'])
    final_mission = todays_missions[-1]
    
    print(f"🚀 ELABORAZIONE MISSIONE ID: {final_mission.get('id')}")

    # INVIO TESTO
    header = f"⚡ *NEXUS INTELLIGENCE* ⚡\n📅 {today}\n\n"
    raw_payload = final_mission.get("payload", "")
    clean_payload = raw_payload.replace("**", "*").replace("_", "-") 
    full_msg = header + clean_payload
    
    if len(full_msg) > 4000:
        send_telegram_msg(full_msg[:4000])
        send_telegram_msg(full_msg[4000:])
    else:
        send_telegram_msg(full_msg)
    print("✅ Testo inviato.")

    # INVIO AUDIO
    audio_file = final_mission.get("audio_file")
    if audio_file:
        if os.path.exists(audio_file):
            send_telegram_audio(audio_file)
        else:
            print(f"⚠️ ERRORE CRITICO: Il JSON dice di inviare '{audio_file}', ma il file NON C'È nella lista sopra!")
    else:
        print("⚠️ Nessun file audio specificato nel JSON.")

if __name__ == "__main__":
    main()
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ ERRORE: Chiave non trovata.")
else:
    print("✅ AUTH OK. Scansione modelli disponibili in corso...\n")
    genai.configure(api_key=api_key)
    
    try:
        # Chiede a Google la lista dei modelli attivi
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"🔹 Modello rilevato: {m.name}")
                
        print("\n✅ Scansione completata.")
    except Exception as e:
        print(f"❌ ERRORE CRITICO: {e}")
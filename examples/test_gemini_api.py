"""
Quick test to verify Google Gemini API is working correctly.
Run this before using the full pipeline to check your API key.
"""
from google import genai
from google.genai import types
import os

def test_gemini_api():
    """Test if Gemini API key is configured correctly."""
    
    print("=" * 60)
    print("🤖 GEMINI API TEST")
    print("=" * 60)
    
    # Check if API key is set
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("\n❌ GOOGLE_API_KEY non trovata nelle variabili d'ambiente!")
        print("\nCome configurarla:")
        print("  Windows: $env:GOOGLE_API_KEY = 'tua-chiave-qui'")
        print("  Linux/Mac: export GOOGLE_API_KEY='tua-chiave-qui'")
        print("\n📖 Vedi SETUP_GEMINI.md per istruzioni dettagliate")
        return False
    
    print(f"\n✓ GOOGLE_API_KEY trovata: {'*' * 8}...")
    
    # Configure Gemini client
    try:
        client = genai.Client(api_key=api_key)
        print("✓ Gemini client configurato correttamente")
    except Exception as e:
        print(f"\n❌ Errore durante la configurazione: {e}")
        return False
    
    # Test a simple request
    print("\n[Test] Invio richiesta di prova a Gemini...")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents="Rispondi con un solo emoji che rappresenta il gaming",
            config=types.GenerateContentConfig(temperature=0.5)
        )
        
        result = response.text.strip()
        print(f"✓ Risposta ricevuta: {result}")
        
    except Exception as e:
        print(f"\n❌ Errore durante la richiesta: {e}")
        print("\nPossibili cause:")
        print("  - API key non valida")
        print("  - Quota giornaliera esaurita")
        print("  - API non abilitata nel progetto Google Cloud")
        print("\n🔗 Verifica su: https://makersuite.google.com/app/apikey")
        return False
    
    # Test JSON response
    print("\n[Test] Verifica risposta JSON...")
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents='Restituisci un JSON con questa struttura: {"test": "ok", "message": "Gemini funziona!"}',
            config=types.GenerateContentConfig(
                temperature=0.3,
                response_mime_type="application/json"
            )
        )
        
        import json
        result = json.loads(response.text)
        print(f"✓ JSON ricevuto: {result}")
        
    except Exception as e:
        print(f"❌ Errore nella risposta JSON: {e}")
        return False
    
    # Success!
    print("\n" + "=" * 60)
    print("✅ GEMINI FUNZIONA PERFETTAMENTE!")
    print("=" * 60)
    print("\n🎮 Sei pronto per creare highlight CS2!")
    print("\nProssimi passi:")
    print("  1. python main.py live        (prima del match)")
    print("  2. Gioca la tua partita CS2")
    print("  3. python main.py process video.mp4  (dopo il match)")
    print("=" * 60 + "\n")
    
    return True


if __name__ == '__main__':
    test_gemini_api()

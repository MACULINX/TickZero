"""
Script per verificare quali modelli Gemini sono disponibili.
"""
from google import genai
import os

def list_available_models():
    """Mostra tutti i modelli disponibili."""
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key:
        print("❌ GOOGLE_API_KEY non trovata!")
        return
    
    print("🔍 Recupero lista modelli disponibili...\n")
    
    try:
        client = genai.Client(api_key=api_key)
        
        # Lista tutti i modelli
        models = client.models.list()
        
        print("📋 MODELLI DISPONIBILI:")
        print("=" * 60)
        
        for model in models:
            print(f"\n• Nome: {model.name}")
            if hasattr(model, 'display_name'):
                print(f"  Display Name: {model.display_name}")
            if hasattr(model, 'description'):
                print(f"  Descrizione: {model.description}")
            if hasattr(model, 'supported_generation_methods'):
                print(f"  Metodi supportati: {model.supported_generation_methods}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == '__main__':
    list_available_models()

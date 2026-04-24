import os
from dotenv import load_dotenv

# Carrega do .env na raiz do Voxcia-Ops
load_dotenv(os.path.join(os.path.dirname(__file__), '../../.env'))

def check_env():
    print("\n--- 🔍 Verificando Conectividade Voxcia ---")
    
    checks = {
        "HUBSPOT": "HUBSPOT_ACCESS_TOKEN",
        "SUPABASE URL": "SUPABASE_URL",
        "SUPABASE KEY": "SUPABASE_SERVICE_ROLE_KEY"
    }

    for label, var in checks.items():
        val = os.getenv(var)
        # Verifica se existe e se tem um tamanho mínimo plausível
        status = "✅ OK" if val and len(val.strip()) > 20 else "❌ INVÁLIDO/AUSENTE"
        print(f"{label:<12}: {status}")

if __name__ == "__main__":
    check_env()

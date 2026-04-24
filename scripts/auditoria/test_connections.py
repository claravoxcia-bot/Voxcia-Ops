import os

def check_env():
    print("--- 🔍 Verificando Ambiente Voxcia ---")
    vars = ["HUBSPOT_ACCESS_TOKEN", "SUPABASE_URL", "SUPABASE_KEY"]
    for v in vars:
        status = "✅ OK" if os.getenv(v) else "❌ AUSENTE"
        print(f"{v}: {status}")

if __name__ == "__main__":
    check_env()

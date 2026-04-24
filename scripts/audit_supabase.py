#!/usr/bin/env python3
import os, sys, requests
from datetime import datetime
from dotenv import load_dotenv

# Carrega as credenciais do OpenClaw
load_dotenv("/root/.openclaw/.env")

HUBSPOT_TOKEN = os.getenv('HUBSPOT_ACCESS_TOKEN')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
REPORTS_DIR = "/root/Voxcia-Ops/reports/daily"

def fetch_hs():
    url = 'https://api.hubapi.com/crm/v3/objects/contacts'
    headers = {'Authorization': f'Bearer {HUBSPOT_TOKEN}'}
    r = requests.get(url, headers=headers, params={'limit': 100, 'properties': 'email'})
    r.raise_for_status()
    return set([o['properties']['email'].lower() for o in r.json().get('results', []) if o['properties'].get('email')])

def fetch_sb():
    # Tenta acessar a tabela 'leads'. Se não existir, retornará erro 404 ou 400.
    url = f"{SUPABASE_URL.rstrip('/')}/rest/v1/leads?select=email"
    headers = {'apikey': SUPABASE_KEY, 'Authorization': f'Bearer {SUPABASE_KEY}'}
    r = requests.get(url, headers=headers)
    if r.status_code == 404:
        print("⚠️ Tabela 'leads' não encontrada no Supabase. Criando conjunto vazio.")
        return set()
    r.raise_for_status()
    return set([row['email'].lower() for row in r.json() if row.get('email')])

def main():
    if not all([HUBSPOT_TOKEN, SUPABASE_URL, SUPABASE_KEY]):
        print("❌ Erro: Verifique as chaves no arquivo /root/.openclaw/.env")
        return
    try:
        print(f"🔍 Conectando ao projeto: {SUPABASE_URL}")
        hs = fetch_hs()
        sb = fetch_sb()
        missing = hs - sb
        
        os.makedirs(REPORTS_DIR, exist_ok=True)
        fn = os.path.join(REPORTS_DIR, f"{datetime.now().strftime('%Y-%m-%d')}_audit.md")
        
        with open(fn, 'w') as f:
            f.write(f"# Auditoria Voxcia - {datetime.now().date()}\n\n")
            f.write(f"- Leads no HubSpot: {len(hs)}\n")
            f.write(f"- Leads no Supabase: {len(sb)}\n\n")
            f.write("## 🚩 Pendentes de Sincronização (Apenas no HubSpot):\n")
            if not missing:
                f.write("Tudo sincronizado! ✅\n")
            for e in missing:
                f.write(f"- {e}\n")
        
        print(f"✅ Relatório de auditoria salvo em: {fn}")
    except Exception as e:
        print(f"❌ Falha na auditoria: {e}")

if __name__ == "__main__":
    main()

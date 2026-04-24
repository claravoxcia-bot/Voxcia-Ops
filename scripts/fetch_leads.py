import os, requests
from datetime import datetime
from dotenv import load_dotenv

# AJUSTADO: Caminho correto do OpenClaw
ENV_PATH = "/root/.openclaw/.env"
load_dotenv(ENV_PATH)

TOKEN = os.getenv('HUBSPOT_ACCESS_TOKEN')
REPORTS_DIR = "/root/Voxcia-Ops/reports/daily"

def get_recent_leads():
    headers = {'Authorization': f'Bearer {TOKEN}', 'Content-Type': 'application/json'}
    params = {'limit': '10', 'properties': 'firstname,lastname,email,createdate', 'sorts': '-createdate'}
    try:
        r = requests.get("https://api.hubapi.com/crm/v3/objects/contacts", headers=headers, params=params)
        r.raise_for_status()
        return r.json().get('results', [])
    except Exception as e:
        print(f"❌ Erro na API: {e}")
        return []

def save_report(leads):
    if not os.path.exists(REPORTS_DIR): os.makedirs(REPORTS_DIR)
    fn = os.path.join(REPORTS_DIR, f"{datetime.now().strftime('%Y-%m-%d')}_leads.md")
    with open(fn, 'w') as f:
        f.write(f"# 📊 Relatório Voxcia\n\n| Nome | Email | Data |\n| :--- | :--- | :--- |\n")
        for l in leads:
            p = l.get('properties', {})
            f.write(f"| {p.get('firstname','')} {p.get('lastname','')} | {p.get('email','')} | {p.get('createdate','')} |\n")
    print(f"✅ Gerado: {fn}")

if __name__ == "__main__":
    if not TOKEN:
        print(f"❌ ERRO: Token não encontrado em {ENV_PATH}")
    else:
        save_report(get_recent_leads())

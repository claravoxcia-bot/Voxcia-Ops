import os
import requests
from datetime import datetime
from dotenv import load_dotenv

# AJUSTADO: Caminho correto do OpenClaw
ENV_PATH = "/root/.openclaw/.env"
load_dotenv(ENV_PATH)

TOKEN = os.getenv('HUBSPOT_ACCESS_TOKEN')
REPORTS_DIR = "/root/Voxcia-Ops/reports/daily"

HUBSPOT_CONTACTS_URL = "https://api.hubapi.com/crm/v3/objects/contacts"
REQUEST_TIMEOUT = 15  # segundos


def get_recent_leads():
    """Busca os 10 contatos mais recentes via HubSpot CRM API v3.

    Nota: a ordenação por createdate é feita client-side pois o endpoint
    GET /crm/v3/objects/contacts não suporta o parâmetro 'sorts' (exclusivo
    do endpoint POST /search).
    """
    if not TOKEN:
        print(f"❌ ERRO: Token não encontrado em {ENV_PATH}")
        return []

    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
    }
    params = {
        'limit': 100,  # busca mais para ordenar corretamente client-side
        'properties': 'firstname,lastname,email,createdate',
    }
    try:
        r = requests.get(
            HUBSPOT_CONTACTS_URL,
            headers=headers,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )
        r.raise_for_status()
        results = r.json().get('results', [])
        # Ordena client-side: mais recentes primeiro (createdate ISO 8601)
        results.sort(
            key=lambda c: c.get('properties', {}).get('createdate', ''),
            reverse=True,
        )
        return results[:10]
    except requests.exceptions.Timeout:
        print(f"❌ Timeout na API HubSpot ({REQUEST_TIMEOUT}s)")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP na API: {e.response.status_code} {e.response.text[:200]}")
        return []
    except Exception as e:
        print(f"❌ Erro na API: {e}")
        return []


def _format_date(iso_str: str) -> str:
    """Converte ISO 8601 para formato legível (YYYY-MM-DD HH:MM)."""
    if not iso_str:
        return ''
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except ValueError:
        return iso_str


def save_report(leads):
    """Salva relatório Markdown com os leads mais recentes."""
    os.makedirs(REPORTS_DIR, exist_ok=True)  # thread-safe, sem race condition
    fn = os.path.join(REPORTS_DIR, f"{datetime.now().strftime('%Y-%m-%d')}_leads.md")
    with open(fn, 'w', encoding='utf-8') as f:
        f.write("# 📊 Relatório Voxcia\n\n")
        if not leads:
            f.write("_Nenhum lead encontrado._\n")
        else:
            f.write("| Nome | Email | Data |\n| :--- | :--- | :--- |\n")
            for lead in leads:
                props = lead.get('properties', {})
                name = f"{props.get('firstname', '')} {props.get('lastname', '')}".strip()
                email = props.get('email', '')
                date = _format_date(props.get('createdate', ''))
                f.write(f"| {name} | {email} | {date} |\n")
    print(f"✅ Gerado: {fn}")


if __name__ == "__main__":
    save_report(get_recent_leads())

import os, json, requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv("/root/.openclaw/.env")

app = Flask(__name__)
HUBSPOT_TOKEN = os.getenv('HUBSPOT_ACCESS_TOKEN')
AGENTMAIL_KEY = os.getenv('AGENTMAIL_API_KEY')

def check_hubspot(email):
    url = 'https://api.hubapi.com/crm/v3/objects/contacts/search'
    headers = {'Authorization': f'Bearer {HUBSPOT_TOKEN}', 'Content-Type': 'application/json'}
    payload = {"filterGroups":[{"filters":[{"propertyName":"email","operator":"EQ","value": email}]}],"limit":1}
    try:
        r = requests.post(url, headers=headers, json=payload)
        return "Conhecido" if r.json().get('total', 0) > 0 else "Novo"
    except: return "Erro"

@app.route('/odoo/webhook', methods=['POST'])
def webhook():
    data = request.json or {}
    email = data.get('email') or data.get('partner_email')
    if not email: return jsonify({"status": "no_email"}), 400
    
    status = check_hubspot(email)
    print(f"📩 Ticket de: {email} | Status: {status}")
    return jsonify({"status": "ok", "lead_type": status}), 200

if __name__ == "__main__":
    app.run(port=8080)

#!/usr/bin/env python3
import os, json
from pathlib import Path
from dotenv import dotenv_values
import requests

# Carrega env (OpenClaw primeiro, depois repo)
env = {}
env.update(dotenv_values('/root/.openclaw/.env'))
env.update(dotenv_values(os.path.expanduser('~/Voxcia-Ops/.env')))

TELEGRAM_TOKEN = env.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT = env.get('TELEGRAM_CHAT_ID')
DISCORD_WEBHOOK = env.get('DISCORD_WEBHOOK_URL')

# Busca o relatório mais recente
repdir = Path(os.path.expanduser('~/Voxcia-Ops/reports/daily'))
files = sorted(repdir.glob('*.md'))
latest = files[-1] if files else None

if latest:
    text = latest.read_text(encoding='utf-8')
    summary = '\n'.join(text.splitlines()[:20])
else:
    summary = 'Nenhum relatório encontrado.'

msg = f"🚀 Voxcia — Piloto Concluído\nArquivo: {latest.name if latest else 'N/A'}\n\n{summary}"

# Envio Telegram
if TELEGRAM_TOKEN and TELEGRAM_CHAT:
    try:
        requests.post(f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage', 
                      json={'chat_id': TELEGRAM_CHAT, 'text': msg}, timeout=10)
    except Exception as e: print(f'Erro Telegram: {e}')

# Envio Discord
if DISCORD_WEBHOOK:
    try:
        requests.post(DISCORD_WEBHOOK, json={'content': msg}, timeout=10)
    except Exception as e: print(f'Erro Discord: {e}')

print('✅ Notificações processadas.')

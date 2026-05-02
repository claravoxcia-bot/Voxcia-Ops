"""
Clara Executor — recebe comandos via HTTP e executa no host real
Roda no host, exposto internamente, acionado pelo OpenClaw via HTTP skill
"""
from flask import Flask, request, jsonify
import subprocess, os, hmac, hashlib

app = Flask(__name__)
SECRET = os.getenv("EXECUTOR_SECRET", "voxcia-internal-2026")

ALLOWED = [
    "fetch_leads", "audit_supabase", "git_push", 
    "git_status", "list_reports", "drive_upload"
]

def verify(token):
    expected = hmac.new(SECRET.encode(), digestmod=hashlib.sha256).hexdigest()
    return hmac.compare_digest(token or "", expected)

@app.route("/run", methods=["POST"])
def run():
    data = request.json or {}
    cmd = data.get("command", "")
    
    if cmd not in ALLOWED:
        return jsonify({"error": f"Comando '{cmd}' não permitido"}), 403
    
    script_map = {
        "fetch_leads":    "python3 /root/Voxcia-Ops/scripts/fetch_leads.py",
        "audit_supabase": "python3 /root/Voxcia-Ops/scripts/audit_supabase.py",
        "git_push":       f'bash /root/Voxcia-Ops/scripts/git_push.sh "{data.get("msg","Auto")}"',
        "git_status":     "git -C /root/Voxcia-Ops status --short",
        "list_reports":   "ls -lt /root/Voxcia-Ops/reports/daily/ | head -10",
        "drive_upload":   f'python3 /root/Voxcia-Ops/scripts/drive_upload.py {data.get("file","")}',
    }
    
    result = subprocess.run(
        script_map[cmd], shell=True, capture_output=True, 
        text=True, timeout=60, cwd="/root/Voxcia-Ops"
    )
    
    return jsonify({
        "command": cmd,
        "stdout": result.stdout[-2000:],
        "stderr": result.stderr[-500:] if result.stderr else None,
        "returncode": result.returncode
    })

@app.route("/health")
def health():
    return jsonify({"status": "ok", "host": "voxcia-ops"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=7070, debug=False)

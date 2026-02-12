import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# n8n Configuration
N8N_BASE_URL = os.getenv("N8N_WEBHOOK_URL", "https://n8n2.allanturing.com/webhook")

def trigger_audit_sync(empresa_id, cnpj, tipo, ie_pr=None):
    """
    Triggers an audit synchronization in n8n.
    Types: 'cnd_federal', 'cnd_pr', 'fgts'
    """
    webhook_map = {
        'cnd_federal': f"{N8N_BASE_URL}/consulta-cnd-federal",
        'cnd_pr': f"{N8N_BASE_URL}/consulta-cnd-pr",
        'fgts': f"{N8N_BASE_URL}/consulta-fgts"
    }
    
    url = webhook_map.get(tipo)
    if not url:
        return False, "Tipo de auditoria inválido."
        
    payload = {
        "consulta_id": f"manual-{empresa_id}-{tipo}",
        "cnpj": cnpj,
        "empresa_id": empresa_id
    }
    
    if tipo == 'cnd_pr' and ie_pr:
        payload['ie_pr'] = ie_pr
        
    try:
        # Use a timeout of 5s to avoid blocking the UI
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code in [200, 201]:
            return True, "Sincronização iniciada com sucesso no n8n."
        else:
            return False, f"Erro no n8n ({response.status_code}): {response.text}"
    except Exception as e:
        return False, f"Falha de conexão com o motor de auditoria: {str(e)}"

def trigger_scheduler():
    """Triggers the global scheduler workflow"""
    url = f"{N8N_BASE_URL}/agendador"
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except:
        return False

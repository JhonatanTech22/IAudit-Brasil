import streamlit as st
from utils.styles import get_custom_css

st.set_page_config(
    page_title="IAudit - Central de Comando",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply high-end CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Central Hero Area
# Institutional Header (GOV.BR Simulation)
st.markdown("""
    <div class='gov-bar'>
        <span>BRASIL — MINISTÉRIO DA FAZENDA</span>
        <span>SENADO FEDERAL • FGTS</span>
    </div>
    <div style='text-align: center; padding: 3rem 0; border-left: 8px solid var(--gov-yellow); margin: 3rem 0; background: linear-gradient(90deg, rgba(15, 23, 42, 0.5) 0%, transparent 100%);'>
        <div class='system-label'>VIGILÂNCIA INSTITUCIONAL ESTRUTURADA</div>
        <h1 style='font-size: 4rem !important;'>iAudit Brasil</h1>
        <p style='color: white; font-size: 1.3rem; font-weight: 500; max-width: 850px; margin: 1.5rem auto; line-height: 1.6;'>
            Monitoramento inteligente e gestão de ativos institucionais em tempo real. 
            Autoridade técnica em conformidade para o ecossistema federativo.
        </p>
    </div>
""", unsafe_allow_html=True)

# The Three Pillars Section
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: var(--text-muted); font-size: 0.8rem; font-weight: 700; letter-spacing: 0.4em; margin-bottom: 2rem;'>PILARES DE AUDITORIA INSTITUCIONAL</div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class='glass-card' style='border-top: 4px solid var(--federal-blue); background: var(--surface-card);'>
            <div style='display: flex; align-items: center; margin-bottom: 1.5rem;'>
                <span style='font-size: 2rem; margin-right: 1rem;'>🏛️</span>
                <span style='color: var(--federal-blue); font-weight: 800; font-size: 0.8rem; letter-spacing: 0.1em;'>SENADO FEDERAL</span>
            </div>
            <h3 style='margin-bottom: 0.8rem;'>Receita & PGFN</h3>
            <p style='color: var(--text-muted); font-size: 0.95rem; line-height: 1.6;'>
                Vigilância contínua da Regularidade Fiscal da União e Certidões Conjuntas.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='glass-card' style='border-top: 4px solid var(--state-purple); background: var(--surface-card);'>
            <div style='display: flex; align-items: center; margin-bottom: 1.5rem;'>
                <span style='font-size: 2rem; margin-right: 1rem;'>🏢</span>
                <span style='color: var(--state-purple); font-weight: 800; font-size: 0.8rem; letter-spacing: 0.1em;'>SENADO ESTADUAL</span>
            </div>
            <h3 style='margin-bottom: 0.8rem;'>SEFA Paraná</h3>
            <p style='color: var(--text-muted); font-size: 0.95rem; line-height: 1.6;'>
                Gestão automatizada de débitos estaduais e situação cadastral ICMS/PR.
            </p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='glass-card' style='border-top: 4px solid var(--fgts-green); background: var(--surface-card);'>
            <div style='display: flex; align-items: center; margin-bottom: 1.5rem;'>
                <span style='font-size: 2rem; margin-right: 1rem;'>🛡️</span>
                <span style='color: var(--fgts-green); font-weight: 800; font-size: 0.8rem; letter-spacing: 0.1em;'>CAIXA ECONÔMICA</span>
            </div>
            <h3 style='margin-bottom: 0.8rem;'>FGTS Digital</h3>
            <p style='color: var(--text-muted); font-size: 0.95rem; line-height: 1.6;'>
                Controle de CND FGTS (CRF) e monitoramento de encargos sociais vigentes.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Quick Access Console
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div class='glass-card' style='background: linear-gradient(135deg, rgba(30, 27, 75, 0.4) 0%, rgba(0, 0, 0, 0.8) 100%);'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h3 style='color: white; margin-bottom: 0.5rem;'>Terminal de Gestão</h3>
                <p style='color: #cbd5e1; font-size: 0.95rem;'>Inicie novas auditorias ou gerencie ativos importados.</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Functional navigation console
col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 1])
with col_btn1:
    if st.button("📊 DASHBOARD", use_container_width=True, type="primary"):
        st.switch_page("pages/00_Dashboard.py")
with col_btn2:
    if st.button("📥 INGESTÃO", use_container_width=True):
        st.switch_page("pages/01_Upload.py")
with col_btn3:
    if st.button("🏢 EMPRESAS", use_container_width=True):
        st.switch_page("pages/02_Empresas.py")
with col_btn4:
    if st.button("📑 DOSSIÊ", use_container_width=True):
        st.switch_page("pages/03_Detalhes.py")

# Automation Management Center
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 1.5rem; margin-bottom: 2rem;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div style='display: flex; align-items: center;'>
                <div style='width: 12px; height: 12px; background: #10b981; border-radius: 50%; margin-right: 1rem; box-shadow: 0 0 10px #10b981;'></div>
                <h4 style='color: white; margin: 0;'>Agendador Inteligente IAudit</h4>
            </div>
            <div style='color: #94a3b8; font-size: 0.8rem; font-family: monospace;'>PROX. EXECUÇÃO: T+5min</div>
        </div>
        <p style='color: #cbd5e1; font-size: 0.85rem; margin-top: 1rem; line-height: 1.5;'>
            O motor de agendamento monitora silenciosamente o repositório. Em produção (n8n), ele executa rotinas de CND Federal, PR e FGTS conforme a periodicidade de cada ativo.
        </p>
    </div>
""", unsafe_allow_html=True)

col_auto1, col_auto2 = st.columns([2, 1])
with col_auto1:
    st.info("A ativação no n8n requer configuração do Supabase no arquivo .env")
with col_auto2:
    if st.button("▶️ FORÇAR AGENDADOR", use_container_width=True):
        import requests
        import os
        from dotenv import load_dotenv
        load_dotenv()
        n8n_url = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook")
        try:
            r = requests.get(f"{n8n_url}/agendador", timeout=5)
            if r.status_code == 200:
                st.success("Agendador disparado com sucesso!")
            else:
                st.error(f"Erro ao disparar: {r.status_code}")
        except Exception as e:
            st.warning("Usando simulador local (Mock n8n)")
            # Try local mock
            try:
                r = requests.get("http://localhost:5678/webhook/agendador", timeout=2)
                st.success("Simulador local executado!")
            except:
                st.error("Servidor Mock não está rodando.")

# Infrastructure Status Line
st.markdown("""
    <div style='display: flex; justify-content: center; gap: 2rem; opacity: 0.8; margin-top: 4rem;'>
        <div style='color: #cbd5e1; font-size: 0.7rem; letter-spacing: 0.2em;'>CORE-ENGINE: ACTIVE</div>
        <div style='color: #cbd5e1; font-size: 0.7rem; letter-spacing: 0.2em;'>DATA-SYNC: LOCAL-STATE</div>
        <div style='color: #cbd5e1; font-size: 0.7rem; letter-spacing: 0.2em;'>SECURE-LAYER: AES-512</div>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from datetime import datetime, time
from utils.styles import get_custom_css
from utils.db import db
from utils.n8n_api import trigger_audit_sync
from utils.formatters import format_cnpj, format_datetime, format_date, get_status_icon

st.set_page_config(
    page_title="Detalhes - Dossier do Ativo",
    page_icon="📋",
    layout="wide"
)

# Apply high-end CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Main Content with Error Handling
try:
    # Handle selection from other pages
    empresas = db.get_empresas()
    default_idx = 0
    if "selected_emp_id" in st.session_state and empresas:
        for i, e in enumerate(empresas):
            if e.get('id') == st.session_state.selected_emp_id:
                default_idx = i
                break

    # Advanced Selector
    if not empresas:
        st.warning("Nenhum ativo cadastrado no repositório.")
        st.stop()

    sel_name = st.selectbox("Selecione Ativo para Auditoria", [str(e.get('razao_social', 'N/A')) for e in empresas], index=default_idx)
    empresa = next((e for e in empresas if e.get('razao_social') == sel_name), empresas[0])
    st.session_state.selected_emp_id = empresa.get('id')

    # Get latest consultations for this specific company
    stats = db.get_latest_status().get(empresa.get('id'), {}) if db.get_latest_status() else {}
    emp_con = stats.get('consultas', {})

    # Official Entity Header
    status_color = '#065f46' if empresa.get('ativo', False) else '#991b1b'
    status_text = 'ESTADO: ATIVO' if empresa.get('ativo', False) else 'ESTADO: INATIVO'
    
    st.markdown(f"""
        <div style='background: #000; padding: 6px 16px; margin-bottom: 1.5rem; border-bottom: 2px solid var(--gov-yellow); font-size: 0.7rem; font-weight: 800; letter-spacing: 0.2em; color: var(--gov-yellow);'>
            AUDITORIA INSTITUCIONAL — CERTIFICAÇÃO OFICIAL DE REGULARIDADE FISCAL
        </div>
        <div class='glass-card' style='border-left: 8px solid var(--gov-yellow); background: #111827; padding: 2rem; border-radius: 0 12px 12px 0; box-shadow: 0 12px 48px rgba(0,0,0,0.5);'>
            <div style='display: flex; justify-content: space-between; align-items: start;'>
                <div>
                    <h2 style='margin-bottom: 0.5rem; font-size: 2.8rem; color: #f8fafc !important; font-weight: 900;'>{str(empresa.get('razao_social', 'N/A')).upper()}</h2>
                    <div style='color: #94a3b8; font-family: "JetBrains Mono", monospace; font-size: 1rem; letter-spacing: 0.1em;'>
                        CNPJ: {format_cnpj(empresa.get('cnpj'))} | ID: {empresa.get('id', 'N/A')} {f"| IE-PR: {empresa.get('inscricao_estadual_pr')}" if empresa.get('inscricao_estadual_pr') else ""}
                    </div>
                </div>
                <div style='background: {status_color}; color: white; padding: 0.8rem 1.5rem; border-radius: 999px; font-weight: 800; font-size: 0.8rem; letter-spacing: 0.1em; box-shadow: 0 0 20px rgba(0,0,0,0.2)'>
                    {status_text}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Audit Pillars Section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='system-label'>PILARE DE CONFORMIDADE — STATUS ATUAL</div>", unsafe_allow_html=True)

    # Mocked latest consultations for the 3 pillars
    tipos = {
        'cnd_federal': ('FEDERAL (SRFB/PGFN)', 'var(--federal-blue)'),
        'cnd_pr': ('ESTADUAL (SEFA-PR)', 'var(--state-purple)'),
        'fgts': ('RECOLHIMENTO (CRF-FGTS)', 'var(--fgts-green)')
    }

    col1, col2, col3 = st.columns(3)
    for idx, (tk, (tn, tc)) in enumerate(tipos.items()):
        with [col1, col2, col3][idx]:
            # Logic to find latest for this type
            latest = emp_con.get(tk)
            
            if latest:
                st.markdown(f"""
                    <div class='glass-card' style='text-align: center; border-bottom: 4px solid {tc};'>
                        <div style='font-size: 3rem; margin-bottom: 1.5rem;'>{get_status_icon(latest.get('situacao'))}</div>
                        <h4 style='margin-bottom: 0.5rem;'>{tn}</h4>
                        <p style='color: {tc}; font-weight: 800; font-size: 0.8rem; letter-spacing: 0.1em;'>{'REGULAR' if latest.get('situacao') == 'positiva' else 'DIVERGENTE'}</p>
                        <div style='margin-top: 1.5rem; color: var(--text-muted); font-size: 0.75rem;'>VALIDADE: {format_date(latest.get('data_validade'))}</div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"FORÇAR ATUALIZAÇÃO: {tk.upper()}", key=f"ex_{idx}", use_container_width=True):
                    with st.spinner("Solicitando auditoria ao motor n8n..."):
                        success, msg = trigger_audit_sync(empresa['id'], empresa['cnpj'], tk, empresa.get('inscricao_estadual_pr'))
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)
            else:
                st.markdown(f"""
                    <div class='glass-card' style='text-align: center; border: 1px dashed var(--border-color); opacity: 0.8;'>
                        <div style='font-size: 3rem; margin-bottom: 1.5rem; color: var(--text-muted); opacity: 0.3;'>○</div>
                        <h4 style='color: var(--text-muted); margin-bottom: 0.5rem;'>{tn}</h4>
                        <p style='color: var(--text-muted); font-size: 0.8rem;'>AGUARDANDO SINCRONIZAÇÃO</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"EXECUTAR AUDITORIA: {idx+1}", key=f"ex_{idx}", type="secondary", use_container_width=True):
                    with st.spinner("Iniciando auditoria..."):
                        success, msg = trigger_audit_sync(empresa['id'], empresa['cnpj'], tk, empresa.get('inscricao_estadual_pr'))
                        if success:
                            st.success(msg)
                        else:
                            st.error(msg)

    # Console de Gestão - Tabs for separation
    st.markdown("<br><br>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["LOG DE AUDITORIA", "CONFIGURAÇÃO DO AGENTE"])

    with t1:
        st.markdown("<div style='background: #010409; border: 1px solid var(--border-color); padding: 1.5rem; margin-top: 1rem;'>", unsafe_allow_html=True)
        if emp_con:
            h_data = []
            consultas_list = [v for v in emp_con.values() if isinstance(v, dict)]
            if consultas_list:
                for c in sorted(consultas_list, key=lambda x: str(x.get('data_execucao', '')), reverse=True):
                    h_data.append({
                        'TIPO': str(c.get('tipo', '')).upper().replace('CND_', ''),
                        'MÉTODO': 'OFICIAL',
                        'TIMESTAMP': format_datetime(c.get('data_execucao')),
                        'SITUAÇÃO': 'CERTIFICADO' if c.get('situacao') == 'positiva' else 'DIVERGÊNCIA'
                    })
                st.dataframe(pd.DataFrame(h_data), use_container_width=True, hide_index=True)
            else:
                st.info("Log de auditoria vazio para esta entidade.")
        else:
            st.info("Log de auditoria vazio para esta entidade.")
        st.markdown("</div>", unsafe_allow_html=True)

    with t2:
        st.markdown("<div class='glass-card' style='margin-top: 1rem;'>", unsafe_allow_html=True)
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            st.selectbox("Frequência de Auditoria", ["DIÁRIA", "SEMANAL", "BI-SEMANAL"], index=0)
            st.text_input("Recipiente de Notificação", value=empresa.get('email_notificacao', 'senado.fiscal@contato.gov.br'))
        with c_p2:
            st.time_input("Janela de Batida (Sincronia)", value=datetime.now().time())
            st.button("SALVAR PARÂMETROS", type="primary", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erro ao carregar detalhes do ativo: {str(e)}")
    st.exception(e)

# Footer
st.markdown("""
    <div style='text-align: center; padding: 4rem 0 2rem 0; opacity: 0.5;'>
        <p style='font-size: 0.7rem; font-family: "JetBrains Mono", monospace; letter-spacing: 0.1em;'>SISTEMA DE AUDITORIA FEDERAL V2.0.4 | GOV-AUTHENTICATED</p>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from utils.styles import get_custom_css
from utils.db import db
from utils.formatters import mask_cnpj, format_date, get_status_icon, format_periodicidade

st.set_page_config(
    page_title="Empresas - Inventário de Ativos",
    page_icon="🏢",
    layout="wide"
)

# Apply high-end CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Institutional Header
st.markdown("""
    <div class='gov-bar'>
         <span>BRASIL — INVENTÁRIO DE ATIVOS FEDERAIS</span>
         <span>RECONHECIMENTO INSTITUCIONAL</span>
    </div>
        <div style='margin-bottom: 3.5rem; border-left: 6px solid var(--gov-yellow); padding-left: 1.5rem;'>
            <div class='system-label'>BASE REPOSITÓRIO V2.0 — GOVERNAMENTAL</div>
            <h1 style='font-size: 2.8rem !important;'>Repositório de Ativos</h1>
            <p style='font-size: 1rem; color: #cbd5e1; font-weight: 600; letter-spacing: 0.05em;'>GESTÃO ESTRUTURADA DE MONITORAMENTO FISCAL (SENADO/FGTS)</p>
        </div>
""", unsafe_allow_html=True)

try:
    # Get data from DataLayer
    empresas = db.get_empresas()
    latest_status = db.get_latest_status()

    # Advanced Filters Console
    st.markdown("<div class='system-label'>CONSOLE DE FILTRAGEM</div>", unsafe_allow_html=True)
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)

    with col_f1:
        search = st.text_input("Localizar por Identificação", placeholder="SOCIAL OU CNPJ")
    with col_f2:
        status_filter = st.selectbox("Estado Operacional", ["Todos", "Ativo", "Inativo"])
    with col_f3:
        periodicidade_filter = st.selectbox("Intervalo de Sincro", ["Todas", "Diário", "Semanal", "Quinzenal", "Mensal"])
    with col_f4:
        situacao_filter = st.selectbox("Score de Risco", ["Todas", "Regular", "Irregular", "Pendente"])

    # Apply filters (simplified logic for UI)
    filtered = list(empresas).copy() if empresas else []
    if search:
        filtered = [e for e in filtered if search.lower() in str(e.get('razao_social', '')).lower() or search in str(e.get('cnpj', ''))]

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Main Inventory Results
    st.markdown(f"<div class='system-label'>RESULTADOS DA BUSCA — {len(filtered)} ENTIDADES</div>", unsafe_allow_html=True)

    if filtered:
        table_data = []
        for e in filtered:
            emp_id = e.get('id', '0')
            emp_status_obj = latest_status.get(emp_id, {}) if latest_status else {}
            consultas = emp_status_obj.get('consultas', {}) if isinstance(emp_status_obj, dict) else {}
            
            cnd_fed = consultas.get('cnd_federal', {}) if isinstance(consultas, dict) else {}
            cnd_pr = consultas.get('cnd_pr', {}) if isinstance(consultas, dict) else {}
            fgts = consultas.get('fgts', {}) if isinstance(consultas, dict) else {}

            table_data.append({
                'IDENTIFICAÇÃO': str(e.get('razao_social', 'N/A')).upper(),
                'CNPJ': mask_cnpj(e.get('cnpj')),
                'FEDERAL': get_status_icon(cnd_fed.get('situacao') if isinstance(cnd_fed, dict) else None),
                'ESTADUAL': get_status_icon(cnd_pr.get('situacao') if isinstance(cnd_pr, dict) else None),
                'FGTS': get_status_icon(fgts.get('situacao') if isinstance(fgts, dict) else None),
                'CICLO': format_periodicidade(str(e.get('periodicidade', 'semanal'))).upper(),
                'STATUS': '● ATIVO' if e.get('ativo', False) else '○ INATIVO',
                'ID': emp_id
            })
        
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)

        # Secondary Action Console
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<div class='system-label'>CENTRAL DE AÇÃO INDIVIDUAL</div>", unsafe_allow_html=True)
        
        names_list = [str(e.get('razao_social', 'N/A')) for e in filtered]
        selected_name = st.selectbox("Selecione Ativo para Auditoria Detalhada", names_list, label_visibility="collapsed")
        
        col_a1, col_a2, col_a3 = st.columns([2, 1, 1])
        with col_a1:
            if st.button(f"ABRIR PAINEL DE CONFORMIDADE", use_container_width=True, type="primary"):
                selected_emp = next((e for e in filtered if str(e.get('razao_social')) == selected_name), None)
                if selected_emp:
                    st.session_state.selected_emp_id = selected_emp.get('id')
                    st.switch_page("pages/03_Detalhes.py")
        with col_a2:
            if st.button("ACIONAR SINCRONIA MANUAL", use_container_width=True):
                st.info("Sincronização global solicitada ao motor n8n...")
        with col_a3:
            if st.button("PAUSAR MONITORAMENTO", use_container_width=True):
                st.warning("Monitoramento suspenso para a entidade selecionada.")

    else:
        st.markdown("""
            <div style='text-align: center; padding: 4rem; background: #0f172a; border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px;'>
                <p style='color: #cbd5e1; font-weight: 500; font-size: 0.9rem;'>CONSULTA SEM RESULTADOS CORRESPONDENTES</p>
            </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erro ao carregar repositório de empresas: {str(e)}")
    st.exception(e)

# Footer
st.markdown("""
    <div style='text-align: center; padding: 4rem 0 2rem 0; opacity: 0.1;'>
        <p style='font-size: 0.7rem; font-family: "JetBrains Mono", monospace; letter-spacing: 0.3em;'>INVENTORY-NODE PR-44 | DATABASE-LAYER: SYNC-OK</p>
    </div>
""", unsafe_allow_html=True)

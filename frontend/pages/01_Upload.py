import streamlit as st
import pandas as pd
from datetime import time
from io import BytesIO
from utils.styles import get_custom_css
from utils.validators import validate_cnpj
from utils.formatters import format_cnpj
from utils.db import db

st.set_page_config(
    page_title="Upload - Ingestão de Ativos",
    page_icon="📥",
    layout="wide"
)

# Apply high-end CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Institutional Header
st.markdown("""
    <div class='gov-bar'>
        <span>BRASIL — PROTOCOLO DE INGESTÃO DE ATIVOS</span>
        <span>SEGURANÇA E CONFORMIDADE</span>
    </div>
    <div style='margin-bottom: 3.5rem; border-left: 6px solid var(--gov-yellow); padding-left: 1.5rem;'>
        <div class='system-label'>INGESTION-NODE — PRESTÍGIO FEDERAL</div>
        <h1 style='font-size: 2.8rem !important;'>Console de Ingestão</h1>
        <p style='font-size: 0.95rem; color: var(--text-muted); font-weight: 600; letter-spacing: 0.05em;'>CARREGAMENTO E VALIDAÇÃO DE ATIVOS INSTITUCIONAIS</p>
    </div>
""", unsafe_allow_html=True)

# File Upload Section
st.markdown("<div class='system-label'>GATEWAY DE ARQUIVOS</div>", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Carregar Base Estruturada",
    type=['csv', 'xlsx'],
    label_visibility="collapsed"
)

# Template Download - Minimalist Link
template_data = pd.DataFrame({
    'CNPJ': ['12345678000195'],
    'Razao Social': ['ENTIDADE EXEMPLO LTDA'],
    'IE_PR': ['1234567890'],
    'Email': ['contato@exemplo.com.br']
})
csv_buffer = BytesIO()
template_data.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
csv_buffer.seek(0)

st.download_button(
    label="Download Structure Template",
    data=csv_buffer,
    file_name="iaudit_template.csv",
    mime="text/csv",
)

if uploaded_file:
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        required_cols = ['CNPJ', 'Razao Social']
        if not all(col in df.columns for col in required_cols):
            st.error("ERRO DE ESTRUTURA: Colunas obrigatórias não detectadas.")
        else:
            df['CNPJ'] = df['CNPJ'].astype(str).str.replace(r'\D', '', regex=True)
            
            valid_indices = []
            invalid_list = []
            duplicates = []
            existing_cnpjs = [e['cnpj'] for e in db.get_empresas()]
            
            for idx, row in df.iterrows():
                cnpj = row['CNPJ']
                is_valid, _ = validate_cnpj(cnpj)
                if not is_valid:
                    invalid_list.append(idx)
                elif cnpj in existing_cnpjs:
                    duplicates.append(idx)
                else:
                    valid_indices.append(idx)
            
            # Validation Dashboard
            st.markdown("<div class='system-label'>REPORT DE CONSISTÊNCIA</div>", unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"<div class='glass-card' style='padding:1.5rem; border-bottom:2px solid #3b82f6;'><div style='color:#94a3b8; font-size:0.7rem; font-weight:800;'>VALOR TOTAL</div><div style='color:white; font-size:2rem; font-weight:800;'>{len(df)}</div></div>", unsafe_allow_html=True)
            with c2:
                st.markdown(f"<div class='glass-card' style='padding:1.5rem; border-bottom:2px solid #10b981;'><div style='color:#94a3b8; font-size:0.7rem; font-weight:800;'>QUALIFICADOS</div><div style='color:#10b981; font-size:2rem; font-weight:800;'>{len(valid_indices)}</div></div>", unsafe_allow_html=True)
            with c3:
                st.markdown(f"<div class='glass-card' style='padding:1.5rem; border-bottom:2px solid #ef4444;'><div style='color:#94a3b8; font-size:0.7rem; font-weight:800;'>REJEITADOS</div><div style='color:#ef4444; font-size:2rem; font-weight:800;'>{len(invalid_list) + len(duplicates)}</div></div>", unsafe_allow_html=True)
            
            st.markdown("<br><br>", unsafe_allow_html=True)
            
            # Preview with pillar-entity focus
            st.markdown("<div class='system-label'>AMSTRAGEM — VISÃO AUDITOR</div>", unsafe_allow_html=True)
            df_preview = df.copy()
            df_preview['ESTADO'] = df_preview.index.map(lambda idx: '✅ QUALIFICADO' if idx in valid_indices else '❌ FALHA')
            df_preview['CNPJ'] = df_preview['CNPJ'].apply(format_cnpj)
            st.dataframe(df_preview.head(8), use_container_width=True, hide_index=True)
            
            if valid_indices:
                st.markdown("<br><br>", unsafe_allow_html=True)
                st.markdown("<div class='system-label'>CONFIGURAÇÃO DE MONITORAMENTO</div>", unsafe_allow_html=True)
                
                c_conf1, c_conf2 = st.columns(2)
                with c_conf1:
                    st.selectbox("Protocolo de Frequência", ["DIÁRIO (ALTA PRIORIDADE)", "SEMANAL (PADRÃO)", "MENSAL (BAIXO VOLUME)"], index=1)
                with c_conf2:
                    st.time_input("Agendamento de Sincro", value=time(8, 0))
                
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("CONFIRMAR INGESTÃO", use_container_width=True, type="primary"):
                    success = db.insert_empresas(df.iloc[valid_indices])
                    if success:
                        st.success(f"PROTOCOLOS DE AUDITORIA INICIADOS PARA {len(valid_indices)} ENTIDADES.")
                        st.balloons()
                        # Delay slightly before redirecting
                        import time as _time
                        _time.sleep(2)
                        st.switch_page("pages/02_Empresas.py")
                    else:
                        st.error("FALHA SISTÊMICA AO SALVAR NO REPOSITÓRIO.")
            
    except Exception as e:
        st.error(f"FALHA NO PARSING: {str(e)}")

else:
    # Instructions
    st.markdown("""
        <div style='text-align: center; padding: 4rem 2rem; background: #1e293b; border: 1px solid var(--border-color); border-radius: 12px; margin-top: 2rem;'>
            <h3 style='margin-bottom: 1rem; color: white !important;'>Console de Ingestão</h3>
            <p style='color: var(--text-muted); font-size: 1rem; max-width: 500px; margin: 0 auto; line-height: 1.6;'>
                Carregue seu inventário de CNPJs. O motor <strong>IAudit</strong> realizará a triagem automática e iniciará a vigilância institucional nos pilares Federal, Estadual e Caixa FGTS.
            </p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div style='text-align: center; padding: 4rem 0 2rem 0; opacity: 0.1;'>
        <p style='font-size: 0.7rem; font-family: "JetBrains Mono", monospace; letter-spacing: 0.3em;'>INGESTION-LAYER V2.0.4 | ENCRYPTED-CHANNEL: ACTIVE</p>
    </div>
""", unsafe_allow_html=True)

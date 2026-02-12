import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.styles import get_custom_css
from utils.db import db
from utils.formatters import format_datetime, get_status_icon

st.set_page_config(
    page_title="Dashboard - Auditoria Sistêmica",
    page_icon="📊",
    layout="wide"
)

# Apply high-end CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Official Header
st.markdown("""
    <div class='gov-bar'>
        <span>BRASIL — SISTEMA DE AUDITORIA FEDERAL</span>
        <span>CONSELHO DE GESTÃO ESTRATÉGICA</span>
    </div>
    <div style='margin-bottom: 3.5rem; border-left: 6px solid var(--gov-yellow); padding-left: 1.5rem;'>
        <div class='system-label'>DATA ANALYTICS NODE — OFICIAL</div>
        <h1 style='font-size: 2.8rem !important;'>Console de Auditoria</h1>
        <p style='font-size: 0.95rem; color: #cbd5e1; font-weight: 600; letter-spacing: 0.05em;'>INDICADORES DE CONFORMIDADE E RISCO FISCAL</p>
    </div>
""", unsafe_allow_html=True)

# Main Dashboard Content
try:
    # Get and validate metrics
    from utils.mock_data import get_dashboard_stats
    base_stats = get_dashboard_stats()
    stats = db.get_latest_status()
    empresas = db.get_empresas()
    active_count = sum(1 for e in empresas if e.get('ativo', False))

    # KPI Row - Institutional Metrics
    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        {"label": "ATIVOS MONITORADOS", "value": active_count, "color": "#f8fafc"},
        {"label": "SINCRONIA HOJE", "value": base_stats.get('consultas_hoje', 0), "color": "var(--federal-blue)"},
        {"label": "TAXA DE REGULARIDADE", "value": f"{base_stats.get('taxa_sucesso', 0)}%", "color": "var(--fgts-green)"},
        {"label": "ALERTA DE RISCO", "value": base_stats.get('alertas_pendentes', 0), "color": "#ef4444"}
    ]

    for i, m in enumerate(metrics):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
                <div class='glass-card' style='border-left: 4px solid {m['color']}; background: #111827; padding: 1.5rem; border-radius: 12px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);'>
                    <div class='system-label' style='color: {m['color']}; opacity: 0.9; font-size: 0.7rem; letter-spacing: 2px;'>{m['label']}</div>
                    <div style='font-size: 2.5rem; font-weight: 900; color: #f8fafc; margin-top: 0.5rem;'>{m['value']}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown("<div class='system-label'>LINHA DO TEMPO — MONITORAMENTO ESTRUTURADO</div>", unsafe_allow_html=True)
        
        chart_data = base_stats.get('chart_data', [])
        if chart_data:
            chart_df = pd.DataFrame(chart_data)
            if 'data' in chart_df.columns:
                chart_df['data_str'] = pd.to_datetime(chart_df['data']).dt.strftime('%d/%m')
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=chart_df['data_str'],
                    y=chart_df['consultas'],
                    mode='lines+markers',
                    line=dict(color='#3b82f6', width=4, shape='spline'),
                    marker=dict(size=10, color='#ffffff', line=dict(color='#3b82f6', width=2)),
                    fill='tozeroy',
                    fillcolor='rgba(59, 130, 246, 0.1)',
                    hovertemplate='<b>DATA: %{x}</b><br>SINCROS: %{y}<extra></extra>'
                ))
                
                fig.update_layout(
                    template='plotly_dark',
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#cbd5e1', size=11, family='Inter'),
                    xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#94a3b8')),
                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', tickfont=dict(color='#94a3b8')),
                    margin=dict(l=0, r=0, t=20, b=0),
                    height=350
                )
                
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("Dados de cronograma indisponíveis.")
        else:
            st.info("Nenhum dado histórico para exibir.")

    with col_side:
        st.markdown("<div class='system-label'>DISTRIBUIÇÃO POR PILAR</div>", unsafe_allow_html=True)
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Federal', 'Estadual', 'FGTS'],
            values=[35, 32, 33],
            hole=0.7,
            marker=dict(colors=['#60a5fa', '#a78bfa', '#34d399']),
            textinfo='label+percent',
            textfont=dict(color='white')
        )])
        
        fig_pie.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            margin=dict(l=20, r=20, t=20, b=20),
            height=350
        )
        
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Critical Events Table
    st.markdown("<div class='system-label'>LOG DE EXCEÇÕES — ÚLTIMAS 24H</div>", unsafe_allow_html=True)

    alertas_recentes = base_stats.get('alertas_recentes', [])
    if alertas_recentes:
        events = []
        for a in alertas_recentes:
            events.append({
                'TIPO': str(a.get('tipo', 'N/A')).upper().replace('CND_', ''),
                'ENTIDADE': str(a.get('empresa_nome', 'N/A')).upper(),
                'TIMESTAMP': format_datetime(a.get('data_execucao', '')),
                'SITUAÇÃO': '⚠️ ALERTA' if a.get('situacao') == 'negativa' else '🚫 FALHA'
            })
        
        st.dataframe(pd.DataFrame(events), use_container_width=True, hide_index=True)
    else:
        st.markdown("""
            <div style='text-align: center; padding: 4rem; background: #0f172a; border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px;'>
                <p style='color: var(--text-muted); font-weight: 500;'>ESTADO DE CONFORMIDADE: NOMINAL</p>
            </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Ocorreu um erro ao carregar o dashboard: {str(e)}")
    st.exception(e)

# Bottom Infrastructure Info
st.markdown("""
    <div style='text-align: center; padding: 3rem 0; border-top: 1px solid var(--border-color); margin-top: 2rem; opacity: 0.5;'>
        <p style='color: var(--text-muted); font-size: 0.7rem; font-family: "JetBrains Mono", monospace; letter-spacing: 0.1em;'>
            AUDIT-DATA-NODE: 0xFD-PR-44 | SYSTEM-HEALTH: STABLE
        </p>
    </div>
""", unsafe_allow_html=True)

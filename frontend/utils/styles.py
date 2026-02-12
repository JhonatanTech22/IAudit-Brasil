"""
Professional Design System for IAudit - Inspired by MonitorHub
Clean, modern, and high-performance light interface.
"""

def get_custom_css():
    return """
    <style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');
    
    /* GOV.BR Dark Design System V2.1 (Elegance & Accessibility) */
    :root {
        --primary-blue: #020617;
        --accent-blue: #1e40af;
        --gov-yellow: #facc15; /* Brighter yellow for better visibility */
        --bg-main: #020617;
        --surface-card: #0f172a;
        --border-color: rgba(255, 255, 255, 0.1); /* Increased opacity for better definition */
        --text-main: #f8fafc;
        --text-muted: #94a3b8; /* Brighter muted text */
        --federal-blue: #3b82f6;
        --state-purple: #8b5cf6;
        --fgts-green: #10b981;
    }

    /* Global Transitions */
    * {
        transition: background-color 0.2s ease, border-color 0.2s ease;
    }

    .stApp {
        background-color: var(--bg-main) !important;
        color: var(--text-main);
    }

    /* Fixing contrast issues - Intelligent Text targeting */
    h1, h2, h3, h4, h5, h6, .system-label, .main-text {
        color: var(--text-main) !important;
    }
    
    /* Allow Streamlit to handle UI components (buttons, inputs) font colors */
    /* but force specific high-contrast for our specialized areas */
    .glass-card h1, .glass-card h2, .glass-card h3, .glass-card h4, .glass-card p {
        color: var(--text-main) !important;
    }

    /* FIX: Ensure tooltips and selectboxes (which might have white backgrounds) are readable */
    div[data-baseweb="popover"] *, div[role="listbox"] *, .stTooltip div {
        color: #0f172a !important; /* Force dark navy text on all popovers/dropdowns */
    }

    /* Input Fields - Text Color Force */
    .stTextInput input, .stSelectbox [data-baseweb="select"] {
        color: #f8fafc !important;
    }

    /* Metrics Styling */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid var(--border-color);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stMetricValue"] {
        color: white !important;
        font-weight: 800 !important;
    }

    </style>
    """

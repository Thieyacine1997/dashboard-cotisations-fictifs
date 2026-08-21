import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard Cotisations", layout="wide")

# --- PALETTE & STYLE ---
GREEN_DARK = "#0B2B20"
GREEN_MED = "#123D2E"
GOLD = "#D4AF37"
GOLD_LIGHT = "#E8C468"
CREAM = "#F5F1E8"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

.stApp {{
    background: linear-gradient(180deg, {GREEN_DARK} 0%, #081F17 100%);
}}
h1, h2, h3 {{
    font-family: 'Fraunces', serif !important;
    color: {GOLD} !important;
}}
p, div, span {{
    font-family: 'IBM Plex Mono', monospace;
    color: {CREAM};
}}
section[data-testid="stSidebar"] {{
    background-color: {GREEN_DARK};
    border-right: 1px solid {GOLD};
}}
</style>
""", unsafe_allow_html=True)

# --- BANNIÈRE D'ACCUEIL ---
st.markdown(f"""
<div style="background:linear-gradient(135deg,{GREEN_MED} 0%,{GREEN_DARK} 100%);
            border:1px solid {GOLD}; border-radius:16px; padding:40px 32px; text-align:center; margin-bottom:24px;">
    <div style="font-family:'Fraunces',serif; color:{GOLD}; font-size:2.4rem; font-weight:700;">DASHBOARD NUMERO UN</div>
    <div style="font-family:'IBM Plex Mono',monospace; color:{CREAM}; font-size:1rem; margin-top:12px;">
        Développé par <span style="color:{GOLD_LIGHT}; font-weight:600;">Thieyacine</span>
    </div>
    <div style="font-family:'IBM Plex Mono',monospace; color:{GOLD_LIGHT}; font-size:0.85rem; margin-top:16px;
                border-top:1px solid {GOLD}; padding-top:14px;">
        ⚠️ Ces données ne sont pas des données réelles — elles ont été générées par l'IA
    </div>
</div>
""", unsafe_allow_html=True)

# --- APERÇU DES PAGES ---
st.markdown(f"""
<div style="font-family:'IBM Plex Mono',monospace; color:{CREAM}; font-size:0.95rem; text-align:center; margin-top:8px;">
    👉 Utilise le menu à gauche pour naviguer entre les pages du dashboard
</div>
""", unsafe_allow_html=True)
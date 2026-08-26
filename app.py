import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dashboard Cotisations", layout="wide")

# --- PALETTE (BLEU / MARRON / BEIGE / NOIR / BLANC) ---
BLACK = "#0B0E14"
BLACK_SOFT = "#121722"
BLUE = "#3B82F6"
BLUE_LIGHT = "#7DA9FA"
BLUE_DEEP = "#1D4ED8"
BROWN = "#8B5E3C"
BROWN_LIGHT = "#B98A63"
BEIGE = "#EADFC8"
WHITE = "#FFFFFF"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@400;500;700&display=swap');

.stApp {{
    background: radial-gradient(1200px 600px at 80% -10%, rgba(59,130,246,.16), transparent 60%),
                radial-gradient(900px 500px at -10% 110%, rgba(139,94,60,.18), transparent 55%),
                linear-gradient(180deg, {BLACK} 0%, #07090D 100%);
    color: {BEIGE};
    font-family: 'Outfit', sans-serif;
}}
h1, h2, h3 {{
    font-family: 'Space Grotesk', sans-serif !important;
    color: {WHITE} !important;
}}
p, div, span {{
    font-family: 'Outfit', sans-serif;
    color: {BEIGE};
}}
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {BLACK_SOFT} 0%, {BLACK} 100%);
    border-right: 1px solid rgba(59,130,246,.35);
}}
section[data-testid="stSidebar"] * {{ color: {BEIGE} !important; }}
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: {BLACK}; }}
::-webkit-scrollbar-thumb {{ background: {BROWN}; border-radius: 8px; }}
</style>
""", unsafe_allow_html=True)

# --- BANNIÈRE D'ACCUEIL ---
st.markdown(f"""
<div style="background:linear-gradient(120deg,{BLACK_SOFT} 0%,#101827 55%,#171310 100%);
            border:1px solid rgba(59,130,246,.3); border-radius:24px;
            padding:56px 40px; text-align:center; margin-bottom:28px; position:relative; overflow:hidden;">
    <div style="position:absolute;right:-70px;top:-70px;width:260px;height:260px;border-radius:50%;
                background:radial-gradient(circle,rgba(59,130,246,.25),transparent 70%);"></div>
    <div style="position:absolute;left:-50px;bottom:-80px;width:220px;height:220px;border-radius:50%;
                background:radial-gradient(circle,rgba(139,94,60,.3),transparent 70%);"></div>
    <div style="font-size:.75rem;font-weight:600;color:{BLUE_LIGHT};letter-spacing:4px;text-transform:uppercase;">
        IPRES · Cotisations
    </div>
    <div style="font-family:'Space Grotesk',sans-serif;color:{WHITE};font-size:3rem;font-weight:800;
                margin-top:10px;letter-spacing:1px;">DASHBOARD NUMÉRO UN</div>
    <div style="width:80px;height:4px;margin:18px auto 0 auto;border-radius:3px;
                background:linear-gradient(90deg,{BLUE},{BROWN});"></div>
    <div style="color:{BEIGE};font-size:1.05rem;margin-top:20px;">
        Développé par <span style="color:{BLUE_LIGHT}; font-weight:600;">Thieyacine</span>
    </div>
    <div style="display:inline-block;margin-top:22px;padding:8px 18px;border-radius:999px;
                background:rgba(139,94,60,.15);border:1px solid rgba(185,138,99,.35);
                color:{BROWN_LIGHT};font-size:.85rem;">
        ⚠️ Ces données ne sont pas des données réelles — elles ont été générées par l'IA
    </div>
</div>
""", unsafe_allow_html=True)

# --- APERÇU DES PAGES ---
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.markdown(f"""
    <div style="background:linear-gradient(150deg,{BLACK_SOFT},#0D1119);
                border:1px solid rgba(59,130,246,.25); border-radius:16px;
                padding:26px 30px; text-align:center; box-shadow:0 12px 32px rgba(0,0,0,.5);">
        <div style="font-size:.72rem;font-weight:600;color:{BLUE_LIGHT};letter-spacing:2px;text-transform:uppercase;">
            Navigation
        </div>
        <div style="color:{BEIGE};font-size:1rem;margin-top:12px;line-height:1.7;">
            👉 Utilise le menu à gauche pour naviguer entre les pages du dashboard
        </div>
        <div style="width:44px;height:3px;margin:16px auto 0 auto;border-radius:3px;
                    background:linear-gradient(90deg,{BLUE},{BROWN});"></div>
    </div>
    """, unsafe_allow_html=True)
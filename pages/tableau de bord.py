import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Tableau de bord — Cotisations", layout="wide")

# --- PALETTE (BLEU / MARRON / BEIGE / NOIR / BLANC) ---
BLACK = "#0B0E14"          # fond principal
BLACK_SOFT = "#121722"     # fond cartes
BLUE = "#3B82F6"           # accent principal
BLUE_LIGHT = "#7DA9FA"
BLUE_DEEP = "#1D4ED8"
BROWN = "#8B5E3C"          # accent secondaire
BROWN_LIGHT = "#B98A63"
BEIGE = "#EADFC8"          # texte doux
WHITE = "#FFFFFF"

PALETTE = [BLUE, BROWN, BLUE_LIGHT, BROWN_LIGHT, BEIGE, BLUE_DEEP, "#5C4033", "#93C5FD", "#D2B48C"]

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
    letter-spacing: .5px;
}}
h1 {{ font-weight: 800 !important; }}
h2, h3 {{ font-weight: 700 !important; }}

p, div, span, label {{
    font-family: 'Outfit', sans-serif;
    color: {BEIGE};
}}

/* --- SIDEBAR --- */
section[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {BLACK_SOFT} 0%, {BLACK} 100%);
    border-right: 1px solid rgba(59,130,246,.35);
}}
section[data-testid="stSidebar"] * {{
    color: {BEIGE} !important;
}}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {{
    color: {BLUE_LIGHT} !important;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 1rem !important;
}}
section[data-testid="stSidebar"] hr {{
    border-color: rgba(185,138,99,.4) !important;
}}

/* --- WIDGETS --- */
div[data-baseweb="select"] > div,
div[data-baseweb="multiselect"] > div,
div[data-baseweb="input"] {{
    background-color: {BLACK_SOFT} !important;
    border: 1px solid rgba(59,130,246,.45) !important;
    border-radius: 10px !important;
}}
span[data-baseweb="tag"] {{
    background-color: {BLUE_DEEP} !important;
    border-radius: 6px !important;
}}
div[data-testid="stPlotlyChart"] {{
    background: linear-gradient(160deg, rgba(18,23,34,.92), rgba(11,14,20,.92));
    border: 1px solid rgba(59,130,246,.22);
    border-radius: 16px;
    padding: 12px 8px 4px 8px;
    box-shadow: 0 10px 30px rgba(0,0,0,.45);
}}

/* --- SCROLLBAR --- */
::-webkit-scrollbar {{ width: 8px; }}
::-webkit-scrollbar-track {{ background: {BLACK}; }}
::-webkit-scrollbar-thumb {{ background: {BROWN}; border-radius: 8px; }}

/* --- BOUTONS --- */
button[kind="primary"] {{
    background: linear-gradient(135deg, {BLUE}, {BLUE_DEEP}) !important;
    border: none !important;
    border-radius: 10px !important;
}}
</style>
""", unsafe_allow_html=True)


# ---------- COMPOSANTS ----------

def metric_card(col, label, value, delta=None, accent=BLUE):
    """Carte KPI moderne avec barre d'accent latérale — hauteur fixe."""
    delta_html = (
        f'<div style="font-size:.82rem;color:{BROWN_LIGHT};margin-top:8px;'
        f'background:rgba(139,94,60,.15);display:inline-block;padding:3px 10px;'
        f'border-radius:999px;border:1px solid rgba(185,138,99,.35);">{delta}</div>'
        if delta else '<div style="height:30px;"></div>'
    )
    col.markdown(f"""
    <div style="position:relative;overflow:hidden;box-sizing:border-box;
                background:linear-gradient(150deg,{BLACK_SOFT} 0%,#0D1119 100%);
                border:1px solid rgba(255,255,255,.08); border-radius:16px;
                padding:20px 20px 16px 26px; height:170px;
                display:flex; flex-direction:column; justify-content:center;
                box-shadow:0 12px 32px rgba(0,0,0,.5);">
        <div style="position:absolute;left:0;top:0;bottom:0;width:5px;
                    background:linear-gradient(180deg,{accent},{BROWN});border-radius:4px;"></div>
        <div style="font-size:.72rem;font-weight:600;color:{BLUE_LIGHT};
                    letter-spacing:2px;text-transform:uppercase;line-height:1.4;
                    display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;">{label}</div>
        <div style="font-family:'Space Grotesk',sans-serif;color:{WHITE};
                    font-size:2rem;font-weight:700;margin-top:8px;line-height:1.1;
                    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{value}</div>
        {delta_html}
        <div style="position:absolute;right:-30px;top:-30px;width:110px;height:110px;border-radius:50%;
                    background:radial-gradient(circle,rgba(59,130,246,.18),transparent 70%);"></div>
    </div>
    """, unsafe_allow_html=True)


def section_header(text):
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:14px;margin:10px 0 4px 0;">
        <div style="width:6px;height:28px;border-radius:4px;
                    background:linear-gradient(180deg,{BLUE},{BROWN});"></div>
        <h2 style="margin:0;font-size:1.35rem;">{text}</h2>
        <div style="flex:1;height:1px;background:linear-gradient(90deg,rgba(59,130,246,.5),rgba(139,94,60,.25),transparent);"></div>
    </div>
    """, unsafe_allow_html=True)


def horizontal_divider():
    st.markdown(f"""
    <hr style="border:none;height:1px;margin:26px 0;
               background:linear-gradient(90deg,transparent,rgba(59,130,246,.45),rgba(139,94,60,.45),transparent);">
    """, unsafe_allow_html=True)


def vertical_divider(mid_col, height=400):
    mid_col.markdown(f"""
    <div style="width:1px;height:{height}px;margin:0 auto;
                background:linear-gradient(180deg,transparent,rgba(59,130,246,.5),rgba(139,94,60,.5),transparent);"></div>
    """, unsafe_allow_html=True)


def style_fig(fig, title, show_legend=False):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit", color=BEIGE, size=13),
        title=dict(
            text=f"<b>{title}</b>",
            font=dict(family="Space Grotesk", size=17, color=WHITE),
            x=0.03, xanchor="left",
        ),
        showlegend=show_legend,
        margin=dict(t=56, b=30, l=20, r=20),
        hoverlabel=dict(bgcolor=BLACK_SOFT, bordercolor=BLUE, font=dict(color=BEIGE, family="Outfit")),
    )
    fig.update_xaxes(gridcolor="rgba(234,223,200,.08)", zerolinecolor="rgba(234,223,200,.15)", linecolor="rgba(234,223,200,.2)")
    fig.update_yaxes(gridcolor="rgba(234,223,200,.08)", zerolinecolor="rgba(234,223,200,.15)", linecolor="rgba(234,223,200,.2)")
    return fig


# ---------- DONNÉES ----------
df = pd.read_excel("data/dataset_ipres.xlsx")

# ---------- TITRE ----------
st.markdown(f"""
<div style="background:linear-gradient(120deg,{BLACK_SOFT} 0%,#101827 55%,#171310 100%);
            border:1px solid rgba(59,130,246,.3); border-radius:20px;
            padding:34px 36px; margin-bottom:10px; position:relative; overflow:hidden;">
    <div style="position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;
                background:radial-gradient(circle,rgba(59,130,246,.25),transparent 70%);"></div>
    <div style="position:absolute;left:-40px;bottom:-70px;width:180px;height:180px;border-radius:50%;
                background:radial-gradient(circle,rgba(139,94,60,.3),transparent 70%);"></div>
    <div style="font-size:.75rem;font-weight:600;color:{BLUE_LIGHT};letter-spacing:3px;text-transform:uppercase;">
        IPRES · Suivi des cotisations
    </div>
    <div style="font-family:'Space Grotesk',sans-serif;color:{WHITE};font-size:2.5rem;
                font-weight:800;margin-top:6px;letter-spacing:1px;">TABLEAU DE BORD</div>
    <div style="width:70px;height:4px;margin-top:14px;border-radius:3px;
                background:linear-gradient(90deg,{BLUE},{BROWN});"></div>
</div>
""", unsafe_allow_html=True)

# ---------- FILTRES (EN HAUT DE PAGE) ----------
filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    regions_disponibles = sorted(df["Region"].unique())
    region_selectionnee = st.selectbox("🌍 Région", ["Tous"] + regions_disponibles)

with filter_col2:
    statuts_disponibles = sorted(df["Statut Cotisation"].unique())
    statut_selectionne = st.selectbox("📋 Statut de cotisation", ["Tous"] + statuts_disponibles)

with filter_col3:
    secteurs_disponibles = sorted(df["Secteur Activite"].unique())
    secteur_selectionne = st.selectbox("🏭 Secteur d'activité", ["Tous"] + secteurs_disponibles)

df_filtre = df.copy()
if region_selectionnee != "Tous":
    df_filtre = df_filtre[df_filtre["Region"] == region_selectionnee]
if statut_selectionne != "Tous":
    df_filtre = df_filtre[df_filtre["Statut Cotisation"] == statut_selectionne]
if secteur_selectionne != "Tous":
    df_filtre = df_filtre[df_filtre["Secteur Activite"] == secteur_selectionne]

if df_filtre.empty:
    st.warning("Aucune donnée ne correspond à ces filtres.")
    st.stop()

section_header("Indicateurs clés")

# ---------- KPIs ----------
cotisation_par_region = df_filtre.groupby("Region")["Cotisation Mensuelle"].agg(["sum", "mean"]).reset_index()
cotisation_par_region.columns = ["Region", "Total", "Moyenne"]
cotisation_par_region = cotisation_par_region.sort_values("Total", ascending=False)

region_qui_cotise_le_plus = cotisation_par_region.loc[cotisation_par_region["Total"].idxmax(), "Region"]
region_qui_cotise_le_moins = cotisation_par_region.loc[cotisation_par_region["Total"].idxmin(), "Region"]
cotisation_globale = df_filtre["Cotisation Mensuelle"].sum()
total_max = cotisation_par_region["Total"].max()
total_min = cotisation_par_region["Total"].min()
moyenne_globale = df_filtre["Cotisation Mensuelle"].mean()

col1, col2, col3 = st.columns(3)
metric_card(col1, "Cotisation globale", f"{cotisation_globale:,.0f}".replace(",", " "),
            f"Moyenne : {moyenne_globale:,.0f}".replace(",", " "), accent=BLUE)
metric_card(col2, "Région la moins contributrice", region_qui_cotise_le_moins,
            f"{total_min:,.0f}".replace(",", " "), accent=BROWN)
metric_card(col3, "Région la plus contributrice", region_qui_cotise_le_plus,
            f"{total_max:,.0f}".replace(",", " "), accent=BLUE_LIGHT)

# ---------- VISUALISATIONS ----------
horizontal_divider()
section_header("Visualisations")

col1, colmid, col2 = st.columns([10, 1, 10])

with col1:
    fig = px.pie(cotisation_par_region, names="Region", values="Total", hole=0.55,
                 color_discrete_sequence=PALETTE)
    fig.update_traces(textinfo="percent", textfont_color=WHITE,
                      marker=dict(line=dict(color=BLACK, width=2)))
    st.plotly_chart(style_fig(fig, "Cotisation par région", show_legend=True), use_container_width=True)

vertical_divider(colmid)

region_effectif = df_filtre.groupby("Region")["Effectif Salaries"].sum().reset_index()
region_effectif.columns = ["Region", "Nombre"]
region_effectif = region_effectif.sort_values("Nombre", ascending=False)
with col2:
    fig = px.bar(region_effectif, y="Region", x="Nombre", orientation="h",
                 color="Region", color_discrete_sequence=PALETTE)
    fig.update_traces(marker_line_color=BLACK, marker_line_width=1, showlegend=False)
    st.plotly_chart(style_fig(fig, "Effectif salarié par région"), use_container_width=True)

impayes = df_filtre.groupby("Region")["Mois Impayes"].sum().reset_index()
impayes.columns = ["Region", "nombre de mois"]
impayes = impayes.sort_values("nombre de mois", ascending=False)

statut = df_filtre["Statut Cotisation"].value_counts().reset_index()
statut.columns = ["Statut cotisation", "nombre"]
statut = statut.sort_values("nombre", ascending=False)

horizontal_divider()
col1, colmid, col2 = st.columns([10, 1, 10])
with col1:
    fig = px.bar(impayes, x="Region", y="nombre de mois",
                 color="Region", color_discrete_sequence=PALETTE)
    fig.update_traces(marker_line_color=BLACK, marker_line_width=1, showlegend=False)
    st.plotly_chart(style_fig(fig, "Mois impayés par région"), use_container_width=True)

vertical_divider(colmid)

with col2:
    fig = px.bar(statut, x="Statut cotisation", y="nombre",
                 color="Statut cotisation", color_discrete_sequence=PALETTE)
    fig.update_traces(marker_line_color=BLACK, marker_line_width=1, showlegend=False)
    st.plotly_chart(style_fig(fig, "Différents statuts de cotisation"), use_container_width=True)

secteur = df_filtre["Secteur Activite"].value_counts().reset_index()
secteur.columns = ["Secteur Activite", "Type"]
secteur = secteur.sort_values("Type", ascending=False)

relance = df_filtre["Dernier Canal Relance"].value_counts().reset_index()
relance.columns = ["Dernier Canal Relance", "nombre"]
relance = relance.sort_values("nombre", ascending=False)

horizontal_divider()
col1, colmid, col2 = st.columns([10, 1, 10])
with col1:
    fig = px.pie(secteur, names="Secteur Activite", values="Type", hole=0.55,
                 color_discrete_sequence=PALETTE)
    fig.update_traces(textinfo="percent", textfont_color=WHITE,
                      marker=dict(line=dict(color=BLACK, width=2)))
    st.plotly_chart(style_fig(fig, "Secteurs d'activité", show_legend=True), use_container_width=True)

vertical_divider(colmid)

with col2:
    fig = px.bar(relance, x="Dernier Canal Relance", y="nombre",
                 color="Dernier Canal Relance", color_discrete_sequence=PALETTE)
    fig.update_traces(marker_line_color=BLACK, marker_line_width=1, showlegend=False)
    st.plotly_chart(style_fig(fig, "Canaux de relance utilisés"), use_container_width=True)
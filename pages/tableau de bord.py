import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")

# --- PALETTE & STYLE ---
GREEN_DARK = "#0B2B20"
GREEN_MED = "#123D2E"
GOLD = "#D4AF37"
GOLD_LIGHT = "#E8C468"
CREAM = "#F5F1E8"
PALETTE = [GOLD, GREEN_MED, GOLD_LIGHT, "#8FBFA3", "#3A6B54", "#6B8F7A", "#C9A227", "#0F4C3A", "#B8860B"]

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

def metric_card(col, label, value, delta=None):
    delta_html = f'<div style="font-size:0.85rem;color:{GOLD_LIGHT};margin-top:6px;">{delta}</div>' if delta else '<div style="font-size:0.85rem;margin-top:6px;">&nbsp;</div>'
    col.markdown(f"""
    <div style="background:linear-gradient(135deg,{GREEN_MED} 0%,{GREEN_DARK} 100%);
                border:1px solid {GOLD}; border-radius:12px; padding:18px 16px; text-align:center;
                min-height:130px; display:flex; flex-direction:column; justify-content:center;">
        <div style="font-family:'IBM Plex Mono',monospace; color:{GOLD_LIGHT}; font-size:0.75rem;
                    letter-spacing:1px; text-transform:uppercase;">{label}</div>
        <div style="font-family:'Fraunces',serif; color:{CREAM}; font-size:1.9rem; font-weight:700; margin-top:6px;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def style_fig(fig, title, show_legend=False):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Mono", color=CREAM),
        title=dict(text=title, font=dict(family="Fraunces", size=18, color=GOLD)),
        showlegend=show_legend,
    )
    return fig

def vertical_divider(mid_col, height=400):
    mid_col.markdown(f"""
    <div style="border-left:1px solid {GOLD}; height:{height}px; margin:0 auto;"></div>
    """, unsafe_allow_html=True)

def horizontal_divider():
    st.markdown(f"""
    <hr style="border:none; border-top:1px solid {GOLD}; margin:28px 0;">
    """, unsafe_allow_html=True)

# --- DONNÉES ---
df = pd.read_excel("data/dataset_ipres.xlsx")

# --- FILTRES (SIDEBAR) ---
st.sidebar.header("Filtres")

regions_disponibles = sorted(df["Region"].unique())
regions_selectionnees = st.sidebar.multiselect("Région", regions_disponibles, default=regions_disponibles)

statuts_disponibles = sorted(df["Statut Cotisation"].unique())
statut_selectionne = st.sidebar.selectbox("Statut de cotisation", ["Tous"] + statuts_disponibles)

secteurs_disponibles = sorted(df["Secteur Activite"].unique())
secteur_selectionne = st.sidebar.selectbox("Secteur d'activité", ["Tous"] + secteurs_disponibles)

df_filtre = df[df["Region"].isin(regions_selectionnees)]
if statut_selectionne != "Tous":
    df_filtre = df_filtre[df_filtre["Statut Cotisation"] == statut_selectionne]
if secteur_selectionne != "Tous":
    df_filtre = df_filtre[df_filtre["Secteur Activite"] == secteur_selectionne]

if df_filtre.empty:
    st.warning("Aucune donnée ne correspond à ces filtres.")
    st.stop()

# --- TITRE ---
st.title("TABLEAU DE BORD")
horizontal_divider()
st.header("INDICATEURS")

# --- KPIs ---
cotisation_par_region = df_filtre.groupby("Region")["Cotisation Mensuelle"].agg(["sum", "mean"]).reset_index()
cotisation_par_region.columns = ["Region", "Total", "Moyenne"]
cotisation_par_region = cotisation_par_region.sort_values("Total", ascending=False)

region_qui_cotise_le_plus = cotisation_par_region.loc[cotisation_par_region["Total"].idxmax(), "Region"]
region_qui_cotise_le_moins = cotisation_par_region.loc[cotisation_par_region["Total"].idxmin(), "Region"]
cotisation_globale = df_filtre["Cotisation Mensuelle"].sum()
total_max = cotisation_par_region["Total"].max()
total_min = cotisation_par_region["Total"].min()
moyenne_globale = df_filtre["Cotisation Mensuelle"].mean()

col1, col2, col3, col4 = st.columns(4)
metric_card(col1, "Cotisation moyenne", f"{moyenne_globale:,.0f}".replace(",", " "))
metric_card(col2, "Cotisation globale", f"{cotisation_globale:,.0f}".replace(",", " "))
metric_card(col3, "Région la moins contributrice", region_qui_cotise_le_moins, f"{total_min:,.0f}".replace(",", " "))
metric_card(col4, "Région la plus contributrice", region_qui_cotise_le_plus, f"{total_max:,.0f}".replace(",", " "))

# --- VISUALISATIONS ---
horizontal_divider()
st.header("Visualisations")
col1, colmid, col2 = st.columns([10, 1, 10])

with col1:
    fig = px.pie(cotisation_par_region, names="Region", values="Total", hole=0.5,
                 color_discrete_sequence=PALETTE)
    st.plotly_chart(style_fig(fig, "Cotisation par région", show_legend=True), use_container_width=True)

vertical_divider(colmid)

region_effectif = df_filtre.groupby("Region")["Effectif Salaries"].sum().reset_index()
region_effectif.columns = ["Region", "Nombre"]
region_effectif = region_effectif.sort_values("Nombre", ascending=False)
with col2:
    fig = px.bar(region_effectif, y="Region", x="Nombre", orientation="h",
                 color="Region", color_discrete_sequence=PALETTE)
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
    st.plotly_chart(style_fig(fig, "Mois impayés par région"), use_container_width=True)

vertical_divider(colmid)

with col2:
    fig = px.bar(statut, x="Statut cotisation", y="nombre",
                 color="Statut cotisation", color_discrete_sequence=PALETTE)
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
    fig = px.pie(secteur, names="Secteur Activite", values="Type", hole=0.5,
                 color_discrete_sequence=PALETTE)
    st.plotly_chart(style_fig(fig, "Secteurs d'activité", show_legend=True), use_container_width=True)

vertical_divider(colmid)

with col2:
    fig = px.bar(relance, x="Dernier Canal Relance", y="nombre",
                 color="Dernier Canal Relance", color_discrete_sequence=PALETTE)
    st.plotly_chart(style_fig(fig, "Canaux de relance utilisés"), use_container_width=True)
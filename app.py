import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")
df = pd.read_excel("data/dataset_ipres.xlsx")

st.title("DASHBOARD NUMERO UN")
st.header("ces donnees sont pas des donnees reelles")

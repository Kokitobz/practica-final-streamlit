import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

import pandas as pd
import streamlit as st
import gdown
import os

FILE_ID = "1I--5yCp9dw0iYpZuGMyMNM6pYnpQac-5"
URL = f"https://drive.google.com/uc?id={FILE_ID}"
OUTPUT = "parte_1.csv"

@st.cache_data
def load_data():
    if not os.path.exists(OUTPUT):
        gdown.download(URL, OUTPUT, quiet=False)
    df = pd.read_csv(OUTPUT, parse_dates=["date"])
    return df

df = load_data()

st.title("📊 Visión Global de las Ventas")

tab1, = st.tabs(["Resumen General"])

col1, col2, col3, col4 = st.columns(4)

total_tiendas = df["store_nbr"].nunique()
total_productos = df["family"].nunique()
total_estados = df["state"].nunique()
total_meses = df[["year", "month"]].drop_duplicates().shape[0]

col1.metric("🏬 Tiendas", total_tiendas)
col2.metric("📦 Productos", total_productos)
col3.metric("🗺️ Estados", total_estados)
col4.metric("📆 Meses con datos", total_meses)

top_productos = (
    df.groupby("family")["sales"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

st.subheader("🔝 Top 10 productos más vendidos (media)")
st.bar_chart(top_productos)

ventas_tienda = df.groupby("store_nbr")["sales"].mean()

st.subheader("🏬 Distribución media de ventas por tienda")
fig, ax = plt.subplots()
ax.boxplot(ventas_tienda)
ax.set_ylabel("Ventas medias")
st.pyplot(fig)

promo_df = df[df["onpromotion"] > 0]

top_tiendas_promo = (
    promo_df.groupby("store_nbr")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.subheader("🔥 Top 10 tiendas con más ventas en promoción")
st.bar_chart(top_tiendas_promo)

ventas_dia = (
    df.groupby("day_of_week")["sales"]
    .mean()
    .sort_values(ascending=False)
)

st.subheader("📅 Ventas medias por día de la semana")
st.bar_chart(ventas_dia)

ventas_semana = (
    df.groupby("week")["sales"]
    .mean()
)

st.subheader("📈 Ventas medias por semana del año")
st.line_chart(ventas_semana)

ventas_mes = (
    df.groupby("month")["sales"]
    .mean()
)

st.subheader("📆 Ventas medias por mes")
st.line_chart(ventas_mes)

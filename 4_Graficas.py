import pandas as pd 
import streamlit as st 
import plotly.express as px 

st.set_page_config(page_title="Árboles San Francisco", layout="centered")

st.title("SF Trees")
st.write("Esta aplicación analiza árboles de San Francisco")

trees_df = pd.read_csv("trees.csv")
trees_df["dbh"] = pd.to_numeric(trees_df["dbh"], errors="coerce")
df_non_null = trees_df.dropna(subset=["dbh"])

st.write(df_non_null.head())

df_dhb_grouped = pd.DataFrame(df_non_null.groupby(["dbh"]).count()["tree_id"])

st.subheader("Gráfico de líneas con Streamlit")
st.line_chart(df_dhb_grouped, x_label="Diámetro del árbol", y_label="Cantidad de árboles")

st.subheader("Gráfico de barras con Streamlit")
st.bar_chart(df_dhb_grouped, x_label="Diámetro del árbol", y_label="Cantidad de árboles")

st.subheader("Gráfico de áreas con Streamlit")
st.area_chart(df_dhb_grouped, x_label="Diámetro del árbol", y_label="Cantidad de árboles")

names = "legal_status"
st.subheader("Distribución del status de los árboles (Pastel con plotly)")
fig = px.pie(trees_df, names=names, title= f"Distribución de {names}")
st.plotly_chart(fig)

fig2 = px.histogram(df_non_null, x="dbh", nbins=20, title="Distribución")
st.plotly_chart(fig2)

fig3 = px.bar(df_non_null.head(50), x="caretaker", color="dbh",
              title="Cantidad de árboles y diámetro promedio por responsable",
              labels={"caretaker": "Responsable", "count": "Cantidad de árboles", "dbh": "Diámetro promedio"})

st.plotly_chart(fig3)

trees_df = trees_df.dropna(subset=["longitude", "latitude"])
trees_df = trees_df.sample(n=1000)
st.subheader("Geolocalización de árboles de San Francisco")
st.map(trees_df)
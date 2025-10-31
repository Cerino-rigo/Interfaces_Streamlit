import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt 
import numpy as np 

df = pd.read_csv('projects.csv', encoding='latin1')
df = df.iloc[:-2].copy()
df['Percent complete'] = pd.to_numeric(df['Percent complete'], errors='coerce')

#Creación de variables para los widgets
areas = df['Geographical scope'].unique().tolist()
estados = df['State'].dropna().unique().tolist()

###Sidebar
st.sidebar.title("Controles y Filtros")

#Selector de área
area = st.sidebar.selectbox("Selecciona área:", ["Todas"] + areas)
if area != "Todas":
    dff = df[df['Geographical scope'] == area]
else:
    dff = df.copy()

#Filtro de estado
estado = st.sidebar.selectbox("Estado del proyecto:", ["Todos"] + estados)
if estado != "Todos":
    dff = dff[dff['State'] == estado]

rango = st.sidebar.slider("Rango de avance (%)", 0, 100, (0, 100), step=5)
dff = dff[(dff['Percent complete'] >= rango[0]) & (dff['Percent complete'] <= rango[1])]

#Mostrar métrcias rápidas en sidebar
st.sidebar.metric("Total proyectos", len(dff))

#Main area

st.title("Rango de avance de proyectos 📈")

col_target = 'Percent complete'
datos = dff[col_target].dropna()

bins = st.slider("Número de bins para el histograma", 5, 30, 20)

hist, edges = np.histogram(datos, bins=bins, range=(0, 100))
etiquetas = [f"{edges[i]:.0f} - {edges[i+1]:.0f}%"for i in range(len(edges)-1)]

fig, ax = plt.subplots(figsize=(8,4))
ax.bar(range(len(hist)), hist, width=0.8, color="#4c8bf5", align='center')
ax.set_xticks(range(len(hist)))
ax.set_xticklabels(etiquetas, rotation=45)
ax.set_xlabel("Rango de avance (%)")
ax.set_ylabel("Frecuencia")
ax.set_title("Distribución de Percent complete (filtrados)")
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)

with st.sidebar.expander("Ayuda y descripción"):
    st.write("""
        -Usa los selectores para filtrar área, estado y rango de avance.
        -El tipo de visualización principal se ajusta con el control superior.
        """)
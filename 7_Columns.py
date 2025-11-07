import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt 
import numpy as np 
import plotly.express as px 

df = pd.read_csv('projects.csv', encoding='latin1')
df = df.iloc[:-2].copy()
df['Percent complete'] = pd.to_numeric(df['Percent complete'], errors='coerce')

#Creación de variables para los widgets
areas = df['Geographical scope'].unique().tolist()
estados = df['State'].dropna().unique().tolist()

st.title("Despliegue de columnas")

st.subheader("Ejemplo con proporciones iguales")

col1, col2 = st.columns(2, gap="large", vertical_alignment="center")

with col1:
    st.write("**Filtros**")

    selected_area = st.selectbox("Selecciona un área: ", areas)
    selected_states = st.selectbox("Selecciona un estado: ", estados)

with col2:
    st.write("**Distribución de avance de proyectos**")
    df_filtered = df[(df['Geographical scope'] == selected_area) & (df['State'] == selected_states)]
    
    if not df_filtered.empty:
        fig = px.histogram(df_filtered, x='Percent complete', nbins=15,
                           title=f"Avance en {selected_area} - Estado: {selected_states}"
                           )
        st.plotly_chart(fig)
    else:
        st.info("No hay datos para esta combinación")

col1, col2 = st.columns([0.75, 0.25],border=True)

with col1:

    if not df_filtered.empty:
        estado_counts = df_filtered['State'].value_counts()
        fig = px.bar(
            x=estado_counts.values,
            y=estado_counts.index,
            orientation='h', 
            labels={'x': 'Cantidad', 'y': 'Estado'}
        )
        fig.update_layout(height=200)
        st.plotly_chart(fig)
    else:
        st.info("No hay datos para mostrar")
    
with col2:
    st.write("**Métrica**")
    num_projects = len(df_filtered)
    avg_progress = df_filtered['Percent complete'].mean() if num_projects > 0 else 0
    st.metric(label="Número de proyectos", value=num_projects)
    st.metric(label="Avance promedio (%)", value=f"{avg_progress:.2f}")
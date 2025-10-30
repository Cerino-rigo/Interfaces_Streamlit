import pandas as pd 
import streamlit as st 
import plotly.express as px 
import numpy as np 

st.title("Widgets interactivos de Streamlit con proyectos reales 🚦")

df = pd.read_csv('projects.csv', encoding='latin1')
df['Percent complete'] = pd.to_numeric(df['Percent complete'], errors='coerce')

#Creación de variables para los widgets
areas = df['Geographical scope'].unique().tolist()
estados = df['State'].dropna().unique().tolist()
managers = df['Project manager'].dropna().unique().tolist()

st.markdown('### Checkbox: Mostrar tabla')
if st.checkbox('¿Mostrar tabla de los primeros proyectos?'):
    st.dataframe(df.head(10))

st.markdown('### Radio: Elegir estado del proyecto')
estado_seleccionado = st.radio(
    'Selecciona el estado del proyecto: ',
    options= estados,
    horizontal=True #Coloca los radioitems de forma horizontal
)
st.write(f"Mostrando los proyectos con estado: **{estado_seleccionado}**")
st.dataframe(df[df['State'] == estado_seleccionado][['Number', 'Project Name', 'Percent complete']].head(5))

st.markdown('### Selectbox: Filtra por Área/Ubicación')
area_elegida = st.selectbox(
    'Filtra los proyectos por área',
    options= areas
)

df_filtrado = df[df['Geographical scope'] == area_elegida]
st.write(f"Proyectos en el área seleccionada: **{area_elegida}**")
st.dataframe(df_filtrado[['Number', 'Project Name', 'Project manager', 'Percent complete']])

st.markdown('### Multiselect: Selección múltiple de Project Managers')
pms = st.multiselect(
    'Selecciona uno o más Project Managers:', 
    options= managers,
    default=managers[:2]
)

df_pms = df[df['Project manager'].isin(pms)]
st.write(f"Proyectos a cargo de {', '.join(pms)}:")
st.dataframe(df_pms[['Number', 'Project Name', 'Project manager', 'Percent complete']].head(8))

st.markdown('### Slider: Rango de progeso (%)')
min_prog, max_prog = st.slider(
    'Filtra proyectos por rango de avance (%)',
    0,100, (0, 50), step=5
)

df_rango = df[(df['Percent complete'] >= min_prog) & (df['Percent complete'] <= max_prog)]
st.write(f"Mostrando {len(df_rango)} proyectos con avance entre {min_prog}% y {max_prog}%")
st.dataframe(df_rango[['Number', 'Project Name', 'Percent complete']].head(10))

st.markdown('### Select Slider: Evaluación global de desempeño')
opciones = ['Malo', 'Regular', 'Aceptable', 'Bueno', 'Excelente']
desempeno = st.select_slider(
    '¿Cómo clasificarías el avance promedio de estos proyectos?',
    options= opciones, 
    value= 'Bueno'
)
st.success(f"Evaluación seleccionada: **{desempeno}**")

st.markdown("---")
st.subheader("Gráfica depende de los filtros (Widget-driven)")

if not df_filtrado.empty:
    fig = px.histogram(df_filtrado, x='Percent complete', nbins=10,
                       title=f"Distribución del avance en {area_elegida}")
    st.plotly_chart(fig)

st.markdown('### Text input: Búsqueda flexible')
buscar = st.text_input('Buscar palabra clave en Project Name:')
if buscar: 
    resultados = df[df['Project Name'].str.contains(buscar, case=False, na=False)]
    #case=False la búsqueda es insensible a mayúsculas o minúsculas
    #na=False si hay valores nulos, se tratan como no coincidentes
    st.write(f"Resultados para '{buscar}':")
    st.dataframe(resultados[['Number', 'Project Name', 'Percent complete']].head(10))

st.markdown('### Number input: Filtro de progreso mínimo')
minimo = st.number_input('Progreso mínimo del proyecto (%)', min_value=0, max_value=100, value=10)
df_filtramin = df[df['Percent complete'] >= minimo]
st.write(f"Mostrando proyectos con progreso >= **{minimo}%**")  
st.dataframe(df_filtramin[['Number', 'Project Name', 'Percent complete']].head(5))

st.markdown('### Selecciona columnas eje X y eje Y para graficar (solo columnas relevantes)')
numeric_options = ['Percent complete']
categorical_options = [c for c in ['Project size', 'Project Type', 'Geographical scope', 'Project manager', 'State'] if c in df.columns]

eje_x = st.selectbox("Selecciona columna para eje X", numeric_options + categorical_options, index=0)
eje_y = st.selectbox("Selecciona columna para eje Y", numeric_options, index=0 )

if eje_x and eje_y:
    st.markdown(f"#### Gráfica: {eje_y} vs {eje_x}")
    if eje_x in numeric_options and eje_y in numeric_options: 
        st.plotly_chart(px.scatter(df, x=eje_x, y=eje_y, title=f"{eje_y} vs {eje_x}"))
    elif eje_x in categorical_options and eje_y in numeric_options: 
        st.plotly_chart(px.box(df, x=eje_x, y=eje_y, title=f"{eje_y} vs {eje_x}"))
    elif eje_x in numeric_options and eje_y in categorical_options: 
        st.plotly_chart(px.box(df, x=eje_x, y=eje_y, title=f"{eje_y} vs {eje_x}"))
    else:
        st.warning("Selecciona al menos un eje numérico para la gráfica")

    st.markdown("---")
    st.caption("Demostración de widgets Streamlit con datos de proyectos reales 2025")

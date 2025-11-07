import pandas as pd 
import streamlit as st 
import plotly.express as px 

#Cargar datos con cache para mejorar el rendimiento
@st.cache_data

def load_data():
    #Esta operación costosa solo se ejecutará la primera vez
    return pd.read_csv('projects.csv', encoding='latin1')

df = load_data()
df = df.iloc[:-2].copy()
df['Percent complete'] = pd.to_numeric(df['Percent complete'], errors='coerce')

def centered_title(text):
    st.markdown(f"<h1 style='text-aling: center;'>{text}</h1>", unsafe_allow_html=True)

centered_title("Ejemplo de pestañas con datos reales de proyectos")

#Crear pestañas con etiquetas
tab1, tab2, tab3 = st.tabs([
    "✅ Datos básicos",
    "📊 Visualización de Avance",
    "📝 Notas y Comentarios"
])

with tab1:
    st.header("Información de proyectos")
    st.write("Vista previa de algunos proyectos")
    st.dataframe(df[['Number', 'Project Name', 'Project manager', 'Percent complete']].head(10))

with tab2:
    st.header("Análisis interactivo del avance")
    #Creación de variables para los widgets
    areas = df['Geographical scope'].unique().tolist()
    estados = df['State'].dropna().unique().tolist()

    estado_seleccionado =st.selectbox("Filtrar por estado:", options=["Todos"] + estados)
    area_seleccionada =st.selectbox("Filtrar por área:", options=["Todas"] + areas)

    df_filtrado = df.copy()

    if estado_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado['State'] == estado_seleccionado]

    if area_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado['Geographical scope'] == area_seleccionada]

    st.write(f"Proyectos después de los filtros: {len(df_filtrado)}")

    if not df_filtrado.empty:
        fig = px.histogram(df_filtrado, x='Percent complete',
                           nbins=20, title='Distribución del proyecto de avance')
        st.plotly_chart(fig)
    else:
        st.info("No hay datos para mostrar con estos filtros")

with tab3:
    st.header("Notas y comentarios")
    comentario = st.text_area("Escribe y guarda tus observaciones aquí: ", height=100)
    if comentario:
        st.success("¡Comentario registrado!")
        st.write(comentario)
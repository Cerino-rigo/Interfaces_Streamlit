import streamlit as st 

#Título principal
st.title("📘 Demostración de tipos de texto en Streamlit")
st.markdown("---")

st.header("Introducción") #Encabezado
st.write("""
En esta aplicación mostraremos cómo **Streamlit** permite presentar distintos tipos de texto
para construir interfaces informativas en proyectos de **IA** y **Amalítica de datos**.
"""
)

st.subheader("Texto con Markdown")
st.markdown("""
Con **Markdown**, podemos dar formato al texto, por ejemplo:
            
- **Negritas** y *cursivas*
- Listas con viñetas
- Citas y enlaces
- Tablas de datos
- Inclusión de emojis 🎯
            
> *La analítica de datos combina estadísticas, programación y visualización.*
""")
#Caption y divisores
st.caption("Tip: Markdown es ideal para agregar descripciones, explicaciones y notas informativas")
st.markdown("---")

##Ejemplos de código
st.header("Inclusión de fragmentos de código")
st.code("""
import pandas as pd

#Cargar datos
df = pd.read_csv("ventas.csv")
        
#Calcular métricas básicas
df.describe()
""")

st.subheader("Resolver la siguiente ecuación: ")
st.latex(r' a+a r^1+a r^2+a r^3 r**2')
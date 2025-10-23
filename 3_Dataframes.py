import streamlit as st
import pandas as pd 
import numpy as np 

#Configurar página
st.set_page_config(
    page_title="Generador de DataFrames",
    page_icon="📊",
    #layout="wide",
    layout="centered",
    menu_items={
        'Get Help': 'https://www.faurecia-mexico.mx/acerca-de-nosotros/descubre-faurecia-mexico',
        'About': "Dashbard profesional para gestión de proyectos \nPRMSnow KPIs"
    }

)

st.title("Visualización de proyectos")
sheet_name = "WAR"

dataframe = pd.read_excel("PRMSnow KPIs_062025_modified2.xlsx",
                          sheet_name= sheet_name)

st.dataframe(dataframe) #Desplegar un dataframe

def convert_df(df): #Función para convertir a CSV
    return df.to_csv().encode("utf-8")

csv = convert_df(dataframe)

#Creamos un botón de descarga
st.download_button(
    label= (f"Descargar datos como CSV"),
    data=csv, 
    file_name=(f"{sheet_name}" + ".csv"),
    mime= "text/csv"
)


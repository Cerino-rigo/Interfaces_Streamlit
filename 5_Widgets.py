import pandas as pd 
import streamlit as st 
import plotly.express as px 
import numpy as np 

st.title("Widgets interactivos de Streamlit con proyectos reales 🚦")

df = pd.read_csv('projects.csv', encoding='latin1')
df['']
import streamlit as st 

def filter_percentage(df, regiones, grupo):
    df_filtered = df.copy()
    if regiones:
        df_filtered = df_filtered[df_filtered['Region'].isin(regiones)]
    if grupo and grupo != 'Todos':
        df_filtered = df_filtered[df_filtered['Group'] == grupo]

    return df_filtered

def filter_projects(df, estados, areas, avance_min):
    df_filtered = df.copy()
    if estados:
        df_filtered = df_filtered[df_filtered['State'].isin(estados)]
    if areas and "Todas" not in areas:
        df_filtered = df_filtered[df_filtered['Geographical scope'].isin(areas)]
    df_filtered = df_filtered[df_filtered['Percent complete'] >= avance_min]
    avg_progress = df_filtered['Percent complete'].mean() if len(df_filtered) > 0 else 0
    return df_filtered, avg_progress


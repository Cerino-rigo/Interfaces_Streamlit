import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

st.set_page_config(page_title="Dashboard de Porcentaje No Actualizado", layout="wide")

# CSS personalizado
#background: linear-gradient; Crea un degradado lineal diagonal desde la esquina superior izquierda
#color: white; El texto del botón será blanco.
#padding: Espaciado interno
#font-weight: 600; Texto semipremium (semi-negrita)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
        text-align: center;
        padding: 1rem 0;
        margin-bottom: 1.5rem;
    }
    
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
        color: white; 
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv('percentage_not_completed.csv')
    return df

data = load_data()

#session_state es un diccionario persistente que Streamlit mantiene durante la sesión del usuario.
#  Permite conservar valores entre ejecuciones de la app (renders). Es la forma recomendada de 
# mantener estado en una aplicación Streamlit, ya que la propia ejecución de la app se “recalcula” 
# cada vez que el usuario interactúa con un widget.

# Estado de sesión para el carrusel
if 'grafica_index' not in st.session_state:
    st.session_state.grafica_index = 0

# Header principal
st.markdown('<h1 class="main-header">📊 Dashboard de Análisis por Región</h1>', unsafe_allow_html=True)

# CONTENEDOR 1: Métricas Generales con columnas internas
with st.container(border=True):
    st.subheader("📈 Resumen General del Dataset")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Registros", len(data))
    
    with col2:
        st.metric("Regiones", data['Region'].nunique())
    
    with col3:
        st.metric("Grupos", data['Group'].nunique())
    
    with col4:
        st.metric("Semanas (CW)", data['CW'].nunique())

# CONTENEDOR 2: Carrusel de Gráficas con columnas
with st.container(border=True):
    st.subheader("🎯 Análisis por Grupo - Navegación de Gráficas")
    
    col_left, col_graph, col_right = st.columns([1, 6, 1])
    
    # Lista de grupos para el carrusel
    grupos = ['Gate Review', 'WAR', 'GoLive']
    grupo_actual = grupos[st.session_state.grafica_index]
    
    with col_left:
        st.write("")
        st.write("")
        if st.button("⬅️ Anterior"):
            st.session_state.grafica_index = (st.session_state.grafica_index - 1) % len(grupos)
            st.rerun()
    
    with col_graph:
        st.markdown(f"### Gráfica Actual: **{grupo_actual}**")
        
        # Filtrar datos por grupo
        selected_data = data[data['Group'] == grupo_actual]
        pivot = selected_data.pivot(index='Region', columns='CW', values='valor')
        pivot_percent = (abs(pivot - 1) * 100).round(2)
        
        # Crear gráfica con matplotlib (estilo notebook)
        fig, ax = plt.subplots(figsize=(10, 5))
        
        for region in pivot_percent.index:
            ax.plot(pivot_percent.columns, pivot_percent.loc[region], 
                   marker='o', linewidth=2, label=region)
        
        ax.set_ylabel('Not Updated (%)')
        ax.set_xlabel('Calendar Week (CW)')
        ax.set_title(f'{grupo_actual} - Updated by Region')
        ax.legend(title='Region', bbox_to_anchor=(1.05, 0.5), loc='center left')
        ax.grid(True, axis='y', linestyle='--', alpha=0.5)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter(decimals=0))
        plt.tight_layout()
        
        st.pyplot(fig)
        
        # Info adicional
        st.info(f"📊 Mostrando gráfica {st.session_state.grafica_index + 1} de {len(grupos)}: **{grupo_actual}**")
    
    with col_right:
        st.write("")
        st.write("")
        if st.button("Siguiente ➡️"):
            st.session_state.grafica_index = (st.session_state.grafica_index + 1) % len(grupos)
            st.rerun()

# CONTENEDOR 3: Tabla de datos con filtros en columnas
with st.container(border=True):
    st.subheader("📋 Exploración de Datos")
    
    col_filters, col_table = st.columns([1, 3])
    
    with col_filters:
        st.markdown("#### 🔍 Filtros")
        region_filter = st.multiselect("Región", data['Region'].unique(), default=data['Region'].unique())
        group_filter = st.multiselect("Grupo", data['Group'].unique(), default=data['Group'].unique())
        
        # Mostrar stats de filtros aplicados
        st.markdown("---")
        st.markdown("**Registros filtrados:**")
        filtered_count = len(data[(data['Region'].isin(region_filter)) & (data['Group'].isin(group_filter))])
        st.write(f"{filtered_count} / {len(data)}")
    
    with col_table:
        # Aplicar filtros
        df_filtered = data[(data['Region'].isin(region_filter)) & (data['Group'].isin(group_filter))]
        
        st.dataframe(
            df_filtered.head(20),
            use_container_width=True,
            hide_index=True
        )
        
        # Botón de descarga
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar datos filtrados (CSV)",
            data=csv,
            file_name='datos_filtrados.csv',
            mime='text/csv'
        )

# CONTENEDOR 4: Comparación visual con columnas
with st.container(border=True):
    st.subheader("⚖️ Comparación Regional")
    
    col_comp1, col_comp2 = st.columns(2)
    
    with col_comp1:
        st.markdown("#### Promedio por Región")
        avg_by_region = data.groupby('Region')['valor'].mean().sort_values(ascending=False)
        fig_bar = px.bar(
            x=avg_by_region.values * 100,
            y=avg_by_region.index,
            orientation='h',
            labels={'x': 'Promedio (%)', 'y': 'Región'},
            title='Promedio de valor por Región'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_comp2:
        st.markdown("#### Distribución por Grupo")
        group_counts = data['Group'].value_counts()
        fig_pie = px.pie(
            names=group_counts.index,
            values=group_counts.values,
            title='Distribución de registros por Grupo'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# Footer
st.markdown("---")
st.caption("📊 Dashboard creado con Streamlit - Análisis de porcentaje no completado por región")

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração do layout do Streamlit
st.set_page_config(
    page_title="Dashboard de Baseball Profissional",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Função para carregar os dados
@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()  # Remove espaços extras nos nomes das colunas
    return data

# Carregar os dados
data = load_data('baseball.csv')

# Sidebar - Configurações
st.sidebar.title("Configurações do Dashboard")
st.sidebar.write("Personalize as informações exibidas no dashboard.")

# Filtros dinâmicos
# Filtro por Time
if 'Team' in data.columns:
    teams = data['Team'].dropna().unique()
    selected_teams = st.sidebar.multiselect("Selecione um ou mais Times", options=sorted(teams), default=teams)
    filtered_data = data[data['Team'].isin(selected_teams)]
else:
    st.sidebar.error("A coluna 'Team' não foi encontrada no dataset.")
    filtered_data = data

# Filtro por Ano
if 'Year' in data.columns:
    year_range = st.sidebar.slider(
        "Selecione o Período de Análise", 
        min_value=int(data['Year'].min()), 
        max_value=int(data['Year'].max()), 
        value=(int(data['Year'].min()), int(data['Year'].max()))
    )
    filtered_data = filtered_data[(filtered_data['Year'] >= year_range[0]) & (filtered_data['Year'] <= year_range[1])]

# Título do Dashboard
st.title("📊 Dashboard de Baseball Profissional")
st.markdown(
    """
    Bem-vindo ao dashboard interativo de Baseball! Aqui você pode:
    - Visualizar dados detalhados de times e jogadores.
    - Explorar gráficos dinâmicos e estatísticas em tempo real.
    - Personalizar sua análise com filtros avançados.
    """
)

# Métricas Gerais
st.subheader("⚖ Métricas Gerais")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Jogadores Totais", len(filtered_data))
with col2:
    st.metric("Times Representados", filtered_data['Team'].nunique() if 'Team' in data.columns else "N/A")
with col3:
    st.metric("Período", f"{year_range[0]} - {year_range[1]}" if 'Year' in data.columns else "N/A")
with col4:
    st.metric("Playoffs", int(filtered_data['Playoffs'].sum()) if 'Playoffs' in data.columns else "N/A")

# Gráficos Interativos
# Distribuição de Jogadores por Time
if 'Team' in filtered_data.columns:
    st.subheader("🔖 Distribuição de Jogadores por Time")
    fig_team = px.histogram(
        filtered_data, 
        x='Team', 
        title='Distribuição de Jogadores por Time', 
        text_auto=True, 
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    st.plotly_chart(fig_team, use_container_width=True)

# Vitórias x Derrotas
if all(col in filtered_data.columns for col in ['W', 'L', 'Team']):
    st.subheader("🔖 Vitórias e Derrotas por Time")
    fig_wl = px.bar(
        filtered_data,
        x='Team',
        y=['W', 'L'],
        barmode='group',
        title='Comparativo de Vitórias e Derrotas por Time',
        labels={'value': 'Quantidade', 'variable': 'Categoria'},
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_wl, use_container_width=True)

# Runs Scored e Runs Allowed
if all(col in filtered_data.columns for col in ['Year', 'RS', 'RA']):
    st.subheader("🔖 Runs Scored (RS) e Runs Allowed (RA)")
    fig_runs = px.line(
        filtered_data,
        x='Year',
        y=['RS', 'RA'],
        title='Pontos Marcados e Permitidos ao Longo dos Anos',
        labels={'value': 'Pontos', 'variable': 'Categoria'},
        color_discrete_sequence=px.colors.qualitative.Set1,
        markers=True
    )
    st.plotly_chart(fig_runs, use_container_width=True)

# Estatísticas de Jogadores por Time
if 'Player' in filtered_data.columns:
    st.subheader("🔖 Estatísticas de Jogadores por Time")
    player_stats = filtered_data.groupby('Team').agg({'Player': 'count'}).reset_index()
    fig_player_stats = px.bar(
        player_stats,
        x='Team',
        y='Player',
        title='Total de Jogadores por Time',
        text_auto=True,
        color='Player',
        color_continuous_scale=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig_player_stats, use_container_width=True)

# Dados Brutos e Estatísticas Descritivas
st.subheader("⚖ Dados e Estatísticas Detalhadas")
with st.expander("Visualizar Dados Brutos"):
    st.dataframe(filtered_data)

with st.expander("Visualizar Estatísticas Descritivas"):
    st.write(filtered_data.describe())

# Informações Personalizadas
st.sidebar.markdown("---")
st.sidebar.info(
    """
    **Sobre o Dashboard**  
    - Desenvolvido com foco em análise empresarial e visualização de dados.
    - Criado utilizando Python, Streamlit e Plotly.
    """
)

st.sidebar.markdown("---")
st.sidebar.success("📨 Para dúvidas ou feedback, entre em contato.")

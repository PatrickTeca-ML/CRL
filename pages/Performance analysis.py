import streamlit as st
import pandas as pd
import plotly.express as px
from dataset import data  # Importa o DataFrame diretamente do módulo dataset


def run_page(data):
    # Configuração da página
    st.set_page_config(
        layout="wide", page_title="Sales Performance Analysis", page_icon="📊")

    # Cabeçalho com título e logo
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.title("Sales Performance Analysis")
    with col2:
        st.image(
            "CRL.png",  # Caminho para o arquivo do logo
            width=80
        )

    # Barra lateral com filtros
    st.sidebar.header("Filters")

    # Calcular o desempenho total por Opportunity Owner
    owner_performance = (
        data.groupby('Opportunity Owner')['Amount']
        .sum()
        .sort_values(ascending=False)
    )

    # Determinar os Top 10 Opportunity Owners com base no total de Amount
    top_10_owners = owner_performance.head(10).index.tolist()

    # Filtro de Opportunity Owners
    selected_owners = st.sidebar.multiselect(
        "Select Opportunity Owners:",
        options=owner_performance.index.tolist(),
        default=top_10_owners
    )

    # Aplicar filtro no DataFrame
    filtered_data = data[data['Opportunity Owner'].isin(selected_owners)]

    # Abas para as análises
    tab1, tab2 = st.tabs(["Opportunity Owners", "Opportunities by Stage"])

    # Aba 1: Opportunity Owners
    with tab1:
        st.header("Performance by Opportunity Owners")

        # Recalcular os valores com base nos proprietários selecionados
        owner_performance_filtered = (
            filtered_data.groupby('Opportunity Owner')['Amount']
            .sum()
            .sort_values(ascending=False)
        )

        # Gráfico de barras interativo com Plotly
        st.subheader("Top Opportunity Owners by Total Amount (Filtered)")
        bar_chart = px.bar(
            owner_performance_filtered.head(10).reset_index(),
            x="Amount",
            y="Opportunity Owner",
            orientation="h",
            title="Top Opportunity Owners by Total Amount",
            labels={
                "Amount": "Total Amount", "Opportunity Owner": "Owner"},
            color="Amount",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(bar_chart, use_container_width=True)

    # Aba 2: Opportunities by Stage
    with tab2:
        st.header("Opportunities by Stage")

        # Contar a quantidade de oportunidades por estágio
        stage_counts = (
            filtered_data['Stage']
            .value_counts()  # Conta as ocorrências de cada estágio
            .reset_index()  # Converte para DataFrame
        )
        # Renomeia as colunas
        stage_counts.columns = ['Stage', 'Opportunities']

        # Debugging para verificar o conteúdo do DataFrame
        st.write("Debugging stage_counts DataFrame:")
        st.write(stage_counts)

        # Gráfico de barras interativo com Plotly
        bar_chart_stage = px.bar(
            stage_counts,
            x="Opportunities",  # Contagem de oportunidades no eixo x
            y="Stage",  # Estágios no eixo y
            orientation="h",  # Gráfico horizontal
            title="Opportunities Distribution by Stage",
            labels={"Opportunities": "Number of Opportunities", "Stage": "Stage"},
            color="Opportunities",  # Coloração baseada na contagem
            color_continuous_scale="Viridis"  # Esquema de cores
        )
        st.plotly_chart(bar_chart_stage, use_container_width=True)

        # Explicações
        st.markdown("### About the Chart")
        st.write("""
            - This chart shows the distribution of opportunities across different stages.
            - Use it to identify where the most opportunities are concentrated and which stages might need more attention.
            
        """)


# Ponto de entrada principal do script
if __name__ == "__main__":
    run_page(data)

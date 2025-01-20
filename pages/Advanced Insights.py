import streamlit as st
import pandas as pd
import plotly.express as px
from dataset import data  # Importa o DataFrame diretamente do módulo dataset


def main():  # Main function
    # Configuração da página
    st.set_page_config(
        layout="wide", page_title="Advanced Insights", page_icon="📊")

    # Cabeçalho com título e logo
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.title("Advanced Insights")
    with col2:
        st.image(
            "CRL.png",  # Caminho para o arquivo do logo
            width=80
        )

    # Resumo de Indicadores
    st.markdown("### Key Indicators")
    col1, col2, col3 = st.columns(3)
    with col1:
        total_opportunities = len(data)
        st.metric("Total Opportunities", total_opportunities)
    with col2:
        total_won = len(data[data['Won']])
        st.metric("Won Opportunities", total_won)
    with col3:
        conversion_rate = (total_won / total_opportunities) * 100
        st.metric("Conversion Rate", f"{conversion_rate:.2f}%")

    # Filtros na barra lateral
    st.sidebar.header("Filters")
    year_filter = st.sidebar.slider(
        "Select Year Created:",
        int(data["Year Created"].min()),
        int(data["Year Created"].max()),
        (int(data["Year Created"].min()), int(data["Year Created"].max()))
    )
    type_filter = st.sidebar.multiselect(
        "Select Opportunity Type:",
        options=data["Type"].unique(),
        default=data["Type"].unique()
    )

    # Aplicar filtros no DataFrame
    filtered_data = data[
        (data["Year Created"].between(year_filter[0], year_filter[1])) &
        (data["Type"].isin(type_filter))
    ]

    # Abas dentro da página
    tab1, tab2 = st.tabs(["Conversion Rate", "Loss Analysis"])

    # Aba 1: Taxa de Conversão
    with tab1:
        st.header("Conversion Rate by Opportunity Type")
        conversion_by_type = (
            filtered_data.groupby('Type')['Won']
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        fig = px.bar(
            conversion_by_type,
            x="Type",
            y="Won",
            text="Won",
            title="Conversion Rate by Type",
            labels={"Won": "Conversion Rate", "Type": "Opportunity Type"},
            color="Won",
        )
        fig.update_traces(texttemplate="%{text:.1%}", textposition="outside")
        st.plotly_chart(fig, use_container_width=True)

    # Aba 2: Análise de Perdas
    with tab2:
        st.header("Loss Analysis")
        lost_opportunities = filtered_data[filtered_data['Stage']
                                           == 'Closed Lost']

        # Estágios Críticos para Perdas
        st.subheader("Critical Stages for Losses")
        critical_stages = lost_opportunities['Stage'].value_counts(
        ).reset_index()
        critical_stages.columns = ["Stage", "Count"]
        fig_stages = px.bar(
            critical_stages,
            x="Stage",
            y="Count",
            text="Count",
            title="Lost Opportunities by Stage",
            labels={"Count": "Number of Lost Opportunities", "Stage": "Stage"},
            color="Count",
        )
        fig_stages.update_traces(textposition="outside")
        st.plotly_chart(fig_stages, use_container_width=True)

        # Perdas por Tipo de Oportunidade
        st.subheader("Losses by Opportunity Type")
        losses_by_type = lost_opportunities['Type'].value_counts(
        ).reset_index()
        losses_by_type.columns = ["Type", "Count"]
        fig_type = px.bar(
            losses_by_type,
            x="Type",
            y="Count",
            text="Count",
            title="Lost Opportunities by Type",
            labels={"Count": "Number of Lost Opportunities",
                    "Type": "Opportunity Type"},
            color="Count",
        )
        fig_type.update_traces(textposition="outside")
        st.plotly_chart(fig_type, use_container_width=True)


# Ponto de entrada principal do script
if __name__ == "__main__":
    main()

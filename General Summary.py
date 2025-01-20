import streamlit as st
import pandas as pd
import plotly.express as px
# Certifique-se de que o arquivo dataset.py está correto e acessível
from dataset import data


def main():  # Main function
    # Configuração da página
    st.set_page_config(
        layout="wide", page_title="Sales Insights 2023", page_icon="📊")

    # Cabeçalho com título e logo
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.title("Sales Insights 2023")  # O título principal do aplicativo
    with col2:
        st.image(
            "CRL.png",  # Caminho para o arquivo do logo
            width=80
        )

    # Barra lateral com filtros
    st.sidebar.header("Filters")

    # Filtro de estágio
    default_stages = ["Closed Won", "Close Lost", "Cancelled", "Negotiate"]
    stage_options = data["Stage"].unique()
    valid_default_stages = [
        stage for stage in default_stages if stage in stage_options]

    selected_stages = st.sidebar.multiselect(
        "Select Stage:",
        options=stage_options,
        default=valid_default_stages
    )

    # Filtro de intervalo de valores
    min_amount = int(data["Amount"].min())
    max_amount = int(data["Amount"].max())

    amounts = st.sidebar.slider(
        "Select Amount Range:",
        min_amount,
        max_amount,
        (min_amount, max_amount)
    )

    # Aplicar filtros
    filtered_data = data[
        (data["Stage"].isin(selected_stages)) &
        (data["Amount"] >= amounts[0]) &
        (data["Amount"] <= amounts[1])
    ]

    # Layout principal: dois gráficos lado a lado
    st.markdown("### Key Insights")
    col_pie, col_bar = st.columns(2)

    # Gráfico de pizza: Distribuição por estágio
    with col_pie:
        st.subheader("Opportunities by Stage")
        stage_counts = filtered_data['Stage'].value_counts().reset_index()
        stage_counts.columns = ['Stage', 'Count']
        pie_chart = px.pie(
            stage_counts,
            names='Stage',
            values='Count',
            title='Opportunities Distribution by Stage',
            color='Stage',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(pie_chart, use_container_width=True)

    # Gráfico de barras: Top 15 contas
    with col_bar:
        st.subheader("Top 15 Opportunities by Account")
        df_top15 = (
            filtered_data.groupby('Account', as_index=False)['Amount']
            .sum()
            .sort_values(by='Amount', ascending=False)
            .head(15)
        )

        bar_chart = px.bar(
            df_top15,
            x='Amount',
            y='Account',
            orientation='h',
            title='Top 15 Accounts by Total Sales Opportunity',
            labels={'Amount': 'Total Amount', 'Account': 'Account'},
            color='Amount',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(bar_chart, use_container_width=True)

    # Adicionar conclusões abaixo dos gráficos
    st.markdown("---")
    st.write("## Summary")
    st.write("""
    - This application provides a detailed visualization of Charles River Laboratories' sales opportunities for 2023.
    - You can filter opportunities by **stage** and **amount range** using the options in the sidebar.
    - The **pie chart** shows the distribution of opportunities across different sales stages in 2023, helping identify where the most progress is happening.
    - The **bar chart** highlights the **top 15 accounts** with the largest sales opportunities, showing the total value for each account.
    """)


if __name__ == "__main__":
    main()

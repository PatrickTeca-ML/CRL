import streamlit as st
import pandas as pd
import plotly.express as px
import os
import pandas as pd


def load_data():
    file_path = 'df_new_4.csv'  # Atualize o caminho do arquivo conforme necessário
    data = pd.read_csv(file_path)
    data['Created Date'] = pd.to_datetime(
        data['Created Date'], errors='coerce')
    data['Close Date'] = pd.to_datetime(data['Close Date'], errors='coerce')
    data['Sales Cycle Duration'] = (
        data['Close Date'] - data['Created Date']).dt.days
    data['Year Created'] = data['Created Date'].dt.year
    data['Year Closed'] = data['Close Date'].dt.year
    data['Won'] = data['Stage'] == 'Closed Won'
    return data


# Carregar os dados
data = load_data()

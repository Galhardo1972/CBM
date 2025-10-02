import os
import pandas as pd
import streamlit as st

# Caminho da pasta de dados
dados_path = os.path.join(os.getcwd(), "dados")

# Lista de arquivos CSV ordenados por data de modificação
arquivos_csv = sorted(
    [f for f in os.listdir(dados_path) if f.endswith(".csv")],
    key=lambda x: os.path.getmtime(os.path.join(dados_path, x)),
    reverse=True
)

# Carrega o mais recente
arquivo_mais_recente = os.path.join(dados_path, arquivos_csv[0])
df = pd.read_csv(arquivo_mais_recente)

st.title("📦 Status dos AWBs")
st.write(f"📄 Arquivo carregado: `{arquivos_csv[0]}`")
st.dataframe(df)
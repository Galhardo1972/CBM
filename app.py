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

# cruzamento com excel originado do BI
# Caminho do arquivo Excel
excel_path = r"C:\CBM\PROGRAMACAO\NA RUA\vencimento_rua.xlsx"

# Carrega o Excel
df_venc = pd.read_excel(excel_path)

# Normaliza os nomes das colunas para evitar erros
df_venc.columns = df_venc.columns.str.strip().str.lower()
df.columns = df.columns.str.strip().str.lower()

# Faz o merge com base no AWB
df_merged = pd.merge(df, df_venc[['awb', 'descrição vencimento']], on='awb', how='left')

# Atualiza o DataFrame principal
df = df_merged

# Forçar a leitura da coluna "awb"
df_venc.rename(columns=lambda x: x.strip().lower(), inplace=True)

# Mostra se a nova coluna "descriçao vencimento" esta no dataframe
st.write("🔍 Colunas disponíveis:", df.columns.tolist())

# Exibe o resultado final
st.dataframe(df)

print(df.columns)
print(df_venc.columns)
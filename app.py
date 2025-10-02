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

# cruzamento com excel originado do BI
# Caminho do arquivo Excel
excel_path = r"C:\CBM\PROGRAMACAO\NA RUA\vencimento_rua.xlsx"

# Carrega o Excel
df_venc = pd.read_excel(excel_path)

# Normaliza os nomes das colunas para evitar erros
df_venc.columns = df_venc.columns.str.strip().str.lower()
df.columns = df.columns.str.strip().str.lower()

# Força tudo para string e remove espaços
df['awb'] = df['awb'].astype(str).str.strip().str.upper()
df_venc['awb'] = df_venc['awb'].astype(str).str.strip().str.upper()

# Extrai apenas os números do AWB no CSV
df['awb'] = df['awb'].astype(str).str.extract(r'(\d+)')

# Garante que o AWB do Excel também seja texto limpo
df_venc['awb'] = df_venc['awb'].astype(str).str.strip()

# As AWBs sem vencimento apara "Sem vencimento"
df['descrição vencimento'] = df['descrição vencimento'].fillna("Sem vencimento")

# Faz o merge com base no AWB
df_merged = pd.merge(df, df_venc[['awb', 'descrição vencimento']], on='awb', how='left')

# Mostra se a nova coluna "descriçao vencimento" esta no dataframe
st.write("🔍 Colunas disponíveis:", df.columns.tolist())

# Exibe o resultado final
st.dataframe(df)

st.write("🔍 Exemplo de AWBs no CSV:", df['awb'].head())
st.write("🔍 Exemplo de AWBs no Excel:", df_venc['awb'].head())
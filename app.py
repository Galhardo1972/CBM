import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Status dos AWBs", layout="wide")

# Título do app
st.title("📦 Status dos AWBs")

# Caminho da pasta de dados
dados_path = os.path.join(os.getcwd(), "dados")

# Verifica se a pasta existe
if not os.path.exists(dados_path):
    st.error(f"❌ Pasta 'dados' não encontrada: `{dados_path}`")
    st.stop()

# Lista de arquivos CSV ordenados por data de modificação
arquivos_csv = sorted(
    [f for f in os.listdir(dados_path) if f.endswith(".csv")],
    key=lambda x: os.path.getmtime(os.path.join(dados_path, x)),
    reverse=True
)

# Verifica se há arquivos CSV
if not arquivos_csv:
    st.error("❌ Nenhum arquivo CSV encontrado na pasta 'dados'.")
    st.stop()

# Carrega o mais recente
arquivo_mais_recente = os.path.join(dados_path, arquivos_csv[0])
df = pd.read_csv(arquivo_mais_recente)

st.write(f"📄 Arquivo CSV carregado: `{arquivos_csv[0]}`")

# Upload manual do Excel
uploaded_file = st.file_uploader("📤 Envie o arquivo Excel com vencimentos", type=["xlsx"])

if uploaded_file is not None:
    df_venc = pd.read_excel(uploaded_file)
    st.success("✅ Excel carregado com sucesso.")

    # Normaliza os nomes das colunas
    df.columns = df.columns.str.strip().str.lower()
    df_venc.columns = df_venc.columns.str.strip().str.lower()

    # Padroniza AWBs
    df['awb'] = df['awb'].astype(str).str.extract(r'(\d+)')[0].fillna("").str.upper().str.strip()
    df_venc['awb'] = df_venc['awb'].astype(str).str.upper().str.strip()
   
    # Merge entre CSV e Excel
    df_merged = pd.merge(df, df_venc[['awb', 'descrição vencimento']], on='awb', how='left')

    # Exibe resultado
    st.write("🔍 Colunas disponíveis:", df_merged.columns.tolist())
    st.dataframe(df_merged)

    st.write("🔍 Exemplo de AWBs no CSV:", df['awb'].head())
    st.write("🔍 Exemplo de AWBs no Excel:", df_venc['awb'].head())

else:
    st.info("📥 Aguardando envio do arquivo Excel para cruzamento com os dados.")

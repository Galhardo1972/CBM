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
st.write(f"🔢 Linhas no CSV original: {len(df)}")

# Upload manual do Excel
uploaded_file = st.file_uploader("📤 Envie o arquivo Excel com vencimentos", type=["xlsx"])

if uploaded_file is not None:
    df_venc = pd.read_excel(uploaded_file)
    st.success("✅ Excel carregado com sucesso.")
    st.write(f"🔢 Linhas no Excel: {len(df_venc)}")

    # Normaliza os nomes das colunas
    df.columns = df.columns.str.strip().str.lower()
    df_venc.columns = df_venc.columns.str.strip().str.lower()

    # Padroniza AWBs
    df['awb'] = df['awb'].astype(str).str.extract(r'(\d+)')[0].fillna("").str.upper().str.strip()
    df_venc['awb'] = df_venc['awb'].astype(str).str.upper().str.strip()

    # Merge entre CSV e Excel
    df_merged = pd.merge(df, df_venc[['awb', 'descrição vencimento']], on='awb', how='left')
    st.write(f"🔢 Linhas após merge: {len(df_merged)}")

    # Preenche vencimentos ausentes após o merge
    df_merged['descrição vencimento'] = df_merged['descrição vencimento'].fillna("Sem vencimento")

    # Exibe resultado
    st.write("🔍 Colunas disponíveis:", df_merged.columns.tolist())
    st.dataframe(df_merged)

    st.write("🔍 Exemplo de AWBs no CSV:", df['awb'].head())
    st.write("🔍 Exemplo de AWBs no Excel:", df_venc['awb'].head())

    # Exportação opcional
    st.markdown("### 📤 Exportar dados")
    filtro = st.checkbox("Exportar apenas AWBs com vencimento")
    if filtro:
        df_export = df_merged[df_merged['descrição vencimento'] != "Sem vencimento"]
    else:
        df_export = df_merged

    st.write(f"🔢 Linhas exportadas: {len(df_export)}")

    st.download_button(
        label="📥 Baixar arquivo CSV",
        data=df_export.to_csv(index=False).encode("utf-8"),
        file_name="awb_exportado.csv",
        mime="text/csv"
    )

else:
    st.info("📥 Aguardando envio do arquivo Excel para cruzamento com os dados.")
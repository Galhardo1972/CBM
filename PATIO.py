import streamlit as st
import pandas as pd
import os
import glob

# 📍 Diretórios dos arquivos
csv_dir = r"C:\CBM\PROGRAMACAO\ATUALIZAR AWB ICS"
xlsx_path = r"C:\CBM\PROGRAMACAO\NA RUA\vencimento_rua.xlsx"  # substitua com o nome real

# 🔍 Encontrar o CSV mais recente
csv_files = glob.glob(os.path.join(csv_dir, "awbs_extraidos_*.csv"))
latest_csv = max(csv_files, key=os.path.getctime)

# 🧾 Carregar os dados
df_csv = pd.read_csv(latest_csv, sep=",", encoding="utf-8")
df_xlsx = pd.read_excel(xlsx_path)

# 🔄 Normalizar nomes de colunas: remover espaços, aspas e deixar tudo minúsculo
df_csv.columns = df_csv.columns.str.strip().str.replace('"', '').str.lower()
df_xlsx.columns = df_xlsx.columns.str.strip().str.replace('"', '').str.lower()

print("Colunas do CSV:", df_csv.columns.tolist())
print("Colunas do XLSX:", df_xlsx.columns.tolist())

# 🔗 Relacionar pelo campo AWB
df_merged = pd.merge(
    df_csv,
    df_xlsx[["awb", "descrição vencimento"]],
    how="left",
    left_on="awb",
    right_on="awb"
)

# 🌐 Interface Streamlit
st.title("📦 Relatório de AWBs Extraídos")
st.write(f"Arquivo CSV mais recente: `{os.path.basename(latest_csv)}`")

# 📊 Mostrar tabela
st.dataframe(df_merged)

# 📥 Download opcional
csv_download = df_merged.to_csv(index=False).encode("utf-8")
st.download_button("📥 Baixar tabela combinada", csv_download, "awb_combinado.csv", "text/csv")
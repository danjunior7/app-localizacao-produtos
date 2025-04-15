
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Localização de Produtos", layout="wide")

st.title("📦 Localização de Produtos nas Lojas")

# Upload da base de dados (já embarcada no repositório)
@st.cache_data
def carregar_dados():
    return pd.read_csv("produtos_por_loja.csv", sep=";", encoding="utf-8")

df = carregar_dados()

# Formulário de entrada inicial
with st.form("info_inicial"):
    col1, col2 = st.columns(2)
    nome_conferente = col1.text_input("👤 Nome do Conferente")
    loja = col2.selectbox("🏪 Loja", sorted(df["LOJA"].unique()))
    data_pesquisa = st.date_input("📅 Data da Pesquisa", value=datetime.today())
    enviar = st.form_submit_button("Iniciar")

if enviar:
    df_loja = df[df["LOJA"] == loja].reset_index(drop=True)
    st.markdown(f"### Produtos para a loja **{loja}** – conferente: **{nome_conferente}**")
    
    respostas = []
    
    for idx, row in df_loja.iterrows():
        with st.expander(f"{row['DESCRIÇÃO']} (COD: {row['COD.INT']})"):
            st.write(f"**Estoque:** {row['ESTOQUE']} unidades")
            st.write(f"**Dias sem movimentação:** {row['DIAS SEM MOVIMENTACAO']}")
            
            local = st.radio(
                "📍 Localização do Produto:",
                ["Seção", "Depósito", "Erro de Estoque"],
                key=f"local_{idx}"
            )
            validade = st.date_input("🗓️ Validade do produto (se houver)", key=f"validade_{idx}")
            
            respostas.append({
                "Conferente": nome_conferente,
                "Loja": loja,
                "Data da Pesquisa": data_pesquisa.strftime("%Y-%m-%d"),
                "COD.INT": row["COD.INT"],
                "Descrição": row["DESCRIÇÃO"],
                "Estoque": row["ESTOQUE"],
                "Dias sem movimentação": row["DIAS SEM MOVIMENTACAO"],
                "Local": local,
                "Validade": validade.strftime("%Y-%m-%d") if validade else ""
            })
    
    if st.button("✅ Finalizar e Exportar Respostas"):
        df_respostas = pd.DataFrame(respostas)
        st.success("Respostas registradas com sucesso!")
        st.download_button("📥 Baixar respostas em Excel", df_respostas.to_csv(index=False).encode("utf-8"), file_name="respostas_localizacao.csv", mime="text/csv")

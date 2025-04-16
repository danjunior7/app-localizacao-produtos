import streamlit as st
import pandas as pd

# Título principal
st.title("📦 Localização de Produtos")

# Função para carregar os dados
@st.cache_data
def carregar_dados():
    return pd.read_excel("Feedback_Localizacao.xlsx")

# Carrega o DataFrame
df = carregar_dados()

# Dropdown com os nomes dos produtos
produtos_disponiveis = df["DESCRIÇÃO"].dropna().unique()
produto_selecionado = st.selectbox("Selecione o produto:", sorted(produtos_disponiveis))

# Filtra os dados com base no produto selecionado
resultado = df[df["DESCRIÇÃO"] == produto_selecionado]

# Exibe os resultados
if not resultado.empty:
    st.subheader("Resultado da busca")
    st.dataframe(resultado, use_container_width=True)

    # Botão para download do Excel
    excel_bytes = resultado.to_excel(index=False, engine="openpyxl")
    st.download_button(
        label="⬇️ Baixar resultado em Excel (somente ADM)",
        data=excel_bytes,
        file_name=f"{produto_selecionado}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.success("Obrigado por usar o sistema! 😊")
else:
    st.warning("Produto não encontrado.")

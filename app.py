import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Pesquisa de Localização de Produtos", layout="wide")

st.title("📦 Pesquisa de Localização de Produtos")

# Carregando a planilha
@st.cache_data
def carregar_dados():
    return pd.read_excel("Feedback_Localizacao.xlsx")

df = carregar_dados()

# Inicializa a session state
if "respostas" not in st.session_state:
    st.session_state.respostas = {}

if "pagina" not in st.session_state:
    st.session_state.pagina = "pesquisa"

# Função para registrar respostas
def registrar_resposta(produto, local, validade):
    st.session_state.respostas[produto] = {
        "local": local,
        "validade": validade
    }

# Página de pesquisa
if st.session_state.pagina == "pesquisa":
    st.subheader("Preencha a localização e validade dos produtos abaixo")

    todos_preenchidos = True

    for index, row in df.iterrows():
        produto = row["Produto"]
        dias = row["Dias Sem Movimentação"]
        estoque = row["Estoque"]

        col1, col2 = st.columns([3, 2])

        with col1:
            st.markdown(f"**🔹 Produto:** {produto}<br>📆 {dias} dias sem movimentação<br>📦 Estoque: {estoque}", unsafe_allow_html=True)

        with col2:
            local = st.selectbox(f"Local - {produto}", ["", "Seção", "Depósito", "Erro de Estoque"],
                                 key=f"local_{produto}")
            validade = st.date_input(f"Validade - {produto}", value=None, key=f"validade_{produto}", format="DD/MM/YYYY")

            if local and validade:
                registrar_resposta(produto, local, validade)
            else:
                todos_preenchidos = False

    if todos_preenchidos:
        if st.button("✅ Finalizar Pesquisa"):
            st.session_state.pagina = "finalizado"
    else:
        st.warning("⚠️ Preencha todos os campos obrigatórios para finalizar.")

# Página de finalização
if st.session_state.pagina == "finalizado":
    st.success("🎉 Obrigado pela pesquisa! Suas respostas foram registradas com sucesso.")
    st.balloons()

    st.subheader("Resumo das Respostas (visível apenas para debug ou admin)")
    resposta_df = pd.DataFrame.from_dict(st.session_state.respostas, orient='index')
    st.dataframe(resposta_df.reset_index().rename(columns={"index": "Produto"}))

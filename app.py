import streamlit as st
import pandas as pd

# Função para carregar os dados da planilha
@st.cache_data
def carregar_dados():
    return pd.read_excel("Feedback_Localizacao.xlsx")

# Carregar os dados
df = carregar_dados()

# Lista de locais (você pode editar conforme necessário)
locais = ["Gôndola 1", "Gôndola 2", "Ponta de Gôndola", "Ilha", "Check-out", "Depósito", "Outro"]

# Inicializar a lista de respostas
respostas = []

# Título da página
st.title("Pesquisa de Localização de Produtos")

# Instrução inicial
st.info("Por favor, selecione o local onde cada produto está localizado na loja.")

# Loop pelos produtos e exibição dos campos de seleção
for index, row in df.iterrows():
    produto = row["DESCRIÇÃO"]  # Usando o nome correto da coluna
    st.markdown(f"### Produto: **{produto}**")
    local = st.selectbox(f"Selecione o local do produto '{produto}'", locais, key=index)
    respostas.append({"Produto": produto, "Local": local})

# Botão de finalizar
if st.button("Finalizar Pesquisa"):
    df_respostas = pd.DataFrame(respostas)
    df_respostas.to_excel("respostas_localizacao.xlsx", index=False)
    st.success("Obrigado! Sua resposta foi registrada com sucesso.")

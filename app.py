import streamlit as st
import pandas as pd

# Função para carregar o arquivo Excel
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_excel("Feedback_Localizacao.xlsx")
        return df
    except FileNotFoundError:
        st.error("Arquivo 'Feedback_Localizacao.xlsx' não encontrado.")
        st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        st.stop()

# Carrega os dados
df = carregar_dados()

# Mostra as colunas disponíveis (ajuda no debug)
st.write("Colunas disponíveis:", df.columns.tolist())

# Tenta identificar automaticamente a coluna de descrição do produto
coluna_produto = None
for col in df.columns:
    if "descr" in col.lower():
        coluna_produto = col
        break

# Se não encontrar, mostra erro
if not coluna_produto:
    st.error("Nenhuma coluna com 'descr' no nome foi encontrada. Verifique o nome da coluna no Excel.")
    st.stop()

# Título do app
st.title("Localização de Produtos")

# Caixa de seleção com os nomes dos produtos
produtos_unicos = df[coluna_produto].dropna().unique()
produto_selecionado = st.selectbox("Selecione o produto:", sorted(produtos_unicos))

# Filtra os dados com base no produto selecionado
resultado = df[df[coluna_produto] == produto_selecionado]

# Mostra os resultados
st.subheader("Resultado da busca")
st.write(resultado)

# Botão para download (opcional para o ADM)
@st.cache_data
def gerar_excel(arquivo):
    return arquivo.to_excel(index=False)

if st.button("🔽 Baixar resultado em Excel (somente ADM)"):
    st.download_button(
        label="Clique para baixar",
        data=resultado.to_csv(index=False).encode('utf-8'),
        file_name="resultado_localizacao.csv",
        mime="text/csv"
    )

# Mensagem final
st.success("Obrigado por usar o sistema! 😊")

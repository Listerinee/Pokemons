import pandas as pd
import streamlit as st
from pokemon_api import salvar_pokemon_csv

st.set_page_config(page_title="PokeAPI com Imagens", page_icon="⭐", layout="wide")

st.title("⭐ Pokédex Interativa com Imagens")
st.write(
    "Escolha a quantidade, clique em buscar e veja a mágica acontecer com as artes oficiais!"
)

st.divider()

# Layout com duas colunas para os inputs de configuração
col_limite, col_nome = st.columns(2)
with col_limite:
    limite = st.number_input(
        "Quantidade de Pokémon:", min_value=1, max_value=151, value=12, step=1
    )
with col_nome:
    nome_arquivo = st.text_input("Nome do arquivo CSV:", value="pokemons_imagens.csv")

if st.button("Buscar Pokémon e Imagens", type="primary"):
    with st.spinner("Buscando dados e imagens (isso pode demorar um pouquinho)..."):
        salvar_pokemon_csv(nome_arquivo_csv=nome_arquivo, limite=limite)

    try:
        df = pd.read_csv(nome_arquivo)
        st.success(f"{len(df)} Pokémon carregados com sucesso!")

        st.subheader("🖼️ Galeria de Pokémon")

        # Criar uma grade de colunas (4 Pokémon por linha)
        colunas_por_linha = 4
        for i in range(0, len(df), colunas_por_linha):
            # Cria um bloco de até 4 colunas
            cols = st.columns(colunas_por_linha)
            for j in range(colunas_por_linha):
                index = i + j
                if index < len(df):
                    pokemon = df.iloc[index]
                    with cols[j]:
                        # Card do Pokémon
                        st.markdown(f"### **{pokemon['nome']}**")
                        # Verifica se existe o link da imagem e exibe
                        if pd.notna(pokemon["url_imagem"]):
                            st.image(pokemon["url_imagem"], use_container_width=True)
                        else:
                            st.warning("Sem imagem disponível")
                        st.caption(f"[Ver dados da API]({pokemon['url_api']})")

        st.divider()

        # Botão de download do CSV gerado
        with open(nome_arquivo, "rb") as file:
            st.download_button(
                label="📥 Baixar CSV com Links das Imagens",
                data=file,
                file_name=nome_arquivo,
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Erro ao processar exibição: {e}")
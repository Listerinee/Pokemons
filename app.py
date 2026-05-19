import pandas as pd
import streamlit as st
from pokemon_api import salvar_pokemon_csv

st.set_page_config(page_title="Pokédex Avançada", page_icon="🧬", layout="wide")

st.title("🧬 Pokédex Analítica Completa")
st.write("Gere seu CSV e veja os detalhes físicos, tipos e gerações de cada Pokémon.")

st.divider()

col_limite, col_nome = st.columns(2)
with col_limite:
    # Aumentei o limite máximo para aceitar mais Pokémon se você quiser testar as outras gerações!
    limite = st.number_input(
        "Quantidade de Pokémon:", min_value=1, max_value=1025, value=12, step=1
    )
with col_nome:
    nome_arquivo = st.text_input("Nome do arquivo CSV:", value="pokemons_completos.csv")

if st.button("Buscar Dados Completos", type="primary"):
    with st.spinner("Buscando dados detalhados na PokeAPI... Aguarde..."):
        salvar_pokemon_csv(nome_arquivo_csv=nome_arquivo, limite=limite)

    try:
        df = pd.read_csv(nome_arquivo)
        st.success(f"{len(df)} Pokémon carregados com sucesso!")

        st.subheader("📊 Cards dos Pokémon")

        colunas_por_linha = 4
        for i in range(0, len(df), colunas_por_linha):
            cols = st.columns(colunas_por_linha)
            for j in range(colunas_por_linha):
                index = i + j
                if index < len(df):
                    pokemon = df.iloc[index]
                    with cols[j]:
                        # Criando uma caixinha/container visual para cada Pokémon
                        with st.container(border=True):
                            # Título com o ID e Nome
                            st.markdown(f"### N° {pokemon['id']} - {pokemon['nome']}")

                            # Exibe a Imagem
                            if pd.notna(pokemon["url_imagem"]):
                                st.image(pokemon["url_imagem"], use_container_width=True)
                            else:
                                st.warning("Sem imagem")

                            # --- NOVAS INFORMAÇÕES ABAIXO DA IMAGEM ---
                            st.markdown(f"**🔹 Tipo:** `{pokemon['tipo']}`")
                            st.markdown(f"**⚖️ Peso:** {pokemon['peso_kg']} kg")
                            st.markdown(f"**📏 Altura:** {pokemon['altura_m']} m")
                            st.caption(f"📍 {pokemon['geracao']}")

        st.divider()

        with open(nome_arquivo, "rb") as file:
            st.download_button(
                label="📥 Baixar CSV Detalhado",
                data=file,
                file_name=nome_arquivo,
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Erro ao processar exibição: {e}")

import pandas as pd
import streamlit as st
from pokemon_api import salvar_pokemon_por_geracao

st.set_page_config(page_title="Pokédex por Geração", page_icon="🌐", layout="wide")

st.title("🌐 Pokédex Organizada por Gerações")
st.write(
    "Selecione uma região/geração específica para listar os Pokémon e gerar o seu relatório em CSV."
)

st.divider()

# Mapeamento do texto do menu para o número da geração correspondente
opcoes_geracao = {
    "1ª Geração - Kanto (151 Pokémon)": 1,
    "2ª Geração - Johto (100 Pokémon)": 2,
    "3ª Geração - Hoenn (135 Pokémon)": 3,
    "4ª Geração - Sinnoh (107 Pokémon)": 4,
    "5ª Geração - Unova (156 Pokémon)": 5,
    "6ª Geração - Kalos (72 Pokémon)": 6,
    "7ª Geração - Alola (88 Pokémon)": 7,
    "8ª Geração - Galar (89 Pokémon)": 8,
    "9ª Geração - Paldea (127 Pokémon)": 9,
}

col_combo, col_nome = st.columns(2)

with col_combo:
    # Cria a caixa de seleção na tela
    selecao = st.selectbox("Escolha a Geração desejada:", list(opcoes_geracao.keys()))
    # Pega o número correspondente (1, 2, 3...) da opção selecionada
    geracao_escolhida = opcoes_geracao[selecao]

with col_nome:
    nome_arquivo = st.text_input(
        "Nome do arquivo CSV:", value=f"pokemon_gen_{geracao_escolhida}.csv"
    )

if st.button("Buscar Geração Completa", type="primary"):
    # Como carregar gerações inteiras pode demorar um pouco (ex: 151 requisições),
    # deixamos um aviso bem claro na tela para o usuário.
    with st.spinner(
        f"Extraindo todos os dados da geração selecionada diretamente da PokeAPI... Aguarde..."
    ):
        salvar_pokemon_por_geracao(
            geracao_num=geracao_escolhida, nome_arquivo_csv=nome_arquivo
        )

    try:
        df = pd.read_csv(nome_arquivo)
        st.success(
            f"Excelente! Todos os {len(df)} Pokémon da geração foram carregados com sucesso."
        )

        st.subheader(f"🖼️ Galeria: {selecao}")

        colunas_por_linha = 4
        for i in range(0, len(df), colunas_por_linha):
            cols = st.columns(colunas_por_linha)
            for j in range(colunas_por_linha):
                index = i + j
                if index < len(df):
                    pokemon = df.iloc[index]
                    with cols[j]:
                        with st.container(border=True):
                            st.markdown(f"### N° {pokemon['id']} - {pokemon['nome']}")

                            if pd.notna(pokemon["url_imagem"]):
                                st.image(pokemon["url_imagem"], use_container_width=True)
                            else:
                                st.warning("Sem imagem")

                            st.markdown(f"**🔹 Tipo:** `{pokemon['tipo']}`")
                            st.markdown(f"**⚖️ Peso:** {pokemon['peso_kg']} kg")
                            st.markdown(f"**📏 Altura:** {pokemon['altura_m']} m")
                            st.caption(f"📍 {pokemon['geracao']}")

        st.divider()

        with open(nome_arquivo, "rb") as file:
            st.download_button(
                label="📥 Baixar CSV da Geração",
                data=file,
                file_name=nome_arquivo,
                mime="text/csv",
            )

    except Exception as e:
        st.error(f"Erro ao processar exibição: {e}")
    except Exception as e:
        st.error(f"Erro ao processar exibição: {e}")

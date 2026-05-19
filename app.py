import pandas as pd
import streamlit as st
from pokemon_api import salvar_pokemon_por_geracao

st.set_page_config(page_title="Pokédex com Gráficos", page_icon="📊", layout="wide")

st.title("📊 Pokédex Estatística com Gráficos")
st.write(
    "Selecione uma região/geração para visualizar a distribuição de tipos e listar os Pokémon."
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
    selecao = st.selectbox("Escolha a Geração desejada:", list(opcoes_geracao.keys()))
    geracao_escolhida = opcoes_geracao[selecao]

with col_nome:
    nome_arquivo = st.text_input(
        "Nome do arquivo CSV:", value=f"pokemon_gen_{geracao_escolhida}.csv"
    )

if st.button("Buscar e Analisar Geração", type="primary"):
    with st.spinner("Buscando dados e gerando análises... Aguarde..."):
        salvar_pokemon_por_geracao(
            geracao_num=geracao_escolhida, nome_arquivo_csv=nome_arquivo
        )

    try:
        df = pd.read_csv(nome_arquivo)
        st.success(f"Dados da geração carregados com sucesso!")

        # ==========================================
        # 📊 NOVA SEÇÃO: GRÁFICO DE BARRAS POR TIPO
        # ==========================================
        st.subheader("📈 Quantidade de Pokémon por Tipo")

        # 1. Separar os tipos combinados (ex: "Grass / Poison" vira ["Grass", "Poison"])
        lista_todos_tipos = []
        for tipos_pokemon in df["tipo"].dropna():
            # Divide os tipos onde houver a barra " / " e limpa espaços extras
            partes = [t.strip() for t in tipos_pokemon.split("/")]
            lista_todos_tipos.extend(partes)

        # 2. Criar um novo DataFrame contando a frequência de cada tipo
        df_contagem_tipos = pd.Series(lista_todos_tipos).value_counts().reset_index()
        df_contagem_tipos.columns = ["Tipo", "Quantidade"]

        # 3. Definir o "Tipo" como índice para o Streamlit entender o eixo X do gráfico
        df_contagem_tipos = df_contagem_tipos.set_index("Tipo")

        # 4. Renderizar o gráfico de barras na tela
        st.bar_chart(df_contagem_tipos, y="Quantidade", color="#ff4b4b")

        st.divider()

        # ==========================================
        # 🖼️ EXIBIÇÃO DOS CARDS
        # ==========================================
        st.subheader(f"🖼️ Galeria de Pokémon: {selecao}")

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
        st.error(f"Erro ao processar exibição ou gráfico: {e}")
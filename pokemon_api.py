import csv
import requests


def salvar_pokemon_csv(nome_arquivo_csv="pokemons.csv", limite=20):
    url_api = f"https://pokeapi.co/api/v2/pokemon/?limit={limite}"

    try:
        print(f"Biblioteca: Buscando {limite} Pokémon...")
        resposta = requests.get(url_api)
        resposta.raise_for_status()

        dados_completos = respose_json = resposta.json()
        lista_basica = dados_completos.get("results", [])

        lista_com_imagens = []

        # Para cada Pokémon, vamos entrar na URL dele para buscar a imagem
        for poke in lista_basica:
            print(f"Buscando detalhes de: {poke['name']}")
            res_detalhes = requests.get(poke["url"])

            if res_detalhes.status_code == 200:
                dados_detalhes = res_detalhes.json()
                # Caminho dentro do JSON para a arte oficial em alta definição
                sprites = dados_detalhes.get("sprites", {})
                other = sprites.get("other", {})
                artwork = other.get("official-artwork", {})
                url_imagem = artwork.get("front_default")

                # Se não achar a oficial, tenta a imagem padrão menor
                if not url_imagem:
                    url_imagem = sprites.get("front_default")
            else:
                url_imagem = ""

            # Criamos um novo dicionário com o Nome, URL e a Imagem
            lista_com_imagens.append(
                {
                    "nome": poke["name"].capitalize(),
                    "url_api": poke["url"],
                    "url_imagem": url_imagem,
                }
            )

        if not lista_com_imagens:
            print("Biblioteca: Nenhum Pokémon encontrado.")
            return

        cabecalhos = lista_com_imagens[0].keys()

        with open(nome_arquivo_csv, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=cabecalhos)
            escritor.writeheader()
            escritor.writerows(lista_com_imagens)

        print(f"Biblioteca: Arquivo '{nome_arquivo_csv}' gerado com sucesso!")

    except Exception as e:
        print(f"Biblioteca: Ocorreu um erro: {e}")
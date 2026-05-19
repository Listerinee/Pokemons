import csv
import requests

# 1. URL da PokeAPI
API_URL = "https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0"


def pokeapi_para_csv(url_api, nome_arquivo_csv):
    try:
        print(f"Acessando a PokeAPI: {url_api}...")
        resposta = requests.get(url_api)
        resposta.raise_for_status()

        # Converte o retorno para dicionário
        dados_completos = resposta.json()

        # Isola a lista de pokémons que vem dentro da chave 'results'
        lista_pokemon = dados_completos.get("results", [])

        if not lista_pokemon:
            print("Nenhum Pokémon encontrado.")
            return

        # Define as colunas do CSV ('name' e 'url')
        cabecalhos = lista_pokemon[0].keys()

        # Grava os dados no arquivo CSV
        with open(nome_arquivo_csv, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=cabecalhos)

            escritor.writeheader()  # Escreve o cabeçalho
            escritor.writerows(lista_pokemon)  # Grava as linhas

        print(
            f"Tudo pronto! Arquivo '{nome_arquivo_csv}' gerado com {len(lista_pokemon)} Pokémon."
        )

    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar na PokeAPI: {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")


# Executar o script
pokeapi_para_csv(API_URL, "pokemons.csv")
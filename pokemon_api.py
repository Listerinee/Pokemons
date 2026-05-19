import csv
import requests


def obter_geracao(pokemon_id):
    """Retorna a geração do Pokémon com base no seu ID."""
    if 1 <= pokemon_id <= 151:
        return "1ª Geração (Kanto)"
    elif 152 <= pokemon_id <= 251:
        return "2ª Geração (Johto)"
    elif 252 <= pokemon_id <= 386:
        return "3ª Geração (Hoenn)"
    elif 387 <= pokemon_id <= 493:
        return "4ª Geração (Sinnoh)"
    elif 494 <= pokemon_id <= 649:
        return "5ª Geração (Unova)"
    elif 650 <= pokemon_id <= 721:
        return "6ª Geração (Kalos)"
    elif 722 <= pokemon_id <= 809:
        return "7ª Geração (Alola)"
    elif 810 <= pokemon_id <= 898:
        return "8ª Geração (Galar)"
    elif 899 <= pokemon_id <= 1025:
        return "9ª Geração (Paldea)"
    return "Outra/Especial"


def salvar_pokemon_csv(nome_arquivo_csv="pokemons_detalhados.csv", limite=20):
    url_api = f"https://pokeapi.co/api/v2/pokemon/?limit={limite}"

    try:
        print(f"Biblioteca: Buscando {limite} Pokémon com detalhes...")
        resposta = requests.get(url_api)
        resposta.raise_for_status()

        dados_completos = resposta.json()
        lista_basica = dados_completos.get("results", [])

        lista_detalhada = []

        for poke in lista_basica:
            print(f"Buscando detalhes extras de: {poke['name']}")
            res_detalhes = requests.get(poke["url"])

            if res_detalhes.status_code == 200:
                detalhes = res_detalhes.json()

                # 1. Capturar ID, Peso e Altura (a API traz em decímetros e hectogramas, convertemos para metros e kg)
                poke_id = detalhes.get("id")
                altura = detalhes.get("height", 0) / 10  # converte para metros
                peso = detalhes.get("weight", 0) / 10  # converte para quilos

                # 2. Capturar os Tipos (pode ser um ou mais, juntamos com uma barra "/")
                tipos_lista = [t["type"]["name"].capitalize() for t in detalhes.get("types", [])]
                tipos_formatados = " / ".join(tipos_lista)

                # 3. Descobrir a Geração baseada no ID
                geracao = obter_geracao(poke_id)

                # 4. Capturar a Imagem Oficial
                sprites = detalhes.get("sprites", {})
                artwork = sprites.get("other", {}).get("official-artwork", {})
                url_imagem = artwork.get("front_default") or sprites.get("front_default")

            else:
                altura, peso, tipos_formatados, geracao, url_imagem = 0, 0, "Desconhecido", "Desconhecida", ""

            # Adiciona o dicionário completo com as novas colunas
            lista_detalhada.append(
                {
                    "id": poke_id,
                    "nome": poke["name"].capitalize(),
                    "tipo": tipos_formatados,
                    "altura_m": altura,
                    "peso_kg": peso,
                    "geracao": geracao,
                    "url_imagem": url_imagem,
                }
            )

        if not lista_detalhada:
            print("Biblioteca: Nenhum Pokémon encontrado.")
            return

        cabecalhos = lista_detalhada[0].keys()

        with open(nome_arquivo_csv, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=cabecalhos)
            escritor.writeheader()
            escritor.writerows(lista_detalhada)

        print(f"Biblioteca: Arquivo '{nome_arquivo_csv}' gerado com sucesso!")

    except Exception as e:
        print(f"Biblioteca: Ocorreu um erro: {e}")

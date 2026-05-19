import csv
import requests


def obter_intervalo_geracao(geracao_num):
    """Retorna o dicionário de mapeamento das gerações com seus respectivos:

    - Nome amigável
    - ID Inicial (offset)
    - Quantidade de Pokémon naquela geração (limit)
    """
    geracoes = {
        1: {"nome": "1ª Geração (Kanto)", "offset": 0, "limit": 151},
        2: {"nome": "2ª Geração (Johto)", "offset": 151, "limit": 100},
        3: {"nome": "3ª Geração (Hoenn)", "offset": 251, "limit": 135},
        4: {"nome": "4ª Geração (Sinnoh)", "offset": 386, "limit": 107},
        5: {"nome": "5ª Geração (Unova)", "offset": 493, "limit": 156},
        6: {"nome": "6ª Geração (Kalos)", "offset": 649, "limit": 72},
        7: {"nome": "7ª Geração (Alola)", "offset": 721, "limit": 88},
        8: {"nome": "8ª Geração (Galar)", "offset": 809, "limit": 89},
        9: {"nome": "9ª Geração (Paldea)", "offset": 898, "limit": 127},
    }
    return geracoes.get(geracao_num)


def salvar_pokemon_por_geracao(geracao_num, nome_arquivo_csv="pokemons_geracao.csv"):
    info_gen = obter_intervalo_geracao(geracao_num)

    if not info_gen:
        print("Biblioteca: Geração inválida.")
        return

    # Construímos a URL usando offset e limit para capturar a geração correta de uma vez só
    url_api = f"https://pokeapi.co/api/v2/pokemon/?offset={info_gen['offset']}&limit={info_gen['limit']}"

    try:
        print(f"Biblioteca: Buscando {info_gen['nome']}...")
        resposta = requests.get(url_api)
        resposta.raise_for_status()

        dados_completos = resposta.json()
        lista_basica = dados_completos.get("results", [])

        lista_detalhada = []

        for poke in lista_basica:
            print(f"Buscando: {poke['name']}")
            res_detalhes = requests.get(poke["url"])

            if res_detalhes.status_code == 200:
                detalhes = res_detalhes.json()

                poke_id = detalhes.get("id")
                altura = detalhes.get("height", 0) / 10
                peso = detalhes.get("weight", 0) / 10

                tipos_lista = [
                    t["type"]["name"].capitalize() for t in detalhes.get("types", [])
                ]
                tipos_formatados = " / ".join(tipos_lista)

                sprites = detalhes.get("sprites", {})
                artwork = sprites.get("other", {}).get("official-artwork", {})
                url_imagem = artwork.get("front_default") or sprites.get("front_default")

                lista_detalhada.append(
                    {
                        "id": poke_id,
                        "nome": poke["name"].capitalize(),
                        "tipo": tipos_formatados,
                        "altura_m": altura,
                        "peso_kg": peso,
                        "geracao": info_gen["nome"],
                        "url_imagem": url_imagem,
                    }
                )

        if not lista_detalhada:
            return

        cabecalhos = lista_detalhada[0].keys()

        with open(nome_arquivo_csv, mode="w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=cabecalhos)
            escritor.writeheader()
            escritor.writerows(lista_detalhada)

        print(f"Biblioteca: Arquivo da {info_gen['nome']} gerado com sucesso!")

    except Exception as e:
        print(f"Biblioteca: Ocorreu um erro: {e}")

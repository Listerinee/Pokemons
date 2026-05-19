# Importa a função específica da sua própria biblioteca (do arquivo pokemon_api.py)
from pokemon_api import salvar_pokemon_csv

# Exemplo 1: Usando os valores padrão (Gera 'pokemons.csv' com 20 Pokémons)
salvar_pokemon_csv()

print("-" * 30)

# Exemplo 2: Personalizando o nome do arquivo e buscando os 151 Pokémons originais!
salvar_pokemon_csv(nome_arquivo_csv="primeira_geracao.csv", limite=151)
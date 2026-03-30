import os
import json

def load_quran(file) -> dict:
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file}' não foi encontrado.")
        return {}
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{file}' existe, mas não é um JSON válido.")
        return {}
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return {}

def extract_ayats(quran):
    all_ayats = []
    for sura in quran:
        for ayat in sura["verses"]:
            # Usando .get() para evitar erro caso a chave não exista
            content = ayat.get("translation_pt", "")
            all_ayats.append(content)
    return all_ayats

# Carregamento dos dados
quran_pt_br_ntlh = load_quran("./quran_pt_br_ntlh.json")
ayats = extract_ayats(quran_pt_br_ntlh)
ayats_text = " ".join(ayats).lower() # Já converte tudo para minúsculo uma vez só

# --- Novas Funcionalidades de Busca ---

# 1. Lista de palavras-chave para pesquisar
palavras_para_buscar = [
    "salvação", 
    "misericórdia", 
    "paraíso", 
    "inferno", 
    "profeta", 
    "oração", 
    "caridade",
    "demônio"
]

print("Contagem de termos no Alcorão:")
print("-" * 30)

for palavra in palavras_para_buscar:
    contagem = ayats_text.count(palavra.lower())
    print(f"{palavra.capitalize()}: {contagem}")
import requests
import json

# URL do arquivo JSON online
url = "https://cdn.jsdelivr.net/npm/quran-json@3.1.2/dist/quran_en.json"

try:
    # 1. Fazendo a requisição GET para a URL
    response = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida (Status Code 200)
    response.raise_for_status()
    
    # 2. Convertendo o conteúdo recebido em um objeto Python (dicionário/lista)
    data = response.json()
    
    # 3. Salvando o conteúdo em um arquivo local
    with open("quran_en.json", "w", encoding="utf-8") as f:
        # indent=4 deixa o arquivo legível para humanos
        # ensure_ascii=False garante que caracteres especiais sejam salvos corretamente
        json.dump(data, f, ensure_ascii=False, indent=4)
        
    print("Arquivo salvo com sucesso como 'quran_en.json'!")

except requests.exceptions.RequestException as e:
    print(f"Erro ao baixar o arquivo: {e}")
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}")

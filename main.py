import os
import json
from ollama import chat
from concurrent.futures import ProcessPoolExecutor

cpu_cores = int(os.cpu_count())

def load_quran(file) -> dict:
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: O arquivo '{file}' não foi encontrado.")
        return {} # Retorna um dicionário vazio para não quebrar o loop posterior
    except json.JSONDecodeError:
        print(f"Erro: O arquivo '{file}' existe, mas não é um JSON válido.")
        return {}
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return {}


def calculate_max_portuguese_chars(arabic_text: str, english_text: str) -> int:
    """
    Calcula o tamanho máximo recomendado (em caracteres) para a tradução em português NTLH,
    baseado no comprimento médio do árabe + inglês.
    
    Retorna um valor reduzido, mas inteligente (mantendo boa legibilidade).
    """
    # Calcula o tamanho em caracteres
    len_arabic = len(arabic_text.strip())
    len_english = len(english_text.strip())
    
    # Média aritmética simples
    avg_input = (len_arabic + len_english) / 2
    
    # Regra prática baseada em estatísticas do Alcorão + estilo NTLH:
    # - O português NTLH costuma ser mais curto que o inglês, mas mais longo que o árabe.
    # - Aplicamos uma redução inteligente (aprox. 65-75% da média de entrada)
    max_chars = int(avg_input * 0.7)
    
    # Limites mínimos e máximos sensatos para NTLH
    max_chars = max(60, max_chars)      # mínimo razoável (evita traduções curtas demais)
    max_chars = min(280, max_chars)     # máximo confortável (evita textos muito longos)
    
    # Ajuste fino para ayats muito curtos ou muito longos
    if avg_input < 80:
        max_chars = min(max_chars, 140)   # ayats curtos ficam ainda mais resumidos
    elif avg_input > 400:
        max_chars = min(max_chars, 250)   # ayats longos têm limite mais apertado
    
    return max_chars


def translate_ayat(arabic_text: str, english_text: str, model: str = "gemma3n:e4b") -> str:
    max_chars = calculate_max_portuguese_chars(arabic_text, english_text)
    
    user_prompt = f"""
        Você é um tradutor profissional e respeitoso, especialista em traduzir o Alcorão para o português brasileiro **exatamente** no estilo da NTLH (Nova Tradução na Linguagem de Hoje).

        A NTLH usa linguagem simples, clara, natural e cotidiana — como uma conversa amigável e acessível. As frases são curtas, diretas e objetivas, priorizando o sentido natural do texto original (equivalência dinâmica) em vez de tradução literal.

        Regras obrigatórias que você deve seguir rigorosamente:
        - Sempre use "Deus" (nunca "Allah")
        - Sempre use "Maomé" (nunca "Muhammad")
        - Frases curtas, diretas e fáceis de ler
        - Linguagem resumida e natural do português brasileiro atual
        - Evite repetições, palavras formais, elevadas ou arcaicas
        - Mantenha um tom calmo, respeitoso, pacífico e acolhedor
        - A tradução deve ter no máximo {max_chars} caracteres (incluindo espaços)
        - **Retorne SOMENTE a tradução em português. Nada mais.** Sem introdução, explicação, aspas, numeração ou qualquer comentário adicional.

        Exemplos de tradução correta no estilo NTLH:

        Exemplo 1:
        Árabe: يَـٰٓأَيُّهَا ٱلَّذِينَ ءَامَنُوا۟ ٱتَّقُوا۟ ٱللَّهَ وَكُونُوا۟ مَعَ ٱلصَّـٰدِقِينَ
        Inglês: O you who have believed, fear Allah and be with the truthful.
        Tradução: Ó fiéis, temam a Deus e fiquem com as pessoas honestas.

        Exemplo 2:
        Árabe: بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ
        Inglês: In the name of Allah, the Most Gracious, the Most Merciful.
        Tradução: Em nome de Deus, o Clemente, o Misericordioso.

        Exemplo 3:
        Árabe: الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ
        Inglês: Praise be to Allah, Lord of the worlds.
        Tradução: Louvado seja Deus, Senhor do universo.

        Exemplo 4:
        Árabe: إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ
        Inglês: You alone we worship, and You alone we ask for help.
        Tradução: Só a ti nós adoramos e só de ti pedimos ajuda.

        Agora traduza o seguinte versículo seguindo todas as regras acima:

        Árabe (fonte principal):
        {arabic_text}

        Inglês (referência auxiliar):
        {english_text}

        Traduza agora:
    """.strip()

    response = chat(
        model=model,
        messages=[{'role': 'user', 'content': user_prompt}],
        options={
            "temperature": 0.3,
            # "top_p": 0.92,
            # "top_k": 50,
            # "repeat_penalty": 1.12,
            "num_predict": 350,
            "seed": 42
        }
    )
    
    return response.message.content.strip()


def iterate_quran(input_file="./quran_en.json", output_file="./quran_pt_br_ntlh.json"):
    # 1. Tenta carregar o progresso já feito. Se não existir, carrega o original.
    if os.path.exists(output_file):
        print("Retomando progresso do arquivo existente...")
        quran_data = load_quran(output_file)
    else:
        print("Iniciando nova tradução do zero...")
        quran_data = load_quran(input_file)

    for sura in quran_data:
        sura_id = sura.get('id')
        print(f"Verificando Sura {sura_id}...")

        for ayat in sura["verses"]:
            # PULA se já tiver a marcação de concluído
            if ayat.get("ntlh") == True:
                continue

            try:
                # Tradução via Ollama
                portuguese_text = translate_ayat(ayat["text"], ayat["translation"])
                
                # Atualiza os campos no objeto que está na memória
                ayat["translation_pt"] = portuguese_text
                ayat["ntlh"] = True

                # SALVA IMEDIATAMENTE (Checkpoint)
                # Salvamos o quran_data inteiro para manter a estrutura de 114 suras
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(quran_data, f, ensure_ascii=False, indent=4)

                print(f" [OK] Sura {sura_id} | Ayat {ayat['id']} traduzido.")

            except Exception as e:
                print(f" [ERRO] Sura {sura_id} | Ayat {ayat['id']}: {e}")
                # Opcional: break ou return para você verificar o que houve


quran = load_quran("./quran_en.json")
quran_pt_br_ntlh = load_quran("./quran_pt_br_ntlh.json")

iterate_quran(quran)

print(quran_pt_br_ntlh)
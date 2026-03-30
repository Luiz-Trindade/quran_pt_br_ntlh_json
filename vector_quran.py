import json
import ollama
import chromadb

# --- Configurações ---
MODEL_EMBEDDING = 'bge-m3'
MODEL_LLM = 'gemma3:27b-cloud'

def load_quran(file) -> list:
    try:
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar: {e}")
        return []

def setup_chroma():
    client = chromadb.PersistentClient(path="./quran_bge_m3_db")
    collection = client.get_or_create_collection(
        name="quran_pt_br", 
        metadata={"hnsw:space": "cosine"}
    )
    return collection

def index_quran(collection, quran):
    if collection.count() > 0:
        print(f"Banco já contém {collection.count()} versículos.")
        return

    print("Indexando versículos com bge-m3...")
    for sura in quran:
        s_id = sura.get("id", "?")
        s_nome = sura.get("name", "Desconhecida")
        for ayat in sura["verses"]:
            texto_full = ayat.get("translation_pt", "").strip()
            if not texto_full: continue
            try:
                res = ollama.embed(model=MODEL_EMBEDDING, input=texto_full)
                collection.add(
                    ids=[f"S{s_id}V{ayat['id']}"],
                    embeddings=[res['embeddings'][0]],
                    documents=[texto_full],
                    metadatas=[{"surata": s_nome, "numero_sura": s_id, "versiculo": ayat['id']}]
                )
            except Exception as e:
                print(f"Erro no versículo {s_id}:{ayat['id']}: {e}")
    print("Indexação concluída!")

# --- NOVAS FUNÇÕES DE IA ---

def expandir_pergunta(pergunta):
    """IA 1: Transforma a pergunta em termos que facilitam a busca vetorial"""
    print(f"\n[IA] Otimizando busca para: '{pergunta}'")
    prompt = f"Transforme esta pergunta em palavras-chave e conceitos do Alcorão para busca semântica: {pergunta}. Responda apenas os termos."
    response = ollama.generate(model=MODEL_LLM, prompt=prompt)
    return response['response']

def gerar_resposta_final(pergunta, contextos):
    """IA 2: Condensa os ayats encontrados em uma resposta única"""
    print("[IA] Sintetizando resposta final...")
    contexto_str = "\n".join([f"- {c}" for c in contextos])
    prompt = f"""
    Baseado nestes versículos do Alcorão:
    {contexto_str}
    
    Responda de forma objetiva e respeitosa: {pergunta}
    Indique as Suratas mencionadas.
    """
    response = ollama.generate(model=MODEL_LLM, prompt=prompt)
    return response['response']

# --- EXECUÇÃO ---

quran_data = load_quran("./quran_pt_br_ntlh.json")
collection = setup_chroma()
index_quran(collection, quran_data)

try:
    while True:
        # Fluxo de Pergunta
        pergunta_usuario = input("\nPergunta (ou 'sair'): ")
        if pergunta_usuario.lower() in ['sair', 'exit', 'quit']:
            break

        # 1. Expandir pergunta com IA
        busca_otimizada = expandir_pergunta(pergunta_usuario)

        # 2. Gerar Embedding da busca expandida
        res_query = ollama.embed(model=MODEL_EMBEDDING, input=busca_otimizada)

        # 3. Buscar no ChromaDB
        results = collection.query(query_embeddings=[res_query['embeddings'][0]], n_results=5)
        # print("="*30)
        # for r in results:
        #     print(f"Textos Similares: {r[2]}")
        # print("="*30)

        # 4. Condensar com IA
        textos_encontrados = results['documents'][0]
        resposta_final = gerar_resposta_final(pergunta_usuario, textos_encontrados)
        resposta_final = resposta_final.replace("*", "")
        resposta_final = resposta_final.replace("#", "")
        resposta_final = resposta_final.strip()

        print("\n" + "="*30)
        print(f"PERGUNTA: {pergunta_usuario}")
        print("="*30)
        print(f"RESPOSTA:\n{resposta_final}")

except KeyboardInterrupt:
    print("\nEncerrando o assistente...")

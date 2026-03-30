import streamlit as st
import ollama
import chromadb
import json

# --- Configurações da Página ---
st.set_page_config(page_title="Assistente do Alcorão", page_icon="🌙")
st.title("🌙 Consulta Semântica ao Alcorão")

# --- Funções de Backend (Mantendo sua lógica original) ---
@st.cache_resource # Evita carregar o banco toda vez que a tela atualiza
def init_resources():
    client = chromadb.PersistentClient(path="./quran_bge_m3_db")
    collection = client.get_or_create_collection(
        name="quran_pt_br", 
        metadata={"hnsw:space": "cosine"}
    )
    return collection

collection = init_resources()
MODEL_EMBEDDING = 'bge-m3'
MODEL_LLM = 'gemma3:27b-cloud'

def expandir_pergunta(pergunta):
    prompt = f"Transforme esta pergunta em palavras-chave e conceitos do Alcorão para busca semântica: {pergunta}. Responda apenas os termos."
    response = ollama.generate(model=MODEL_LLM, prompt=prompt)
    return response['response']

def gerar_resposta_final(pergunta, contextos):
    contexto_str = "\n".join([f"- {c}" for c in contextos])
    prompt = f"Baseado nestes versículos: {contexto_str}\n\nResponda: {pergunta}\nIndique as Suratas."
    response = ollama.generate(model=MODEL_LLM, prompt=prompt)
    return response['response']

# --- Interface de Chat ---

# Inicializa o histórico na sessão do navegador
if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe as mensagens do histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada do usuário
if prompt_usuario := st.chat_input("Pergunte algo sobre o Alcorão..."):
    
    # 1. Mostra a pergunta do usuário
    st.session_state.messages.append({"role": "user", "content": prompt_usuario})
    with st.chat_message("user"):
        st.markdown(prompt_usuario)

    # 2. Processamento (RAG)
    with st.chat_message("assistant"):
        with st.spinner("Consultando versículos..."):
            # Lógica original
            busca_otimizada = expandir_pergunta(prompt_usuario)
            res_query = ollama.embed(model=MODEL_EMBEDDING, input=busca_otimizada)
            results = collection.query(query_embeddings=[res_query['embeddings'][0]], n_results=5)
            textos = results['documents'][0]
            
            resposta = gerar_resposta_final(prompt_usuario, textos)
            
            # Limpeza
            #resposta = resposta.replace("*", "").replace("#", "").strip()
            
            st.markdown(resposta)
            
            # Adiciona ao histórico da sessão
            st.session_state.messages.append({"role": "assistant", "content": resposta})

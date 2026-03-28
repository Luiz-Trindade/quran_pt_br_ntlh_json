import os
import json
from pathlib import Path

def split_quran_json(input_file: str = "quran_pt_br_ntlh.json", output_dir: str = "suras"):
    """
    Divide o arquivo JSON grande do Alcorão em arquivos individuais por sura.
    Cada arquivo conterá apenas uma sura completa.
    """
    
    # Criar pasta de saída se não existir
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    try:
        print(f"Carregando arquivo: {input_file}")
        with open(input_file, "r", encoding="utf-8") as f:
            quran_data = json.load(f)
        
        print(f"Arquivo carregado com sucesso! Total de suras: {len(quran_data)}\n")
        
        for sura in quran_data:
            sura_id = sura.get("id")
            sura_name = sura.get("transliteration", f"Sura_{sura_id}")
            sura_arabic = sura.get("name", "")
            
            # Nome do arquivo: sura-001.json, sura-002.json, ..., sura-114.json
            filename = f"sura-{sura_id:03d}.json"
            file_path = output_path / filename
            
            # Criar o objeto com apenas os dados da sura
            sura_data = {
                "id": sura.get("id"),
                "name": sura.get("name"),                    # Nome em árabe
                "transliteration": sura.get("transliteration"),
                "translation": sura.get("translation"),
                "type": sura.get("type"),
                "total_verses": sura.get("total_verses"),
                "verses": sura.get("verses", [])             # Apenas os ayats
            }
            
            # Salvar arquivo individual
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(sura_data, f, ensure_ascii=False, indent=2)
            
            print(f"✓ Criado: {filename} → {sura_id:03d} | {sura_name} ({sura_arabic}) | {len(sura_data['verses'])} ayats")
        
        print(f"\n✅ Concluído! {len(quran_data)} suras foram salvas na pasta '{output_dir}/'")
        print(f"   Local: {output_path.absolute()}")
        
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo '{input_file}' não encontrado.")
    except json.JSONDecodeError:
        print(f"❌ Erro: O arquivo '{input_file}' não é um JSON válido.")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

# ===================== EXECUÇÃO =====================
if __name__ == "__main__":
    # Você pode mudar os caminhos aqui se quiser
    split_quran_json(
        input_file="quran_pt_br_ntlh.json",   # ← Seu arquivo original
        output_dir="suras"                    # ← Pasta que será criada
    )
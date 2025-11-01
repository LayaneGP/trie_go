import os
import re
import json
import math
from collections import defaultdict
from compact_trie import TrieCompacta, TrieNode

# conversão Trie <-> dict
def trie_to_dict(node):
    data = {
        "label": node.label,
        "is_word": node.is_word,
        "doc_ids": node.doc_ids,
        "stats": node.stats,
        "children": {k: trie_to_dict(v) for k, v in node.children.items()}
    }
    return data

def dict_to_trie(d):
    node = TrieNode(d["label"])
    node.is_word = d["is_word"]
    node.doc_ids = {int(k): v for k, v in d["doc_ids"].items()}
    node.stats = d["stats"]
    node.children = {k: dict_to_trie(v) for k, v in d["children"].items()}
    return node

# calvar/carregar índice JSON
def salvar_indice_json(trie, doc_metadata, filename):
    data = {
        "trie": trie_to_dict(trie.root),
        "docs": doc_metadata
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def carregar_indice_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    trie = TrieCompacta()
    trie.root = dict_to_trie(data["trie"])
    doc_metadata = {int(k): v for k, v in data["docs"].items()}
    return trie, doc_metadata

# calcular zscore
def calcular_estatisticas_recursivas(node, N_total_docs):
    if node.is_word:
        all_freqs = [node.doc_ids.get(doc_id, 0) for doc_id in range(1, N_total_docs + 1)]
        mu = sum(all_freqs) / N_total_docs
        variance = sum((x - mu) ** 2 for x in all_freqs) / N_total_docs
        sigma = math.sqrt(variance)
        node.stats['mu'] = mu
        node.stats['sigma'] = sigma

    for child in node.children.values():
        calcular_estatisticas_recursivas(child, N_total_docs)

# indexação de documentos
def indexar_documentos(corpus_path, json_file="indice.json"):
    
    # se já existe índice, carrega
    if os.path.exists(json_file):
        return carregar_indice_json(json_file)

    trie = TrieCompacta()
    doc_metadata = {}
    doc_id = 0
    
    all_files = []
    for root, dirs, files in os.walk(corpus_path):
        for filename in files:
            if filename.endswith(".txt") and ":Zone.Identifier" not in filename:
                all_files.append(os.path.join(root, filename))

    N_total_docs = len(all_files)
    
    if N_total_docs == 0:
        print("Nenhum documento de texto válido encontrado no corpus.")
        return trie, doc_metadata 

    for filepath in all_files:
        doc_id += 1
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                texto = f.read()
        except UnicodeDecodeError:
            print(f"Não foi possível ler o arquivo {filepath}.")
            doc_id -= 1
            continue

        # caminho relativo à pasta dos documentos
        rel_path = os.path.relpath(filepath, corpus_path).replace("\\", "/")

        # metadata do documento
        doc_metadata[doc_id] = {
            "nome": os.path.basename(filepath),
            "texto": texto,
            "caminho_relativo": rel_path
        }

        # contagem de palavras
        word_counts = defaultdict(int)
        tokens = re.findall(r"[a-zA-Z\-]+", texto.lower())
        for token in tokens:
            word_counts[token] += 1
            
        for token, frequency in word_counts.items():
            trie.insert(token, doc_id, frequency)

    # calcula mu e sigma
    calcular_estatisticas_recursivas(trie.root, N_total_docs)

    # salva índice
    salvar_indice_json(trie, doc_metadata, json_file)
    
    return trie, doc_metadata

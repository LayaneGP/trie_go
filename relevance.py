import math
from collections import defaultdict

def calcular_zscores_e_relevancia(trie, docs_encontrados, query_terms):
    zscores = defaultdict(dict)
    relevancia = {}
    #pega dados da trie
    term_data = {}
    for term in query_terms:
        posting_list, stats = trie.search(term)
        #armazena posting list mu, sigma se existir
        if posting_list and stats:
            term_data[term] = {'postings': posting_list, 'stats': stats}
    for doc_id in docs_encontrados: 
        doc_zscores = {}
        termos_presentes = 0
        total_zscore = 0
        
        for term, data in term_data.items():
            mu = data['stats']['mu']
            sigma = data['stats']['sigma']
            frequencia_x = data['postings'].get(doc_id, 0)

            if frequencia_x > 0:
                
                # se sigma for zero z-score e 0
                z = (frequencia_x - mu) / sigma if sigma != 0 else 0
                
                doc_zscores[term] = z
                total_zscore += z
                termos_presentes += 1
        
        if termos_presentes > 0:
            relevancia[doc_id] = total_zscore / termos_presentes
            zscores[doc_id] = doc_zscores
        else:
             relevancia[doc_id] = 0

    return dict(zscores), relevancia

def ordenar_resultados_por_relevancia(relevancia):
    #mais relevante para o menos relevante
    
    return sorted(relevancia.keys(), key=lambda x: relevancia[x], reverse=True)


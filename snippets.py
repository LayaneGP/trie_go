import re

def gerar_snippet(doc_texto, termo, chars_antes=80, chars_depois=80):
    
    termo_lower = termo.lower()
    texto_lower = doc_texto.lower()
    
    match = re.search(r'\b{}\b'.format(re.escape(termo_lower)), texto_lower)
    
    if not match:
        match = re.search(re.escape(termo_lower), texto_lower)
        
        if not match:
            return doc_texto[:chars_antes + chars_depois] + "..."
    
    start, end = match.start(), match.end()
    # limites snippet
    snippet_start = max(0, start - chars_antes)
    snippet_end = min(len(doc_texto), end + chars_depois)
    
    prefixo = "..." if snippet_start > 0 else ""
    sufixo = "..." if snippet_end < len(doc_texto) else ""
    
    # marca-texto na palabra encontrada
    snippet = prefixo + \
              doc_texto[snippet_start:start] + \
              '<span class="highlight">' + doc_texto[start:end] + '</span>' + \
              doc_texto[end:snippet_end] + \
              sufixo
              
    return snippet

def gerar_snippets_por_documento(resultados_pagina, doc_metadata, zscores):
    #identifica o termo mais relevante e gera o snippet centrado nele
    snippets = {}
    for doc_id in resultados_pagina:
        
        termo_mais_relevante = max(zscores[doc_id], key=lambda t: zscores[doc_id][t])
        
        texto = doc_metadata[doc_id]["texto"]
        snippets[doc_id] = gerar_snippet(texto, termo_mais_relevante)
        
    return snippets
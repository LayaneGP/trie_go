from flask import Flask, render_template, request, send_from_directory
from indexing import indexar_documentos
from query import tokenize_query, to_rpn, evaluate_rpn
from relevance import calcular_zscores_e_relevancia, ordenar_resultados_por_relevancia
from snippets import gerar_snippets_por_documento
import os

app = Flask(__name__)

# carregar índice ao iniciar
try:
    TRIE, DOCS = indexar_documentos(
        os.path.join(os.path.dirname(__file__), "static/bbc_news"), 
        json_file="indice.json"
    )
except Exception as e:
    print(f"ERRO CRÍTICO AO CARREGAR ÍNDICE: {e}")
    TRIE, DOCS = None, None

RESULTS_PER_PAGE = 10

# rotas flask
@app.route("/", methods=["GET"])
def index():
    if TRIE is None:
        return "Erro na inicialização do índice. Verifique o terminal.", 500
    return render_template("index.html")


@app.route("/results", methods=["POST"])
def results():
    query = request.form.get("query", "")
    page = int(request.form.get("page", 1))

    if not query:
        return render_template("index.html", error="Digite uma consulta!")

    # busca booleana
    tokens = tokenize_query(query)
    rpn = to_rpn(tokens)
    docs_dados_filtrados = evaluate_rpn(rpn, TRIE)

    if not docs_dados_filtrados:
        return render_template(
            "results.html", query=query, resultados=[], mensagem="Nenhum documento encontrado.", page=page, total_pages=1
        )

    query_terms = [t.lower() for t in tokens if t.isalpha() and t not in ("AND", "OR")]

    # ranqueamento
    zscores, relevancia = calcular_zscores_e_relevancia(TRIE, docs_dados_filtrados.keys(), query_terms)

    # ordenação
    resultados_ordenados = ordenar_resultados_por_relevancia(relevancia)

    # paginação
    total_resultados = len(resultados_ordenados)
    total_pages = (total_resultados + RESULTS_PER_PAGE - 1) // RESULTS_PER_PAGE
    page = max(1, min(page, total_pages))
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    resultados_pagina = resultados_ordenados[start:end]

    # geração de snippet
    snippets = gerar_snippets_por_documento(resultados_pagina, DOCS, zscores)

    return render_template(
        "results.html",
        query=query,
        resultados=resultados_pagina,
        doc_metadata=DOCS,
        snippets=snippets,
        page=page,
        total_pages=total_pages
    )

# rota para servir arquivos da pasta bbc_news
@app.route("/bbc_news/<path:filename>")
def serve_bbc_news(filename):
    bbc_path = os.path.join(app.root_path, "static", "bbc_news")
    return send_from_directory(bbc_path, filename)


# executando no servidor
if __name__ == "__main__":
    port = 8000
    url = f"http://127.0.0.1:{port}/"
    print(f"Iniciando o servidor na porta {port}...")

    import webbrowser
    import os
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open_new_tab(url)

    app.run(debug=True, host="0.0.0.0", port=port)

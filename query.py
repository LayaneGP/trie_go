import re
from collections import defaultdict
precedence = {"AND": 2, "OR": 1}

def tokenize_query(query):
    return re.findall(r'\(|\)|AND|OR|[a-zA-Z\-]+', query)

def to_rpn(tokens):
    #shunting-yard
    output = []
    stack = []
    for token in tokens:
        if token.isalpha() and token not in ("AND", "OR"):
            output.append(token.lower())
        elif token in ("AND", "OR"):
            while stack and stack[-1] != "(" and precedence.get(stack[-1], 0) >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()
    while stack:
        output.append(stack.pop())
    return output



def intersecao_com_dados(doc_data_a, doc_data_b):
    resultado = defaultdict(dict)
    chaves_a = set(doc_data_a.keys())
    chaves_b = set(doc_data_b.keys())
    for doc_id in chaves_a.intersection(chaves_b):
        resultado[doc_id].update(doc_data_a[doc_id])
        resultado[doc_id].update(doc_data_b[doc_id])
    return resultado

def uniao_com_dados(doc_data_a, doc_data_b):
    resultado = defaultdict(dict)
    chaves_a = set(doc_data_a.keys())
    chaves_b = set(doc_data_b.keys())
    for doc_id in chaves_a.union(chaves_b):
        if doc_id in doc_data_a:
            resultado[doc_id].update(doc_data_a[doc_id])
        if doc_id in doc_data_b:
            resultado[doc_id].update(doc_data_b[doc_id])
    return resultado



def evaluate_rpn(rpn_tokens, trie):
    stack = []
    for token in rpn_tokens:
        if token.isalpha() and token not in ("AND", "OR"):
            posting_list, stats = trie.search(token)
            doc_data = defaultdict(dict)
            if posting_list:
                for doc_id, freq_x in posting_list.items():
                    doc_data[doc_id][token] = freq_x
            stack.append(doc_data)
        elif token == "AND":
            b = stack.pop()
            a = stack.pop()
            stack.append(intersecao_com_dados(a, b))
        elif token == "OR":
            b = stack.pop()
            a = stack.pop()
            stack.append(uniao_com_dados(a, b))
    return stack[0] if stack else {}
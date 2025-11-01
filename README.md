# 🚀 DCC207 - Máquina de Busca Híbrida (Trabalho Prático 1)

## Alunos

* **Isabela Ramos dos Santos** (Matrícula: 2023034757)
* **Layane Garcia** (Matrícula: 2023034765)

---

## 💡 Visão Geral do Projeto

Este projeto implementa um protótipo de máquina de busca para o corpus BBC News (2225 documentos). O sistema atua de forma **híbrida**: usa lógica booleana para filtrar documentos e o ranqueamento por **Z-score** para ordená-los por relevância.

-   **Indexação:** Utiliza uma \*\*Trie Compacta\*\* customizada para armazenar o índice em memória principal.
-   **Ranqueamento:** Os resultados são ordenados pela média dos \*\*Z-scores\*\* dos termos da consulta, medindo a concentração temática.
-   **Interface:** Implementada em Flask, com paginação e \*\*snippets\*\* destacados.

---

## 🛠️ 1. Configuração e Inicialização

O projeto foi configurado com um bloco de execução robusto para evitar conflitos de porta no ambiente WSL/Linux.

### 1.1. Configuração Inicial

1.  **Pré-requisitos:** Python 3.9+ e Flask.
2.  **Ambiente Virtual:** Na pasta raiz do projeto, crie e ative o ambiente virtual e instale o Flask:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Para Linux/WSL
    pip install Flask
    ```
3.  **Corpus:** A pasta `bbc_news/` contém os documentos.

### 1.2. Execução do Servidor (Método Robusto)

O comando abaixo executa o `app.py` e inicia o servidor na primeira porta livre que encontrar (tentando 8080, 8081, 9000, etc.).

1.  **Comando de Execução:** Execute o arquivo principal diretamente:

    ```bash
    python3 app.py
    ```

2.  **Acesso:** O terminal notificará a porta utilizada (Ex: 8080 ou 9000). O navegador será aberto automaticamente (ou acesse manualmente):

    $$\text{http://127.0.0.1:[PORTA\_LIVRE]/}$$

---

## 🔍 2. Testes de Corretude (Validação da Lógica)

Utilize estes exemplos de consulta para validar o processamento booleano e o ranqueamento estatístico.

| Consulta | Lógica Testada |
| :--- | :--- |
| `technology AND phone` | Interseção ($\text{AND}$) e Relevância Temática. |
| `economy OR politics` | União ($\text{OR}$) e Ranqueamento em Conjuntos Grandes. |
| `(apple OR google) AND tech` | Precedência (Parênteses) e Interseção. |
| `hi-tech` | Tokenização Correta de Palavra Composta (Hífen). |

### Destaques da Implementação

* \*\*Persistência:\*\* O arquivo \`indice.json\` é gerado e lido por \*\*serialização manual\*\*, atendendo à restrição de não usar \texttt{pickle}.
* \*\*Ranqueamento:\*\* O Módulo RI utiliza os valores persistidos de $\mu$ e $\sigma$ para calcular o Z-score, garantindo a ordenação correta.
* \*\*Usabilidade:\*\* A paginação está configurada para \*\*10 resultados por página\*\* e suporta navegação direta por número de página.

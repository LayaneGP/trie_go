# 🚀 DCC207 - Máquina de Busca Híbrida (Trabalho Prático 1)

## Alunos

* **Isabela Ramos dos Santos** (Matrícula: 2023034757)
* **Layane Garcia** (Matrícula: 2023034765)

---

## 💡 Visão Geral do Projeto

[cite_start]Este projeto implementa um protótipo de máquina de busca para o corpus BBC News (2225 documentos) [cite: 17, 18][cite_start], unindo algoritmos de estrutura de dados avançados com lógica de Recuperação de Informação (RI)[cite: 13, 16]. [cite_start]O sistema atua de forma **híbrida** [cite: 33][cite_start]: usa lógica booleana para filtrar documentos [cite: 34] [cite_start]e o ranqueamento por **Z-score** para ordená-los por relevância[cite: 40].

-   [cite_start]**Indexação:** Utiliza uma \*\*Trie Compacta\*\* customizada [cite: 23, 24] [cite_start]para armazenar o índice em memória principal[cite: 22].
-   [cite_start]**Ranqueamento:** Os resultados são ordenados pela média dos \*\*Z-scores\*\* dos termos da consulta[cite: 40], medindo a concentração temática.
-   [cite_start]**Interface:** Implementada em Flask [cite: 46][cite_start], com paginação [cite: 43] [cite_start]e \*\*snippets\*\* destacados[cite: 43].

---

## 🛠️ 1. Configuração e Inicialização

O projeto foi configurado com um bloco de execução robusto para evitar conflitos de porta no ambiente WSL/Linux.

### 1.1. Configuração Inicial

1.  [cite_start]**Pré-requisitos:** Python 3.9+ [cite: 53] [cite_start]e Flask[cite: 54].
2.  **Ambiente Virtual:** Na pasta raiz do projeto, crie e ative o ambiente virtual e instale o Flask:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Para Linux/WSL
    pip install Flask
    ```
3.  [cite_start]**Corpus:** A pasta `bbc_news/` contém os documentos[cite: 17].

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

[cite_start]Utilize estes exemplos de consulta para validar o processamento booleano [cite: 34] [cite_start]e o ranqueamento estatístico[cite: 40].

| Consulta | Lógica Testada |
| :--- | :--- |
| `tech AND phone` | [cite_start]Interseção ($\text{AND}$) e Relevância Temática[cite: 35]. |
| `economy OR politics` | [cite_start]União ($\text{OR}$) e Ranqueamento em Conjuntos Grandes[cite: 35]. |
| `the or this` | [cite_start]Precedência (Parênteses) e Interseção[cite: 36]. |

### Destaques da Implementação

* [cite_start]\*\*Persistência:\*\* O arquivo \`indice.json\` é gerado e lido por \*\*serialização manual\*\*, atendendo à restrição de não usar \texttt{pickle}[cite: 30].
* [cite_start]\*\*Ranqueamento:\*\* O Módulo RI utiliza os valores persistidos de $\mu$ e $\sigma$ para calcular o Z-score, garantindo a ordenação correta[cite: 40].
* [cite_start]\*\*Usabilidade:\*\* A paginação está configurada para \*\*10 resultados por página\*\* [cite: 43] e suporta navegação direta por número de página.

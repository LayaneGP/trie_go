# arquivo: rename_corpus.py
import os

# diretório raiz do corpus
CORPUS_ROOT = "static/bbc_news"

# mapeamento de pastas para prefixos (primeira letra da pasta)
PREFIX_MAP = {
    "business": "b",
    "entertainment": "e",
    "politics": "p",
    "sport": "s",
    "tech": "t"
}

def rename_documents(root_dir):
    """Percorre as pastas e renomeia os arquivos com o prefixo da categoria, 
    apenas se ainda não estiverem renomeados.
    """
    print("Iniciando renomeação do corpus...")

    for folder_name, prefix in PREFIX_MAP.items():
        folder_path = os.path.join(root_dir, folder_name)

        if not os.path.isdir(folder_path):
            print(f"Aviso: Pasta {folder_name} não encontrada.")
            continue

        print(f"\nProcessando pasta: {folder_name} (Prefixo: {prefix})")

        for filename in os.listdir(folder_path):
            # ignora arquivos não .txt ou metadados
            if not filename.endswith(".txt") or ":Zone.Identifier" in filename:
                continue

            old_filepath = os.path.join(folder_path, filename)

            # se o arquivo já começa com o prefixo correto, pula
            if filename.lower().startswith(prefix.lower()):
                # print(f"  Ignorado (já renomeado): {filename}")
                continue

            # caso contrário, adiciona o prefixo
            new_filename = f"{prefix}{filename}"
            new_filepath = os.path.join(folder_path, new_filename)

            try:
                os.rename(old_filepath, new_filepath)
                # print(f"  Renomeado: {filename} -> {new_filename}")
            except Exception as e:
                print(f"  Erro ao renomear {filename}: {e}")

    print("\n✅ Renomeação concluída.")


if __name__ == "__main__":
    rename_documents(CORPUS_ROOT)

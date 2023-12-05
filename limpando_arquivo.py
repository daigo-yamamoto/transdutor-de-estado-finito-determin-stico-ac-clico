import unidecode

def clean_and_sort_words(file_path):
    # Lendo o conteúdo do arquivo
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.readlines()

    # Removendo acentos e apóstrofes, convertendo para minúsculas e removendo espaços em branco
    cleaned_words = [unidecode.unidecode(word.strip().lower()).replace("'", "") for word in words]

    # Ordenando as palavras
    sorted_words = sorted(cleaned_words)

    # Sobrescrevendo o arquivo com as palavras processadas
    with open(file_path, 'w', encoding='utf-8') as file:
        for word in sorted_words:
            file.write(word + '\n')

# Caminho do seu arquivo
file_path = './dicionario/american-english.txt'  # Substitua pelo caminho correto do arquivo

# Chamar a função
clean_and_sort_words(file_path)

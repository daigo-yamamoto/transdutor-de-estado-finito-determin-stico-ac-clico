import fst
import trie
import tkinter as tk
from tkinter import scrolledtext
import time
import tracemalloc

def read_words_from_file(file_path):
    words = []
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()  # Remove espaços em branco e quebras de linha
            if word:  # Verifica se a linha não está vazia
                words.append(word)
    return words


def update_results():
    prefix = prefix_entry.get()

    # Iniciar o rastreamento de memória
    tracemalloc.start()

    # Medir o tempo e a memória para o FST
    start_time = time.time()
    fst_results = fst.autocomplete(my_fst, prefix)
    fst_time = time.time() - start_time
    _, fst_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Reiniciar o rastreamento de memória para o TRIE
    tracemalloc.start()

    # Medir o tempo e a memória para o TRIE
    start_time = time.time()
    trie_results = my_trie.autocomplete(prefix)
    trie_time = time.time() - start_time
    _, trie_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Atualizar as áreas de texto
    fst_text.delete('1.0', tk.END)
    fst_text.insert(tk.END, '\n'.join(fst_results))

    trie_text.delete('1.0', tk.END)
    trie_text.insert(tk.END, '\n'.join(trie_results))

    # Atualizar os rótulos de tempo e memória para o FST
    fst_time_label.config(text=f"Tempo do FST: {fst_time:.6f} seg")
    fst_memory_label.config(text=f"Memória do FST: {fst_memory} bytes")

    # Atualizar os rótulos de tempo e memória para o TRIE
    trie_time_label.config(text=f"Tempo do TRIE: {trie_time:.6f} seg")
    trie_memory_label.config(text=f"Memória do TRIE: {trie_memory} bytes")

window = tk.Tk()
window.title("Autocompletar com FST e TRIE")

# Pegando as palavras
file_path = './dicionario/meses.txt'
words = read_words_from_file(file_path)

# Criando a fst
my_fst, _ = fst.create_fst(words)

#Criando a trie
my_trie = trie.Trie()
trie.build_trie(my_trie, words)

# Campo de entrada para o prefixo
prefix_label = tk.Label(window, text="Digite o prefixo:")
prefix_label.pack()
prefix_entry = tk.Entry(window)
prefix_entry.pack()

# Área de texto para resultados do FST
fst_label = tk.Label(window, text="Resultados do FST:")
fst_label.pack()
fst_text = scrolledtext.ScrolledText(window, height=10)
fst_text.pack()

# Área de texto para resultados do TRIE
trie_label = tk.Label(window, text="Resultados do TRIE:")
trie_label.pack()
trie_text = scrolledtext.ScrolledText(window, height=10)
trie_text.pack()

# Rótulos para exibir o tempo e a memória do FST
fst_time_label = tk.Label(window, text="Tempo do FST:")
fst_time_label.pack()
fst_memory_label = tk.Label(window, text="Memória do FST:")
fst_memory_label.pack()

# Rótulos para exibir o tempo e a memória do TRIE
trie_time_label = tk.Label(window, text="Tempo do TRIE:")
trie_time_label.pack()
trie_memory_label = tk.Label(window, text="Memória do TRIE:")
trie_memory_label.pack()

prefix_entry.bind('<KeyRelease>', lambda event: update_results())
window.mainloop()

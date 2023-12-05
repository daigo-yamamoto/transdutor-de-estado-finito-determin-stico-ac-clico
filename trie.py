from graphviz import Digraph

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True


    def _search_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def _autocomplete_helper(self, node, prefix, results):
        if node.is_end_of_word:
            results.append(prefix)
        for char, next_node in node.children.items():
            self._autocomplete_helper(next_node, prefix + char, results)

    def autocomplete(self, prefix):
        node = self._search_node(prefix)
        if not node:
            return []
        results = []
        self._autocomplete_helper(node, prefix, results)
        return results

    def visualize(self):
        dot = Digraph(comment='The Trie')

        def add_nodes_and_edges(node, node_id=0):
            if node.is_end_of_word:
                dot.node(str(node_id), shape='doublecircle')  # Nó final com círculo duplo
            else:
                dot.node(str(node_id))

            for char, child in node.children.items():
                child_id = id(child)  # Usando a identificação do objeto Python para identificar unicamente os nós
                if child.is_end_of_word:
                    dot.node(str(child_id), char, shape='doublecircle')
                else:
                    dot.node(str(child_id), char)
                dot.edge(str(node_id), str(child_id))
                add_nodes_and_edges(child, child_id)

        add_nodes_and_edges(self.root)

        dot.render('output/fst_graph', view=True)

def read_words_from_file(file_path):
    words = []
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()  # Remove espaços em branco e quebras de linha
            if word:  # Verifica se a linha não está vazia
                words.append(word)
    return words

def build_trie(trie, words):
    for word in words:
        trie.insert(word)

'''
  Teste da trie
'''
file_path = './dicionario/meses.txt'
words = read_words_from_file(file_path)

trie = Trie()
build_trie(trie, words)
trie.visualize()

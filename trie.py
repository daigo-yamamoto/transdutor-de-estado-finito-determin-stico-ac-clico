from graphviz import Digraph

class TrieNode:
    def __init__(self):
        self.subtree_representation = None
        self.children = {}  # Dicionário para armazenar os filhos
        self.is_end_of_word = False  # Indica se é o fim de uma palavra
        self.index = None

    def compute_subtree_representation(self):
        # Criar uma lista para armazenar as representações dos filhos
        child_representations = []

        # Iterar sobre os filhos e obter suas representações
        for char, child_node in sorted(self.children.items()):
            child_node.compute_subtree_representation()
            child_representations.append((char, child_node.subtree_representation))

        # Incorporar a informação de ser um nó final
        end_of_word_marker = '1' if self.is_end_of_word else '0'

        # Criar a representação da sub-árvore (aqui usamos uma string, mas poderia ser um hash)
        self.subtree_representation = end_of_word_marker + ''.join([f'({char},{rep})' for char, rep in child_representations])

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.next_index = 0  # Inicializando um contador para índices

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        # Atribua um índice ao nó se ainda não tiver um
        if node.index is None:
            node.index = self.next_index
            self.next_index += 1

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def find_prefix_node(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def compute_subtree_representations(self):
        self._compute_subtree_representations(self.root)

    def _compute_subtree_representations(self, node):
        for child in node.children.values():
            self._compute_subtree_representations(child)
        node.compute_subtree_representation()

    def find_words_from_node(self, node, prefix):
        words = []
        if node.is_end_of_word:
            words.append(prefix)

        for char, next_node in node.children.items():
            words += self.find_words_from_node(next_node, prefix + char)

        return words

    def autocomplete(self, prefix):
        prefix_node = self.find_prefix_node(prefix)
        if prefix_node is None:
            return []  # Nenhum prefixo encontrado
        return self.find_words_from_node(prefix_node, prefix)

def draw_trie(trie_root, file_path):
    dot = Digraph(comment='Trie')

    def add_nodes_and_edges(node, parent_index=None, edge_label=''):
        if node.index is None:  # Certifique-se de que o índice não seja None
            return

        node_id = str(node.index)
        if node.is_end_of_word:
            dot.node(node_id, label=node_id, shape='doublecircle')
        else:
            dot.node(node_id, label=node_id)

        if parent_index is not None:
            dot.edge(str(parent_index), node_id, label=edge_label)

        for char, child in node.children.items():
            if child.index is not None:  # Certifique-se de que o filho tenha um índice
                add_nodes_and_edges(child, node.index, edge_label=char)

    add_nodes_and_edges(trie_root)

    dot.render(file_path, view=True)

def build_trie_from_file(trie, file_path):
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()  # Remove espaços e quebras de linha
            trie.insert(word)
    return trie

'''
  Teste da trie
'''
file_path = "./dicionario/semana.txt"
trie = Trie()
build_trie_from_file(trie, file_path)
draw_trie(trie.root, file_path)
print(trie.autocomplete("t"))

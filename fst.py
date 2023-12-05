import copy
from graphviz import Digraph
from queue import Queue
import levenshein

class FstNode:
    def __init__(self):
        self.next = []
        self.output = []
        self.is_end_of_word = False


def longest_common_prefix(str1, str2):
    min_length = min(len(str1), len(str2))
    common_prefix = ""

    for i in range(min_length):
        if str1[i] == str2[i]:
            common_prefix += str1[i]
        else:
            break
    return common_prefix


def final(state):
    return state.is_end_of_word


def set_final(state, bool):
    if bool:
        state.next = [(None, None, '')]
    state.is_end_of_word = bool


def transition(state, char):
    final_state = None
    for next_state in state.next:
        if next_state[1] == char:
            final_state = state.next[state.next.index(next_state)][0]
        return final_state


def set_transition(initial_state, char, final_state):
    for next_state in initial_state.next:
        if next_state[1] == char:
            initial_state.next[initial_state.next.index(next_state)] = (final_state, ) + initial_state.next[initial_state.next.index(next_state)][1:]
            return

    initial_state.next.append((final_state, char, ''))


def state_output(state):
    return state.output


def set_state_output(state, list):
    state.output = list


def output(state, char):
    string = ''
    for next_state in state.next:
        if next_state[1] == char:
            string = state.next[state.next.index(next_state)][2]
        return string


def set_output(state, char, string):
    for next_state in state.next:
        if next_state[1] == char:
            state.next[state.next.index(next_state)] = state.next[state.next.index(next_state)][:2] + (string, )


def clear_state(state):
    state.next = []
    state.output = []
    state.is_end_of_word = False


def member(list, state):
    # Criar um dicionário para contar a frequência dos elementos em state.next
    state_freq = {}
    for item in state.next:
        state_freq[item] = state_freq.get(item, 0) + 1

    for element in list:
        # Se os tamanhos são diferentes, pula para o próximo elemento
        if len(element.next) != len(state.next):
            continue

        # Criar um dicionário para contar a frequência dos elementos em element.next
        element_freq = {}
        for item in element.next:
            element_freq[item] = element_freq.get(item, 0) + 1

        # Comparar os dois dicionários
        if state_freq == element_freq:
            return element

    return None


def find_minimized(list, state):
    r = member(list, state)
    if r is None:
        r = copy.copy(state)
        list.append(r)
    return r


def create_fst(input):  #input é uma lista de palavras
    currentWord = ''
    previousWord = ''
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    tempState = []
    outList = []
    maxWordSize = 0

    for string in input:  # Procurando a maior palavra
        if len(string) > maxWordSize:
            maxWordSize = len(string)

    for i in range(maxWordSize + 1):
        tempState.append(FstNode())

    clear_state(tempState[0])

    i_out = 1

    for string in input:
        currentWord = string
        currentOutput = str(i_out)
        i_out = i_out + 1
        i = 1

        while (i <= len(currentWord)) and (i <= len(previousWord)) and (previousWord[i - 1] == currentWord[i - 1]):
            i = i + 1

        prefixLengthPlus1 = i

        # we minimize the states from the suffix of the previous word
        for j in range(len(previousWord), prefixLengthPlus1 - 1, -1):
            set_transition(tempState[j-1], previousWord[j-1], find_minimized(outList, tempState[j]))

        # This loop initializes the tail states for the current word
        for j in range(prefixLengthPlus1, len(currentWord) + 1):
            clear_state(tempState[j])
            set_transition(tempState[j-1], currentWord[j-1], tempState[j])

        if currentWord is not previousWord:
            set_final(tempState[len(currentWord)], True)
            set_state_output(tempState[len(currentWord)], [])

        for j in range(1, prefixLengthPlus1):
            commonPrefix = longest_common_prefix(output(tempState[j-1], currentWord[j-1]), currentOutput)
            wordSuffix = output(tempState[j-1], currentWord[j-1]).replace(commonPrefix, '')
            set_output(tempState[j-1], currentWord[j-1], commonPrefix)

            for ch in alphabet:
                if transition(tempState[j], ch) is not None:
                    set_output(tempState[j], ch, wordSuffix + output(tempState[j], ch))

            if final(tempState[j]):
                tempSet = []
                if state_output(tempState[j]):
                    for tempString in state_output(tempState[j]):
                        tempSet.append(wordSuffix + tempString)
                set_state_output(tempState[j], tempSet)

            currentOutput = currentOutput.replace(commonPrefix, '')

        if currentWord == previousWord:
            set_state_output(tempState[len(currentWord)], state_output(tempState[len(currentWord)]).append(currentOutput))
        else:
            set_output(tempState[prefixLengthPlus1-1], currentWord[prefixLengthPlus1-1], currentOutput)

        previousWord = currentWord

    # here we are minimizing the states of the last word
    for i in range(len(currentWord), 0, -1):
        set_transition(tempState[i-1], previousWord[i-1], find_minimized(outList, tempState[i]))

    initialState = find_minimized(outList, tempState[0])

    return initialState, outList


def autocomplete(root, prefix):
    # Primeiro, encontramos o estado que corresponde ao último caractere do sufixo
    def find_state(node, suffix):
        for char in suffix:
            next_node = None
            for next_state, transition_char, _ in node.next:
                if transition_char == char:
                    next_node = next_state
                    break
            if next_node is None:
                return None  # Se não encontrarmos o sufixo no FST, retornamos None
            node = next_node
        return node

    # Depois, realizamos uma busca em profundidade para encontrar todas as palavras completas
    def dfs(node, current_word, complete_words):
        if node.is_end_of_word:
            complete_words.append(current_word)
        for next_node, char, _ in node.next:
            if char:  # Ignora transições vazias
                dfs(next_node, current_word + char, complete_words)

    state = find_state(root, prefix)
    if state is None:
        return []  # Se o sufixo não existir no FST, retorna uma lista vazia

    complete_words = []
    dfs(state, prefix, complete_words)
    return complete_words


def fst_to_graphviz(initial_state):
    dot = Digraph(comment='Finite State Transducer')
    visited_states = set()  # Conjunto de estados visitados
    state_queue = Queue()   # Fila para a busca em largura
    state_ids = {}          # Dicionário para mapear estados para IDs
    next_id = 0             # Contador para gerar IDs sequenciais

    # Função auxiliar para adicionar um nó ao gráfico
    def add_node(state):
        if state in visited_states:
            return

        nonlocal next_id
        state_id = str(next_id)
        state_ids[state] = state_id
        next_id += 1
        # Verifica se o estado é um estado final (is_end_of_word == True)
        node_shape = 'doublecircle' if state.is_end_of_word else 'circle'
        dot.node(state_id, label=state_id, shape=node_shape)
        visited_states.add(state)
        state_queue.put(state)

    add_node(initial_state)  # Inicia a travessia pelo estado inicial

    while not state_queue.empty():
        current_state = state_queue.get()
        current_state_id = state_ids[current_state]

        for next_state, char, output in current_state.next:
            if next_state is not None:
                if next_state not in visited_states:
                    add_node(next_state)
                next_state_id = state_ids[next_state]
                label = f"{char}" if char and output else char or output or 'ε'
                dot.edge(current_state_id, next_state_id, label=label)

    return dot


def read_words_from_file(file_path):
    words = []
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()  # Remove espaços em branco e quebras de linha
            if word:  # Verifica se a linha não está vazia
                words.append(word)
    return words


# Teste do FST
#file_path = './dicionario/meses.txt'
#word_list = read_words_from_file(file_path)

#estado_inicial, out = create_fst(word_list)

# Desenhando os automatos
#dot = fst_to_graphviz(estado_inicial)
#dot.render('output/fst_graph_semana', view=True)

# Testando o autocomplete manualmente
#completions = autocomplete(estado_inicial, 'ja')
#print(completions)

# print(levenshein.autocomplete_with_levenshtein(estado_inicial, 'ja', 2))

# Printando os estados
#def print_final(estado_inicial):
#    for estado, ch, _ in estado_inicial.next:
#        if estado:
#            print(estado.is_end_of_word)
#            print_final(estado)

#print_final(estado_inicial)
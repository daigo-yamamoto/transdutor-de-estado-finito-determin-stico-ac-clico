import copy
from graphviz import Digraph
from queue import Queue


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
    final_state = None
    for element in list:
        p=[]
        if len(element.next) == len(state.next):
            for i in range(0, len(state.next)):
                if state.next[i] in element.next:
                    p.append(1)
            if len(p) == len(element.next):
                final_state = element
    return final_state


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

        while (i < len(currentWord)) and (i < len(previousWord)) and (previousWord[i - 1] == currentWord[i - 1]):
            i = i + 1

        prefixLengthPlus1 = i

        # we minimize the states from the suÆx of the previous word
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


def autocomplete(fst, prefix):
    # Encontra o estado correspondente ao final do prefixo
    def find_state_for_prefix(current_state, prefix):
        for char in prefix:
            next_state = None
            for trans in current_state.next:
                if trans[1] == char:  # Verifica se o caractere coincide com a transição
                    next_state = trans[0]
                    break
            if next_state is None:
                return None  # Retorna None se o prefixo não estiver no FST
            current_state = next_state
        return current_state

    # Realiza uma busca em profundidade para encontrar todas as palavras a partir deste estado
    def dfs(current_state, current_prefix, words):
        if current_state.is_end_of_word:
            words.append(current_prefix)
        for next_state, char, _ in current_state.next:
            if next_state is not None and char is not None:
                dfs(next_state, current_prefix + char, words)

    # Iniciar autocompletar
    starting_state = find_state_for_prefix(fst, prefix)
    if starting_state is None:
        return []  # Se o prefixo não existir, retorna uma lista vazia

    completions = []
    dfs(starting_state, prefix, completions)
    return completions


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
                label = f"{char}/{output}" if char and output else char or output or 'ε'
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
file_path = './dicionario/meses.txt'
word_list = read_words_from_file(file_path)

estado_inicial, out = create_fst(word_list)

# Desenhando os automatos
#dot = fst_to_graphviz(estado_inicial)
#dot.render('output/fst_graph', view=True)

# Testando o autocomplete manualmente
completions = autocomplete(estado_inicial, 'ja')
print(completions)

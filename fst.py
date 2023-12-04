class FstNode:
    def __init__(self):
        self.next = []  # Lista de tuplas (prox estado, char, '')
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

def set_final(state):
    state.next = None
    state.output = None
    state.is_end_of_word = True

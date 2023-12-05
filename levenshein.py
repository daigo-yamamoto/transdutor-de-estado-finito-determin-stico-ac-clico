class LevenshteinAutomaton:
    def __init__(self, string, n):
        self.string = string
        self.max_edits = n

    def start(self):
        return range(len(self.string)+1)

    def step(self, state, c):
        new_state = [state[0]+1]
        for i in range(len(state)-1):
            cost = 0 if self.string[i] == c else 1
            new_state.append(min(new_state[i]+1, state[i]+cost, state[i+1]+1))
        return [min(x,self.max_edits+1) for x in new_state]

    def is_match(self, state):
        return state[-1] <= self.max_edits

    def can_match(self, state):
        return min(state) <= self.max_edits

    def transitions(self, state):
        return set(c for (i,c) in enumerate(self.string) if state[i] <= self.max_edits)

def autocomplete_with_levenshtein(root, prefix, max_distance):
    levenshtein_automaton = LevenshteinAutomaton(prefix, max_distance)

    def dfs_with_levenshtein(node, current_word, state_levenshtein, complete_words):
        if node.is_end_of_word and levenshtein_automaton.is_match(state_levenshtein):
            complete_words.append(current_word)

        for next_node, char, _ in node.next:
            if next_node is None or char is None:
                continue

            # Calcula a nova distância de Levenshtein considerando apenas as transições existentes no FST
            new_state_levenshtein = levenshtein_automaton.step(state_levenshtein, char)
            if levenshtein_automaton.can_match(new_state_levenshtein):
                dfs_with_levenshtein(next_node, current_word + char, new_state_levenshtein, complete_words)

    complete_words = []
    initial_state_levenshtein = levenshtein_automaton.start()
    dfs_with_levenshtein(root, "", initial_state_levenshtein, complete_words)
    return complete_words

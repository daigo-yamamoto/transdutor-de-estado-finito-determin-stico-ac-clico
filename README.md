# Transdutor de estado finito determinístico acíclico
## Introdução

Este projeto visa desenvolver um sistema avançado de autocompletar que integra duas estruturas de dados poderosas e eficientes para o processamento de texto: Trie (Árvore de Prefixos) e FST (Transdutor de Estado Finito Determinístico Acíclico). O objetivo é criar uma ferramenta de autocompletar que não apenas prevê as palavras enquanto os usuários digitam, mas que também oferece correções inteligentes.

A Trie, conhecida por sua eficiência na recuperação de palavras, é uma árvore de busca onde cada nó representa um caractere de uma palavra. Esta estrutura é particularmente eficiente para autocompletar, uma vez que permite armazenar e recuperar grandes conjuntos de palavras de forma rápida e com um consumo de memória relativamente baixo, proporcionando assim uma maneira eficiente de buscar e sugerir palavras a partir de prefixos inseridos pelo usuário.

Os Transdutores de Estado Finito Determinístico Acíclico (FST) são estruturas de dados extremamente versáteis e poderosas que são utilizadas no processamento de linguagem natural e em sistemas de informação para uma variedade de aplicações, incluindo análise morfológica, reconhecimento de padrões, e compressão de dados.

A eficácia do FST deriva de sua habilidade em mapear conjuntos de strings de entrada para conjuntos de strings de saída de forma eficiente. Aqui estão algumas das características principais que definem como um FST funciona:

- **Determinístico**: Cada estado no FST tem uma transição única para um determinado símbolo de entrada. Isso significa que o FST não tem ambiguidade no caminho a ser seguido quando processa uma string de entrada.
- **Acíclico**: Não existem ciclos no FST, ou seja, você não pode começar de um estado e seguir um caminho que o leve de volta ao mesmo estado. Isso garante que cada operação de processamento terminará após um número finito de passos.
- **Uso de Prefixos e Sufixos**: Embora os FSTs possam ser construídos para usar tanto prefixos quanto sufixos, a forma como eles são utilizados pode variar. FSTs podem ser otimizados para lidar com prefixos de forma que, ao começar a digitar uma palavra, o FST pode rapidamente sugerir conclusões para essa palavra. Da mesma maneira, eles podem ser adaptados para reconhecer sufixos, o que é útil para análises morfológicas e para gerar formas flexionadas de palavras.
- **Transdução**: FSTs realizam uma função de transdução, onde cada transição entre estados não apenas consome um símbolo de entrada, mas também pode gerar um símbolo de saída. Isso os torna particularmente úteis para tarefas como a conversão de texto em sua forma fonética ou a transformação de palavras em suas raízes lexicais.
- **Economia de Espaço**: Graças à sua natureza acíclica e determinística, os FSTs podem representar grandes vocabulários de forma compacta, já que compartilham estados comuns entre palavras com prefixos ou sufixos similares, reduzindo a redundância.

## Construção a partir de uma entrada ordenada
Uma trie é um dicionário com um grafo de transição que é uma árvore com o estado raiz e todos os estados finais. Na figura abaixo, podemos observar a diferença entre a trie e o FST.

IMAGEM

Tradicionalmente, para obtermos um dicionário mínimo, primeiro criamos um dicionário para a linguagem, não necessariamente mínimo, e então minimizamos com um algoritmo. Como vamos realizar a implementação da trie, vamos utilizar a trie como sendo a primeira etapa da criação da FST. Note que embora os algoritmos que minimizam as tries sejam eficientes no uso de memória, infelizmente eles têm um desempenho ruim em tempo de execução. Neste projeto vamos apresentar uma maneira de reduzir esses requisitos intermediários de memória e diminuir o tempo total de construção ao construir o dicionário intermediário palavra por palavra, mantendo um invariante de minimalidade, evitando assim ter uma trie na memória.

A parte central dos algoritmos de minimização de autômatos é a classificação de estados. Os estados de um dicionário são divididos em classes de equivalência das quais os estados representativos são os estados do dicionário mínimo. Assumindo que o dicionário original não tem estados inúteis, podemos deduzir que cada estado no dicionário mínimo deve ter uma linguagem à direita única. Como esta é uma condição necessária e suficiente para a minimidade, podemos usar igualdade de linguagem à direita como nossa relação de equivalência para nossas classes.

Vamos realizar a minimização do trie usando o algoritmo de Hopcroft e Ullman e Watson. Para o primeiro passo, pares de esados onde um é final e o outro não, podem ser imediatamente marcados como pertencendo a diferentes classes de equivalência. Pares de estados que têm um número diferente de transições de saída ou o mesmo número, mas com rótulos diferentes, também podem ser marcados como pertencendo a diferentes classes de equivalência. Finalmente, pares de estados que tem transições rotuladas com os mesmos símbolos, mas levando a estados diferentes que ja foram considerados, podem ser marcados como pertencendo a classes de equivalência diferentes.

Vamos percorrer a trie com o pós-ordem e ver como a partição pode ser realizada. Começamos com a folha, voltando pelo trie até o estado inicial. 





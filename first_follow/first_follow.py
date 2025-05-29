from grammar.grammar_reader import GrammarReader
     
"""
         start_symbol = None             
         nonterminals = set()            
         terminals = set()                
         nonterminal_productions = dict()  #dictionary with a key and value which is array of arrays.      
         terminal_productions = dict()   #dictionary with a key and value which is array of arrays.    
         
         
         
         nonterminal_productions={'E': [['T', 'E_prime']], 'E_prime': [['PLUS', 'T', 'E_prime'], ['eps']],
                                  'T': [['F', 'T_prime']], 'T_prime': [['STAR', 'F', 'T_prime'], ['eps']],
                                  'F': [['LEFT_PAR', 'E', 'RIGHT_PAR'], ['IDENTIFIER'], ['LITERAL']]},


         terminal_productions={'IDENTIFIER': '[a-zA-Z_][a-zA-Z0-9_]*', 'LITERAL': '\d+(\.\d+)?',
                                'PLUS': '\\+', 'STAR': '\\*', 'LEFT_PAR': '\\(', 'RIGHT_PAR': '\\)' }

"""


# we recursively compute the first for each nonterminal symbol.however as a basecase we have assigned the first of each terminal to itself:
def first_computation(grammar):
    # making the dictionary:
    first = {}
    for nonterm in grammar.nonterminals:   # for each nonterminal we set FIRST[nonterm] to an an empty set
        first[nonterm] = set()

    for t in grammar.terminals:                # every terminal is first of itself
        first[t] = {t}
    first['eps'] = {'eps'}

    # avoiding infinite recursions
    visited = set()

    def first_of(symbol):
        if symbol in grammar.terminals or symbol == 'eps':           # Terminal or ε: base case
            return {symbol}

        if symbol in visited:        # avoiding cycles
            return first[symbol]
        visited.add(symbol)

        # Foreach production A → alpha
        for production in grammar.nonterminal_productions.get(symbol, []):
            for rhs in production:
                righthandside_first = first_of(rhs)
                # Add everything except eps
                first[symbol].update(righthandside_first - {'eps'})
                # If rhs cannot produce eps, we stop here:
                if 'eps' not in righthandside_first:
                    break
            else:
                # If we never broke, all rhs can produce eps → so eps is in FIRST(A)
                first[symbol].add('eps')

        return first[symbol]

    # start doing first method for each nonterminal
    for nonterm in grammar.nonterminals:
        visited.clear()
        first_of(nonterm)

    return first

# debugging:
grammar = GrammarReader.load("example/grammar.ll1")
print(first_computation(grammar))


def follow_computation(grammar, first):

    follow = {}
    for nonterminal in grammar.nonterminals:  # make an empty set for each nonterminal's follow
        follow[nonterminal] = set()

    follow[grammar.start_symbol].add('$')  # start symbol always has '$' in its follow

    changed = True
    while changed:  # keep doing this until no more changes happen
        changed = False

        for head, productions in grammar.nonterminal_productions.items():
            for production in productions:
                carry = follow[head].copy()  # what we carry over as we go backwards through the rule

                for symbol in reversed(production):  # go through the rule from right to left
                    if symbol in grammar.nonterminals:
                        before = len(follow[symbol])
                        follow[symbol].update(carry)  # pass down the carry to the symbol
                        after = len(follow[symbol])
                        if after > before:
                            changed = True

                        if 'eps' in first[symbol]:  # if symbol can be empty, add its first (without eps) to carry
                            carry.update(first[symbol] - {'eps'})
                        else:
                            carry = first[symbol].copy()  # otherwise, reset carry
                    else:
                        carry = {symbol}  # if it's a terminal, we just carry that terminal

    return follow



# to run this file we should do like this:
#                                           python -m first_follow.first_follow

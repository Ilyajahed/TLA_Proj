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
    first = dict()
    for nonterm in grammar.nonterminals:   # for each nonterminal we set FIRST[nonterm] to an an empty set
        first[nonterm] = set()

    for t in grammar.terminals:                # every terminal is first of itself
        first[t] = {t}
    first['eps'] = {'eps'}

    # avoiding infinite recursions (with this part of code at lines 41-43: ********)
    visited = set()

    def first_of(symbol):
        if symbol in grammar.terminals or symbol == 'eps':           # if it is eps or terminal it will stop in this if clause.
            return {symbol}

        if symbol in visited:        # avoiding cycles(********)
            return first[symbol]
        visited.add(symbol)

        # Foreach production A → alpha
        for production in grammar.nonterminal_productions.get(symbol, []):     #here we know that the symbol is nonterminal and we should lookfor its production rule.
            for rhs in production:
                righthandside_first = first_of(rhs)
                # Add everything except eps
                first[symbol].update(righthandside_first - {'eps'})
                
                if 'eps' not in righthandside_first:   # If rhs cannot produce eps, we should break from the loop because we have found the first and then on the outer loop
                    break                              # we will find the other first for the header symbol:
                                                       # (if the righthandside has eps then we should not break and we should go to see the next product after it)
                    
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
# print(first_computation(grammar))



def follow_computation(grammar, first):
    follow = dict()
    for nonterm in grammar.nonterminals:
        follow[nonterm] = set()
    follow[grammar.start_symbol].add('$')  # rule: FOLLOW(start) = {$}

    changed = True
    while changed:
        changed = False

        # 1. loop over all productions A → α
        for headersymbol, productions in grammar.nonterminal_productions.items():
            for production in productions:
                prod_len = len(production)
                # 2. loop through each symbol in RHS
                for i in range(prod_len):
                    symbol = production[i]
                    if symbol in grammar.nonterminals:
                        # check what's after symbol
                        after = production[i + 1:]  # symbols after current

                        if after:
                            # 3. take FIRST of what's after
                            first_of_after = set()
                            for next_sym in after:     # use a new name
                                first_of_after |= (first[next_sym] - {'eps'})      #time to add the first of the next symbol(in this step we ignore if it has eps or not.next line we will handle it.)
                                if 'eps' in first[next_sym]:   # if the first of the next symbol contains eps then we got to see the next symbol in the 'after' part.

                                                                #forexample see this:       E'-> [[+,T,E'], [eps]]   then we choose the T and then the after part is E' so we check First(E') and forexample it is {+,eps} then we will choose the + and then go to the next symbol in the first(E') if it contains eps then we ignore that subarray and go to the next      
                                    continue
                                else:      # if there is no eps then it will break and it won't see the else clause.
                                    break
                            else:
                                # all after symbols had eps
                                first_of_after.add('eps')

                            # 4. add FIRST(after) minus eps to FOLLOW(symbol)
                            before = len(follow[symbol])
                            follow[symbol] |= (first_of_after - {'eps'})

                            # 5. if FIRST(after) includes eps → add FOLLOW(header)
                            if 'eps' in first_of_after:
                                follow[symbol] |= follow[headersymbol]
                            if len(follow[symbol]) > before:
                                changed = True
                        else:
                            # 6. symbol is at the end → FOLLOW(A) added
                            before = len(follow[symbol])
                            follow[symbol] |= follow[headersymbol]
                            if len(follow[symbol]) > before:
                                changed = True
    return follow


# x =first_computation(grammar)
# print(follow_computation(grammar ,x ))




# to run this file we should do like this:
#                                           python -m first_follow.first_follow

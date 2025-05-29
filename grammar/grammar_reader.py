class Grammar:
    def __init__(self):
        self.start_symbol = None             
        self.nonterminals = set()            
        self.terminals = set()                
        self.nonterminal_productions = dict()   # for nonterminal_productions,like :  E -> T E_prime       
        self.terminal_productions = dict()      # for terminal_productions(token regex) rules like: IDENTIFIER -> [a-zA-Z_][a-zA-Z0-9_]*   

    def __repr__(self):            #to visually see in the console what is the values in our grammar object
        return (
            f"Grammar(\n"
            f"  start_symbol={self.start_symbol!r},\n"
            f"  nonterminals={self.nonterminals!r},\n"
            f"  terminals={self.terminals!r},\n"
            f"  nonterminal_productions={self.nonterminal_productions!r},\n"
            f"  terminal_productions={self.terminal_productions!r}\n"
            f")"
        )


class GrammarReader:
    @staticmethod
    def load(filepath: str):
        grammar = Grammar()              # we've made an object of grammar and we will fill it with the values in the given ll1 grammar input.
        with open(filepath, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):    #we ignore the comments 
                    continue

                if line.startswith("START ="):             # To store the start_symbol of the given grammar to the object grammar we have.
                    grammar.start_symbol = line.split('=')[1].strip()

                elif line.startswith("NON_TERMINALS ="):         # To store the nonterminals of the given grammar to the object grammar we have.
                    # NON_TERMINALS = E, E_prime, T, T_prime, F
                    title, value = line.split('=')
                    for x in value.strip().split(', '):
                        grammar.nonterminals.add(x.strip())
                    

                elif line.startswith("TERMINALS ="):         # To store the start_symbol of the given grammar to the object grammar we have:
                    # TERMINALS = IDENTIFIER, LITERAL, PLUS, STAR, LEFT_PAR, RIGHT_PAR
                    title , value = line.split('=')
                    for x in value.strip().split(', '):
                        grammar.terminals.add(x.strip())

                elif '->' in line:
                    head, body = line.split('->')
                    head = head.strip()
                    body = body.strip()

                    if head in grammar.nonterminals:             #check to see whether if it is nonterminal production

                        # Example: body = "PLUS T E_prime | eps"
                        alternatives = body.split('|')
                        for alt in alternatives:
                            symbols = alt.strip().split()
                            grammar.nonterminal_productions.setdefault(head, []).append(symbols)     # here the nonterminal_production is a dictionary made of a key and
                                                                                                     # value which is an array of arrays


                    else:             #if we reach this else clause so it is a terminal production rule.

                        # IDENTIFIER -> [a-zA-Z_][a-zA-Z0-9_]*
                        grammar.terminal_productions[head] = body

        return grammar



# for debugging:

# print(GrammarReader.load("Example/grammar.ll1"))
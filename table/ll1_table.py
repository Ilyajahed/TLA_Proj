def build_ll1_table(grammar, first, follow) -> dict:
    table = {}                                   # this will hold the ll1 parse table as a dictionary


    for A, productions in grammar.nonterminal_productions.items():
        for production in productions:

            
            if production == ['eps']:   # if the production is eps, use follow set
                for b in follow[A]:
                    table[(A, b)] = production  # map (A, b) to the epsilon production

            else:
                first_alpha = set()  # we stored the first set of the production

                # loop through the symbols in the production
                for symbol in production:
                    # add first of symbol excluding epsilon
                    first_alpha |= (first[symbol] - {'eps'})

                    # if this symbol does not derive epsilon we will stop it
                    if 'eps' not in first[symbol]:
                        break
                else:
                    # if all symbols derive epsilon, add epsilon to first_alpha
                    first_alpha.add('eps')

                # for each terminal in first_alpha (except epsilon), map it to the production
                for a in first_alpha - {'eps'}:
                    table[(A, a)] = production

                # if epsilon is in first_alpha, also add follow entries
                if 'eps' in first_alpha:
                    for b in follow[A]:
                        table[(A, b)] = production

    return table  # return the completed ll1 table

import os
import sys

# Add project root to sys.path so imports work no matter where this is run from
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from grammar.grammar_reader import GrammarReader
from first_follow.first_follow import first_computation, follow_computation


def build_ll1_table(grammar, first, follow):
    table = {}

    for header, productions in grammar.nonterminal_productions.items():
        for production in productions:
            if production == ['eps']:
                for terminal in follow[header]:
                    table[(header, terminal)] = production
            else:
                first_alpha = set()
                for symbol in production:
                    first_alpha |= (first[symbol] - {'eps'})
                    if 'eps' not in first[symbol]:
                        break
                else:
                    first_alpha.add('eps')

                for terminal in first_alpha - {'eps'}:
                    table[(header, terminal)] = production

                if 'eps' in first_alpha:
                    for terminal in follow[header]:
                        table[(header, terminal)] = production

    return table




grammar = GrammarReader.load("Example/grammar.ll1")

first = first_computation(grammar)
follow = follow_computation(grammar, first)
table = build_ll1_table(grammar, first, follow)
# print(follow)

# print()
# print()
print(table)




''' Generate randomized CFG sentences '''
from nltk.grammar import Nonterminal
from nltk import CFG as nltkCFG
import random
import re

class CFG(object):
    ''' a grammar from an input file '''

    def __init__(self, grammar):
        self.grammar = nltkCFG.fromstring(grammar)


    def get_sentence(self, start=None, depth=7):
        ''' follow the grammatical patterns to generate a random sentence '''
        if not self.grammar:
            return 'Please set a self.grammar file'

        start = start if start else self.grammar.start()

        if isinstance(start, Nonterminal):
            productions = self.grammar.productions(start)
            if not depth:
                # time to break the cycle
                terminals = [p for p in productions \
                             if not isinstance(start, Nonterminal)]
                if len(terminals):
                    production = terminals
            production = random.choice(productions)

            sentence = []
            for piece in production.rhs():
                sentence += self.get_sentence(start=piece, depth=depth-1)
            return sentence
        else:
            return [start]


    def format_sentence(self, sentence):
        ''' fix display formatting of a sentence array '''
        for index, word in enumerate(sentence):
            if word == 'a' and index + 1 < len(sentence) and \
                    re.match(r'^[aeiou]', sentence[index + 1]) and not \
                    re.match(r'^uni', sentence[index + 1]):
                sentence[index] = 'an'
        text = ' '.join(sentence)
        text = '%s%s' % (text[0].upper(), text[1:])
        text = text.replace(' ,', ',')
        return '%s.' % text

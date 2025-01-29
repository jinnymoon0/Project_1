#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 15:52:47 2024

@author: jinnymoon
"""
def sample_file_write(filename):
    """A function that demonstrates how to write a
       Python dictionary to an easily-readable file.
    """
    d = {'test': 1, 'foo': 42}
    f = open(filename, 'w')
    f.write(str(d))
    f.close()
    
def sample_file_read(filename):
    """A function that demonstrates how to read a
       Python dictionary from a file.
    """
    file = open(filename, 'r')
    string = file.read()
    file.close()

    d = dict(eval(string))

    print("Inside the newly-read dictionary, d, we have:")
    print(d)
    
class TextModel:
    def __init__(self, model_name):
        """constructs a new TextModel object by accepting a string model_name
            as a parameter and initializing name, words, and word_lengths
        """
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.prefixes = {}   
        
    def __repr__(self):
        """ return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of prefixes: ' + str(len(self.prefixes))
        return s
    
    def add_string(self, s):
        """ adds a string of text s to the model by augmenting the feature 
            dictionaries defined in the constructor.
        """
        current_sentence_length = 0
        words = s.split()
        for word in words:
            last_char = word[-1:]
            if last_char in '.!?':
                current_sentence_length += 1
                if current_sentence_length in self.sentence_lengths:
                    self.sentence_lengths[current_sentence_length] += 1
                else:
                    self.sentence_lengths[current_sentence_length] = 1
                current_sentence_length = 0
            else:
                current_sentence_length += 1
        if current_sentence_length > 0:
            if current_sentence_length in self.sentence_lengths:
                self.sentence_lengths[current_sentence_length] += 1
            else:
                self.sentence_lengths[current_sentence_length] = 1
        words = clean_text(s)
        for word in words:
            if word in self.words:
                self.words[word] += 1
            else:
                self.words[word] = 1
            length = len(word)
            if length in self.word_lengths:
                self.word_lengths[length] += 1
            else:
                self.word_lengths[length] = 1
            word_stem = stem(word)
            if word_stem in self.stems:
                self.stems[word_stem] += 1
            else:
                self.stems[word_stem] = 1
            if len(word) >= 3:
                prefix = word[:3]
                if prefix in self.prefixes:
                    self.prefixes[prefix] += 1
                else:
                    self.prefixes[prefix] = 1
        
    def add_file(self, filename):
        """ adds all the text in the file identified by filename to the model.
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = ''
        for line in f:
            text += line
        f.close()
        self.add_string(text)

    def save_model(self):
        """ saves the TextModel object self by writing its various feature
            dictionaries to files.
        """
        # Save words 
        f = open(self.name + '_words', 'w')
        f.write(str(self.words))
        f.close()
        # Save word_lengths 
        f = open(self.name + '_word_lengths', 'w')
        f.write(str(self.word_lengths))
        f.close()
        # Save stems 
        f = open(self.name + '_stems', 'w')
        f.write(str(self.stems))
        f.close()
        # Save sentence_lengths 
        f = open(self.name + '_sentence_lengths', 'w')
        f.write(str(self.sentence_lengths))
        f.close()
        # Save prefixes 
        f = open(self.name + '_prefixes', 'w')
        f.write(str(self.prefixes))
        f.close()

    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object from
            their files and assigns them to the attributes to the called TextModel.
        """
        # read words
        file = open(self.name + '_words', 'r')
        string = file.read()
        file.close()
        self.words = eval(string)
        # read word_lengths
        file = open(self.name + '_word_lengths', 'r')
        string = file.read()
        file.close()
        self.word_lengths = eval(string)
        # read stems
        file = open(self.name + '_stems', 'r')
        string = file.read()
        file.close()
        self.stems = eval(string)
        # read sentence_lengths
        file = open(self.name + '_sentence_lengths', 'r')
        string = file.read()
        file.close()
        self.sentence_lengths = eval(string)
        # read prefixes
        file = open(self.name + '_prefixes', 'r')
        string = file.read()
        file.close()
        self.prefixes = eval(string)
        
    def similarity_scores(self, other):
        """ compute and return a list of log similarity scores measuring the
            similarity of self and other.
        """
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        prefixes_score = compare_dictionaries(other.prefixes, self.prefixes)
        return [word_score, word_lengths_score, stems_score, sentence_lengths_score, prefixes_score]

    def classify(self, source1, source2):
        """ compare TextModel object (self) to two other "source" TextModel
            objects (source1 and source 2) and determines which of these other
            TextModel is the more likely source called TextModel.
        """
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        print('scores for ' + source1.name + ':', [round(score, 3) for score in scores1])
        print('scores for ' + source2.name + ':', [round(score, 3) for score in scores2])
        source1_wins = 0
        source2_wins = 0
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                source1_wins += 1
            elif scores2[i] > scores1[i]:
                source2_wins += 1
        if source1_wins > source2_wins:
            print(self.name + ' is more likely to have come from ' + source1.name)
        elif source2_wins > source1_wins:
            print(self.name + ' is more likely to have come from ' + source2.name)
        else:
            weights = [10, 5, 7, 3, 1]
            for i in range(len(weights)):
                weighted_sum1 = sum(weights[i] * scores1[i])
                weighted_sum2 = sum(weights[i] * scores2[i])
            if weighted_sum1 > weighted_sum2:
                print(self.name + ' is more likely to have come from ' + source1.name)
            else:
                print(self.name + ' is more likely to have come from ' + source2.name)
                
def clean_text(txt):
    """ takes a string of text txt as a parameter and returns a list 
        containing the words in txt after it has been cleaned. This function
        will be used when processing each word in a text individually, without
        worrying about punctuation or special characters.
    """
    for symbol in """.,?"'!;:""":
        txt = txt.replace(symbol, ' ')
    return txt.lower().split()

def stem(s):
    """ accepts a string as a parameter, and retrun the stem of s. The stem of
        word is the root part of the word, which excludes any prefixes and 
        suffixes.
    """
    word = s.lower()
    n = len(word)
    if n >= 3:
        if word[n-3:] == 'ies':
            return word[:n-3] + 'i'
        elif word[n-3:] == 'ing':
            return word[:n-3] + 'e'
        elif word[n-1:] == 's':
            if word[n-2:] == 'es':
                return word[:n-2]
            if word[:3] == 'the':
                return word
            return word[:n-1]
        elif word[:3] == 'the':
            return word
        elif word[:3] == 'lov':
            return word[:3]
    return word

import math

def compare_dictionaries(d1, d2):
    """ take two feature dictionaries d1 and d2 as inputs, compute and return
        their log similarity score.
    """
    if d1 == {}:
        return - 50
    score = 0
    total = 0
    for x in d1:
        total += d1[x]
    for y in d2:
        if y in d1:
            x = d1[y] / total
        else:
            x = 0.5 / total
        score += math.log(x) * d2[y]
        
    return score

def test():
    """ Text TextModel implementation """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)

def run_tests():
    """ compare sources """
    source1 = TextModel('trump')
    source1.add_file('trump.txt')

    source2 = TextModel('harris')
    source2.add_file('harris.txt')

    new1 = TextModel('bush')
    new1.add_file('bush.txt')
    new1.classify(source1, source2)
    
    new2 = TextModel('mlk')
    new2.add_file('mlk.txt')
    new2.classify(source1, source2)
    
    new3 = TextModel('BBC')
    new3.add_file('BBC.txt')
    new3.classify(source1, source2)
    
    new4 = TextModel('CNN')
    new4.add_file('CNN.txt')
    new4.classify(source1, source2)
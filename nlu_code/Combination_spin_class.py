# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 11:47:08 2023

"""

import pandas as pd
import re
import random
from nltk import word_tokenize
from nltk.corpus import wordnet

class Spin_text:
    def __init__(self, input_file, output_file, random_seed=123):
        self.df = pd.read_csv(input_file)
        self.output_file = output_file
        self.random_seed = random_seed
        random.seed(self.random_seed)
        
    def paraphrase_sentence(self, sentence):
        tag_pattern = re.compile(r'\[E[12]\].*?\[/E[12]\]')
        tag_matches = re.findall(tag_pattern, sentence)
        tag_replacements = [f"TAG{i}" for i in range(len(tag_matches))]
        sentence_without_tags = re.sub(tag_pattern, lambda x: tag_replacements.pop(0), sentence)

        words = word_tokenize(sentence_without_tags)

        paraphrased_words = [self.get_synonyms(word) if random.choice([True, False]) else word for word in words]

        paraphrased_sentence = ' '.join(paraphrased_words)
        paraphrased_sentence = re.sub('TAG(\d+)', lambda x: tag_matches[int(x.group(1))], paraphrased_sentence)

        return sentence, paraphrased_sentence

    def get_synonyms(self, word):
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        if synonyms:
            return random.choice(synonyms)
        else:
            return word

    def process_and_save(self):
        self.df['Combination_spin_text'] = ''

        for index, row in self.df.iterrows():
            sentence = str(row['Combinations'])
            spin_text = self.paraphrase_sentence(sentence)
            self.df.at[index, 'Combination_spin_text'] = spin_text

        df_exploded = self.df.explode('Combination_spin_text').reset_index(drop=True)
        
        # Drop the 'index' column
        df_exploded = df_exploded.drop(columns=['index'], errors='ignore')

        df_exploded.to_csv(self.output_file, index=False)


#example
Obj1 = Spin_text(input_file='augmentation_cleaned_file1.csv', output_file='Combination_spin.csv')
Obj1.process_and_save()

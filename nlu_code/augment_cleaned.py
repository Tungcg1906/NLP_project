# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 18:18:07 2023


"""

import re
import warnings
warnings.filterwarnings(action="ignore")
import pandas as pd

class Augmentation:
    def __init__(self, cleaned_file):
        self.cleaned_data = pd.read_csv(cleaned_file)

    def get_cleaned_data(self):
        return self.cleaned_data

    def remove_null_values(self, cleaned_data):
        cleaned_data = cleaned_data.dropna(subset=['cleaned_text'])
        cleaned_data['cleaned_text'] = cleaned_data['cleaned_text'].astype(str)
        return cleaned_data

    def create_augmented_df(self, augmented_sentences):
        augment_df = pd.DataFrame({"Combinations": augmented_sentences})
        return augment_df

    def augmentation(self, augment_df):
        augment_exploded_df = augment_df.explode('Combinations').reset_index(drop=True)
        augment_exploded_df.columns = ['Combinations']
        augment_exploded_df['Combinations'] = augment_exploded_df['Combinations'].str.strip()
        return augment_exploded_df

    def result_data(self, cleaned_data, augment_exploded_df):
        final_augmented_df = pd.concat([cleaned_data, augment_exploded_df], axis=1)
        return final_augmented_df

    def texts_augment(self, sentence, relation):
        subj_pattern = r'\[E1\](.*?)\[/E1\]'
        obj_pattern = r'\[E2\](.*?)\[/E2\]'
        pattern_sentence_check = r'\[E1\].*\[/E2\]'
        subj = re.search(subj_pattern, sentence)
        obj = re.search(obj_pattern, sentence)
        tags = r"\[E1\](.*?)\[/E1\]|\[E2\](.*?)\[/E2\]"
        if subj and obj:
            subj = subj.group(1)
            obj = obj.group(1)

        if relation == "noRelation":
            relation = ""

        if re.search(pattern_sentence_check, sentence):
            output_string_E1 = re.sub(subj_pattern, f'[E1]{obj}[/E1]', sentence)
            output_string_E1 = re.sub(obj_pattern, f'[E2]{subj}[/E2]', output_string_E1)
            verb_E1 = r'\[/E1\](.*?)\[E2\]'
            text_verb = re.search(verb_E1, sentence)
            text_verb = text_verb.group(1) if text_verb else ""
            output_string_E1 = re.sub(verb_E1, f'[/E1] {relation[:-2]} [E2]', output_string_E1)
            combination_text = re.sub(tags, lambda x: f"[E2]{x.group(1)}[/E2]" if x.group(1) else f"[E1]{x.group(2)}[/E1]",
                                     output_string_E1)
            verb_string = re.sub(subj_pattern, f'{relation} [/E2]', sentence)
            out = re.sub(obj_pattern, f'[E1]{subj}[/E1]', verb_string)
            pattern_in_out = r'\[/E2](.*?)\[E1]'
            final_text_verb = re.sub(pattern_in_out, f'[E2]{obj}[/E2][E1]', out)

            if relation == "managerOf":
                sentences_list = [sentence, combination_text, final_text_verb]
                return sentences_list
            else:
                sentences_list = [sentence, combination_text]
                return sentences_list
        else:
            output_string_E2 = re.sub(subj_pattern, f'[E1]{obj}[/E1]', sentence)
            output_string_E2 = re.sub(obj_pattern, f'[E2]{subj}[/E2]', output_string_E2)
            verb_E2_pattern = r'\[/E2\](.*?)\[E1\]'
            text_verb = re.search(verb_E2_pattern, sentence)
            text_verb_E2 = text_verb.group(1) if text_verb else ""
            output_string_E2 = re.sub(verb_E2_pattern, f'[/E2]{relation[:-2]}[E1]', output_string_E2)
            combination_text_E2 = re.sub(tags,
                                         lambda x: f"[E2]{x.group(1)}[/E2]" if x.group(1) else f"[E1]{x.group(2)}[/E1]",
                                         output_string_E2)
            text_verb_pattern = re.search(verb_E2_pattern, sentence)
            text_verb_E2 = text_verb_pattern.group(1) if text_verb_pattern else ""
            output_verb = re.sub(obj_pattern, f'{relation}[/E2]', sentence)
            temp = re.sub(verb_E2_pattern, f'[E2]{subj}[/E2][E1]', output_verb)
            final_temp_string = re.sub(subj_pattern, f'[E1]{obj}[/E1]', temp)
            replaced_text_verb = re.sub(tags,
                                        lambda x: f"[E2]{x.group(1)}[/E2]" if x.group(1) else f"[E1]{x.group(2)}[/E1]",
                                        final_temp_string)
            if relation == "managerOf":
                sentences_list = [sentence, combination_text_E2, replaced_text_verb]
                return sentences_list
            else:
                sentences_list = [sentence, combination_text_E2]
                return sentences_list


clean_file = "cleaned_sentences.csv"
augment = Augmentation(clean_file)
reading_cleaned_file = augment.get_cleaned_data()

# Remove null values
cleaned_data = augment.remove_null_values(reading_cleaned_file)

# Reset index
cleaned_data = cleaned_data.reset_index()

# Create augmented sentences
augmented_sentences = cleaned_data.apply(lambda x: augment.texts_augment(x['cleaned_text'], x['relations']), axis=1)

# Create augmented DataFrame
augment_df = augment.create_augmented_df(augmented_sentences)

# Explode the DataFrame
final_augmented_df = augment.result_data(cleaned_data, augment_df)
final_augmented_df = final_augmented_df.explode('Combinations').reset_index(drop=True)


final_augmented_df.to_csv("augmentation_cleaned_file1.csv", index=False)

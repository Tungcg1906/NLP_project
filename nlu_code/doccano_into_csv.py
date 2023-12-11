import json
import pandas as pd
import numpy as np
import os
from os import listdir
import zipfile
import re

# Get jsonl files form directory
def get_jsonl(directory):
    path = []
    for filename in os.listdir(directory):
            if filename.endswith(".jsonl"):
                path.append(os.path.join(directory, filename))
    return path

# Create dictionary for relations
def Dataframe(dir):
    sentences, sentences_labels, subject, object, relations, labels, filenames = [],[],[],[],[],[],[]
    jsonl_files = get_jsonl(dir)
    for file in jsonl_files:
    # Tranform jsonl into json
        with open(file, 'r', encoding='utf8') as json_file:
            json_list = list(json_file)
        # Transform json into dataframe
        for json_str in json_list:
            result = json.loads(json_str)
            entities = get_entities(result) 
            ent1, ent2, rela = get_relation(result, entities)
            for i in range(len(ent1)):
                subject.append(ent1[i][0])
                object.append(ent2[i][0])
                relations.append(rela[i])
                labels.append([ent1[i][2],ent2[i][2]])
                try:
                    # for windows
                    filenames.append(re.search(r'\\([^\\]+)\.jsonl$', file).group(1) + '.txt')
                except:
                    # for linux
                    name_of_file = os.path.basename(file).split('.jsonl')[0]
                    filenames.append(name_of_file + '.txt')

                if ent1[i][1][0] < ent2[i][1][0]:
                    sent =  result['text'][:ent1[i][1][0]] + "[E1]" + result['text'][ent1[i][1][0]:ent1[i][1][1]] + "[/E1]" + result['text'][ent1[i][1][1]:]
                    sent =  sent[:ent2[i][1][0]+9] + "[E2]" + sent[ent2[i][1][0]+9:ent2[i][1][1]+9] + "[/E2]" + sent[ent2[i][1][1]+9:]
                    sentences.append(sent)

                    sentence_labels =  result['text'][:ent1[i][1][0]] + "[" + ent1[i][2] + "]" + result['text'][ent1[i][1][0]:ent1[i][1][1]] + "[/" + ent1[i][2] + "]" + result['text'][ent1[i][1][1]:]
                    incr = len(ent1[i][2])*2 + 5
                    sentence_labels =  sentence_labels[:ent2[i][1][0]+incr] + "[" + ent2[i][2] + "]" + sentence_labels[ent2[i][1][0]+incr:ent2[i][1][1]+incr] + "[/" + ent2[i][2] + "]" + sentence_labels[ent2[i][1][1]+incr:]
                    sentences_labels.append(sentence_labels)
                elif ent1[i][1][0] > ent2[i][1][0]:
                    sent =  result['text'][:ent2[i][1][0]] + "[E2]" + result['text'][ent2[i][1][0]:ent2[i][1][1]] + "[/E2]" + result['text'][ent2[i][1][1]:]
                    sent =  sent[:ent1[i][1][0]+9] + "[E1]" + sent[ent1[i][1][0]+9:ent1[i][1][1]+9] + "[/E1]" + sent[ent1[i][1][1]+9:]
                    sentences.append(sent)

                    sentence_labels =  result['text'][:ent2[i][1][0]] + "[" + ent2[i][2] + "]" + result['text'][ent2[i][1][0]:ent2[i][1][1]] + "[/" + ent2[i][2] + "]" + result['text'][ent2[i][1][1]:]
                    sentence_labels =  sentence_labels[:ent1[i][1][0]+9] + "[" + ent1[i][2] + "]" + sentence_labels[ent1[i][1][0]+9:ent1[i][1][1]+9] + "[/" + ent1[i][2] + "]" + sentence_labels[ent1[i][1][1]+9:]
                    sentences_labels.append(sentence_labels)

    df = pd.DataFrame ({'sentences':sentences, 'sentences_labels':sentences_labels, 'Subject': subject, 'Object': object, 'relations':relations, 'labels':labels, 'filename':filenames})
    return df

# Get entities
def get_entities(sentence):
    ent = []
    for sent in sentence['entities']:
        ent.append([sent['id'], sentence['text'] [sent['start_offset']:sent['end_offset']], [sent['start_offset'],sent['end_offset']], sent['label']])
    return ent

# Get relationship between entities
def get_relation(sentence, ent):
    ent1, ent2, relation = [],[],[]
    for sent in sentence['relations']:
        relation.append(sent['type'])
        for i in ent:
            if i[0] == sent['from_id']:
                ent1.append([i[1],i[2],i[3]])
            elif i[0] == sent['to_id']:
                ent2.append([i[1],i[2],i[3]])
    return ent1, ent2, relation

# Relate relationships to ids
def Relations_Mapper(relations):
    rel2idx = {}
    idx2rel = {}

    sd_relations = {'employedBy': 2,
                    'managerOf': 0,
                    'locatedAt': 1,
                    'noRelation': 3
                    }

    # n_classes = 0
    for relation in relations:
            rel2idx[relation] = sd_relations[relation]

    for key, value in rel2idx.items():
        idx2rel[value] = key

    return rel2idx, idx2rel

def add_ids(df):
    df['relations_id']= df['relations'].map(Relations_Mapper(df['relations'])[0])
    relations = Relations_Mapper(df['relations'])[1]
    return df

def train_test_split (df):
    test = df.sample(frac=0.2, random_state=42)
    train = df.drop(test.index)
    return train, test


if __name__ == '__main__':
    # Get the path where the json file directory has been created from doccano 
    path= os.path.join(os.getcwd(), 'jsonl_files')

    # Create Dataframe 
    df = Dataframe(path)
    df = add_ids(df)
    # Split the dataframe into train and test
    test_df = df.sample(frac=0.2)
    train_df = df.drop(test_df.index)

    # Convert train and test DataFrames into csv files and zip them 
    with zipfile.ZipFile('train_test.zip', 'w') as csv_zip:
        csv_zip.writestr("train.csv", train_df.to_csv(index=False))
        csv_zip.writestr("test.csv", test_df.to_csv(index=False))
    
    np.save('idx2rel.npy', Relations_Mapper(df['relations'])[1])
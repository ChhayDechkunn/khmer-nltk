from typing import List
from tqdm import tqdm

from khmernltk.utils.constants import *
from khmernltk.utils.data import *

def word_to_features(sent, i):
    word = sent[i]
    kccs = seg_kcc(word)

    features = {
        'bias': 1.0,
        'len(kccs)':len(kccs),        
        'word.isdigit()': word.isdigit(),
        'word':word
    }
    
    for k in range(len(kccs)):
        features.update({f"{kccs[k]}":kccs[k]})
    
    if i > 0:
        word1 = sent[i-1]
        kccs1 = seg_kcc(word1)
        features.update({
            '-1:word.isdigit()': word1.isdigit(),
            '-1:word': word1,
            '-1len(kccs)':len(kccs),  
        })
        for k in range(len(kccs1)):
            features.update({f"-1kccs1[{k}]":kccs1[k]})
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1]
        kccs1 = seg_kcc(word1)
        features.update({
            '+1:word.isdigit()': word1.isdigit(),  
            '+1:word': word1,
            '+1len(kccs)':len(kccs),
        })
        for k in range(len(kccs1)):
            features.update({f"+1kccs1[{k}]":kccs1[k]})
    else:
        features['EOS'] = True

    return features

def create_word_features(sent):
    return [word_to_features(sent, i) for i in range(len(sent))]
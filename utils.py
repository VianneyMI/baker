"""Notebook utilities"""

import spacy
import numpy as np

spacy_motor = spacy.load('en_core_web_sm')

def count_token(text):
    
    output  = np.nan
    try:
        doc = spacy_motor(text)
        output =  len(doc)
    except Exception as e:
        print(e)
        

    return output
    
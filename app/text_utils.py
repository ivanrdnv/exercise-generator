import pandas as pd
import numpy as np
import spacy
from sentence_splitter import SentenceSplitter
import random
from pyinflect import getAllInflections

nlp = spacy.load('en_core_web_sm')

# Ogden's Basic English Word List (850)
ogden_basic_english = pd.read_csv('ogden_basic_english.csv')['0'].values.tolist()

def text_to_sentences(text):
    """
    Transforms the provided text into a pandas DataFrame containing sentences.
    Parameters: text (str). Returns: pandas.DataFrame.
    """
    splitter = SentenceSplitter(language='en')
    sentences = splitter.split(text)
    df = pd.DataFrame(sentences, columns=['raw'])
    return df

def select_word(sentence):
    """
    Selects a word from a given sentence and returns a list of possible inflected forms.
    Args: sentence (str). Returns: a list of inflected word forms. 
    """
    doc = nlp(sentence)
    candidate_tokens = [token for token in doc if not token.is_punct and not token.is_space
                            and token.is_lower and token.tag_.startswith(('V', 'N'))] # , 'A'
    if not candidate_tokens:
        return np.nan, np.nan
    
    selected_word = random.choice(candidate_tokens)
    inflections = getAllInflections(selected_word.lemma_, pos_type=selected_word.tag_[0])

    unique_values = [selected_word.lower_]

    # add the plural form for checking user's knowledge of noun pluralization
    if selected_word.pos_.startswith('N'):
        s_form = selected_word.lemma_ + 's'
        if s_form not in unique_values:
            unique_values.append(s_form)

    for forms in inflections.values():
        for form in forms:
            if form not in unique_values:
                unique_values.append(form)

    while len(unique_values) > 4:
        unique_values.pop()

    random.shuffle(unique_values)
    return selected_word, unique_values

def missing_word(sentence):
    """
    Selects a word from a given sentence and returns it 
    """
    doc = nlp(sentence)
    candidate_tokens = [token for token in doc if not token.is_punct and not token.is_space
                            and token.is_lower and token.lemma_ in ogden_basic_english]
    if not candidate_tokens:
        return np.nan
    
    selected_word = random.choice(candidate_tokens)
    return selected_word
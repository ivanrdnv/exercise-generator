import pandas as pd
import numpy as np
import spacy
from sentence_splitter import SentenceSplitter
import random
from pyinflect import getAllInflections

exercise_percentage = 0.5
min_sentence_length = 5
max_sentence_length = 15

# word categories
categories = {
        "noun": ["NOUN", "PROPN"],
        "adjective": ["ADJ"],
        "verb": ["VERB"],
        "adverb": ["ADV"],
        "pronoun": ["PRON"]
    }

nlp = spacy.load('en_core_web_sm')

# Ogden's Basic English Word List (850)
# ogden_basic_english = pd.read_csv('ogden_basic_english.csv')['0'].values.tolist()

def text_to_dataframe(text):
    """
    Transforms the provided text into a pandas DataFrame containing sentences.
    Parameters: text (str). Returns: pandas.DataFrame.
    """
    splitter = SentenceSplitter(language='en')
    sentences = splitter.split(text)
    df = pd.DataFrame(sentences, columns=['raw'])
    df['exercise'] = df['raw'].apply(lambda sentence: random.choice(list(exercise_functions.keys()))
                                     if min_sentence_length < len(nlp(sentence)) < max_sentence_length 
                                     and random.random() < exercise_percentage else None)

    def update_row(row):
        exercise_type = row['exercise']
        sentence = row['raw']
        if exercise_type in exercise_functions:
            result = exercise_functions[exercise_type](sentence)
            if pd.isna(result):
                row['exercise'] = None
            else:
                correct_answer, options = result
                row['correct_answer'] = correct_answer
                row['options'] = options
        return row

    df = df.apply(update_row, axis=1)

    return df



def select_word(sentence):
    """
    Selects a word from a given sentence and returns a list of possible inflected forms.
    Args: sentence (str). Returns: a list of inflected word forms. 
    """
    doc = nlp(sentence)
    candidate_tokens = [token for token in doc if not token.is_punct and not token.is_space
                            and not token.is_digit
                            and token.is_lower and token.tag_.startswith(('V', 'N'))] # , 'A'
    if not candidate_tokens:
        return np.nan
    
    selected_word = random.choice(candidate_tokens)
    inflections = getAllInflections(selected_word.lemma_, pos_type=selected_word.tag_[0])

    unique_values = ['______', selected_word.lower_]

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
    return selected_word.text, unique_values

# TODO: remake the functionality of this function
# def missing_word(sentence):
#     """
#     Selects a word from a given sentence and returns it 
#     """
#     doc = nlp(sentence)
#     candidate_tokens = [token for token in doc if not token.is_punct and not token.is_space
#                             and token.is_lower and token.lemma_ in ogden_basic_english]
#     if not candidate_tokens:
#         return np.nan
    
#     selected_word = random.choice(candidate_tokens)
#     return selected_word

def arrange_words(sentence):
    """
    Returns a list of shuffled words extracted from a sentence.
    """
    if not sentence:
        return np.nan
    doc = nlp(sentence)
    if len(doc) > 15:
        return np.nan
    tokens = [token.text for token in doc if not token.is_space and not token.is_punct]
    correct_sentence = ' '.join(tokens)
    random.seed(123)
    random.shuffle(tokens)
    
    # ! streamlit_sortables can't handle duplicates in a list
    processed_tokens = []
    for token in tokens:
        if token in processed_tokens:
            token += " "
        processed_tokens.append(token)
    return correct_sentence, processed_tokens

def word_category(sentence):
    """
    Randomly selects a word from a given sentence and returns the chosen word and its category.
    """
    doc = nlp(sentence)
    
    word_categories = {}
    for token in doc:
        for category, tags in categories.items():
            if token.pos_ in tags:
                if category not in word_categories:
                    word_categories[category] = []
                word_categories[category].append(token.text)
                
    if not word_categories:
        return np.nan
    
    category = random.choice(list(word_categories.keys()))
    chosen_word = random.choice(word_categories[category])
    
    return category, chosen_word

exercise_functions = {
    'select_word': select_word,
    'arrange_words': arrange_words,
    'word_category': word_category
}

import streamlit as st
import pandas as pd
from sentence_splitter import SentenceSplitter
import random
import text_utils 
from streamlit_sortables import sort_items
from annotated_text import annotated_text

options_pos = ["______", "verb", "noun", "adjective", "pronoun", "adverb"]

@st.cache_data
def process_text_file(text):
    df = text_utils.text_to_dataframe(text)
    return df
 
def main():
    st.title('Exercise Generator')

    st.header('Upload Text File')
    text_file = st.file_uploader('Choose a text file', type=['txt'])
    # TODO: 1. rewrite the logic 
    # TODO: 2. add the improved function missing_word
    if text_file is not None:
        text = text_file.read().decode('utf-8')
        df = process_text_file(text)

        for index, row in df.iterrows():
            exercise_type = row['exercise']
            sentence = row['raw']

            if exercise_type is None:
                st.write(sentence)

            elif exercise_type == 'select_word':
                selected_word = row['correct_answer']
                options = row['options']

                col_sentence, col_word = st.columns([3, 1])
                sentence = sentence.replace(selected_word, '**{}**')

                with col_word:
                    user_answer = None
                    user_answer = st.selectbox("Select the missing word:", options, index=options.index('______'), key=index)

                with col_sentence:
                    st.write(sentence.format(user_answer))

                    if user_answer == '______':
                        pass
                    else:
                        if user_answer == selected_word:
                            st.success("Correct!")
                        else:
                            st.error("Incorrect!")

            elif exercise_type == 'arrange_words':
                correct_answer = row['correct_answer']
                words = row['options']

                st.caption('Put words in the correct order:')
                user_answer = sort_items(words)
                user_answer = ' '.join(word.strip() for word in user_answer)

                
                if  user_answer== correct_answer:
                        st.success("Correct!")
               

            elif exercise_type == 'word_category':
                chosen_word = row['options']
                correct_category = row['correct_answer']
                sentence = sentence.split(chosen_word)

                col_sentence_pos, col_word_pos = st.columns([3, 1])
                with col_word_pos:
                    user_category = st.selectbox("Select the category of the word:", options_pos, index=0, key=index)
                with col_sentence_pos:
                    annotated_text(sentence[0], (chosen_word, user_category), sentence[1])
                    if user_category == '______':
                        pass
                    else:
                        if user_category == correct_category:
                            st.success("Correct!")
                        else:
                            st.error("Incorrect!")

                

if __name__ == "__main__":
    main()




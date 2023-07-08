import streamlit as st
import pandas as pd
import numpy as np
 
st.header('Exercise Generator for English')

data = st.file_uploader("Upload your text", type=["txt"])
if data is not None:
    text = data.getvalue().decode('utf-8')
    df = text_to_sentences(text)

    df_filtered = df[df['raw'].apply(lambda x: len(x.split()) > 5)]   
    df_filtered['select_word'] = df_filtered['raw'].apply(select_word)
    st.dataframe(df_filtered.head(15))
    #st.text(text)
    



st.subheader('Select the correct options for the missing words:')

sentence = "Once upon a time there {} a sweet little girl."
options = ['was', 'were', 'be', 'is', 'select']

missing_word = st.selectbox("Select the missing word:", options)
exercise_sentence = sentence.format(missing_word)

st.write(exercise_sentence)

import streamlit as st
import spacy
from spacy import displacy

def text_function(texto):
    nlp=spacy.load("output/model-last/")
    doc=nlp(texto)
    colors = {"Estado" : "#5F9EA0", "Terapêutica" : "#00FF00","RAM" : "#FFA07A","MCDT" : "#FF00FF", "Dose" : "#696969", "Posologia" : "#E6E6FA"}
    options = {"colors" : colors}
    return displacy.render(doc,style="ent",jupyter="True", options = options)

def main():
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    st.title('Text Analysis using Spacy Textblob')
    st.markdown('Type a sentence in the below text box and choose the desired option in the adjacent menu.')
    texto = st.text_input("Enter the sentence")

    if st.button("teste"):
        st.write(text_function(texto))
if __name__ == "__main__":
    main()

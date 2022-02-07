import streamlit as st
import spacy
from spacy import displacy

def text_function(texto):
    nlp = spacy.load("output/model-last/")
    doc = nlp(texto)
    colors = {"Estado" : "#5F9EA0", "Terapêutica" : "#00FF00","RAM" : "#FFA07A","MCDT" : "#FF00FF", "Dose" : "#696969", "Posologia" : "#E6E6FA"}
    options = {"colors" : colors}
    html = displacy.render(doc,style = "ent", jupyter = False,options = options)
    st.markdown(html, unsafe_allow_html = True)

def main():
    st.set_page_config(layout = 'wide', initial_sidebar_state = 'expanded')
    st.title('NLP em consulta farmacêutica')
    texto = st.text_input("Insira aqui a nota")

    if st.button("Analisar"):
        return text_function(texto)
if __name__ == "__main__":
    main()

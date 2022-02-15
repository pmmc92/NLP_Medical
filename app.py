import streamlit as st
import pandas as pd
import plotly.express as pe
import spacy
import openpyxl
from spacy import displacy

def text_function(texto):
    nlp = spacy.load("output/model-last/")
    doc = nlp(texto)
    colors = {"Estado" : "#5F9EA0", "Terapêutica" : "#00FF00","RAM" : "#FFA07A","MCDT" : "#FF00FF", "Dose" : "#696969", "Posologia" : "#E6E6FA"}
    options = {"colors" : colors}
    html = displacy.render(doc,style = "ent", jupyter = False,options = options)
    st.markdown(html, unsafe_allow_html = True)

ent = []
labels = []
def processar(x):
    doc = nlp(x)
    for entity in doc.ents:
        ent.append(entity.text)
        labels.append(entity.label_)

def main():
    st.set_page_config(layout = 'wide', initial_sidebar_state = 'expanded')
    st.title('NLP em consulta farmacêutica')
    
    st.header("Utilizando um ficheiro")
    ficheiro = st.file_uploader("Faça Upload do ficheiro contendo as notas clínicas", type=["xls","xlsx"])
    if ficheiro is not None:
        file_data =  ficheiro.read()
        st.write("Ficheiro escolhido:", ficheiro.name)
        df=pd.read_excel(ficheiro)
        
    st.header("utilizando texto livre")
    texto = st.text_input("Insira aqui a nota")

    if st.button("Analisar"):
        return text_function(texto)
if __name__ == "__main__":
    main()

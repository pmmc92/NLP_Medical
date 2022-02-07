import streamlit as st
import spacy
from spacy import displacy

HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""

def text_function(texto):
    nlp=spacy.load("output/model-last/")
    doc=nlp(texto)
    colors = {"Estado" : "#5F9EA0", "Terapêutica" : "#00FF00","RAM" : "#FFA07A","MCDT" : "#FF00FF", "Dose" : "#696969", "Posologia" : "#E6E6FA"}
    options = {"colors" : colors}
    html = displacy.render(docx,style="ent")
	html = html.replace("\n\n","\n")
	st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)

def main():
    st.set_page_config(layout='wide', initial_sidebar_state='expanded')
    st.title('Text Analysis using Spacy Textblob')
    st.markdown('Type a sentence in the below text box and choose the desired option in the adjacent menu.')
    texto = st.text_input("Enter the sentence")

    if st.button("teste"):
        return text_function(texto)
if __name__ == "__main__":
    main()

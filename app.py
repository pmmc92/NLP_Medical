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
ID = []
def processar(x):
    nlp = spacy.load("output/model-last/")
    doc = nlp(x["Nota"])
    for entity in doc.ents:
        ID.append(x["ID"])
        ent.append(entity.text)
        labels.append(entity.label_)

def exportar(x):
    download_dataset = []
    if x == "RAM":
        download_dataset = RAMS
    elif x == "Estado do Doente":
        download_dataset = Estado
    else:
        download_dataset = Tx
    ficheiro_relatorio = download_dataset.to_excel("relatorio.xlsx")
    return ficheiro_relatorio

def main():
    st.set_page_config(layout = 'wide', initial_sidebar_state = 'expanded')
    st.title('NLP em consulta farmacêutica')
    
    st.header("Utilizando um ficheiro")
    ficheiro = st.file_uploader("Faça Upload do ficheiro contendo as notas clínicas", type=["xls","xlsx"])
    if ficheiro is not None:
        file_data =  ficheiro.read()
        st.write("Ficheiro escolhido:", ficheiro.name)
        df=pd.read_excel(ficheiro)
        
    st.header("Utilizando texto livre")
    texto = st.text_input("Insira aqui a nota")

    if st.button("Analisar"):
        if ficheiro is not None:
            st.header("Dashboard de análise")
            st.write("Foram analisados registos de **{}** doentes".format(df.ID.nunique()))
            for i in range(len(df.index)):
                processar(df.iloc[i,:])
            base = pd.DataFrame({"ID":ID,"Entidade":ent,"Classific":labels})
            RAMS=base.loc[base.Classific=="RAM"]
            fig1=pe.pie(RAMS, names=RAMS.Entidade, title = "Distribuição de RAMS", width = 400, height = 400, color_discrete_sequence=pe.colors.qualitative.Vivid)
            Tx=base.loc[base.Classific=="Terapêutica"]
            fig2=pe.pie(Tx, names=Tx.Entidade, title = "Distribuição de Terapêutica", width = 400, height = 400, color_discrete_sequence=pe.colors.qualitative.Vivid)
            Estado=base.loc[base.Classific=="Estado"]
            fig3=pe.pie(Tx, names=Estado.Entidade, title = "Distribuição de Estado Global", width = 400, height = 400, color_discrete_sequence=pe.colors.qualitative.Vivid)
            col1,col2,col3 = st.columns(3)
            with col1:
                st.write(fig1)
            with col2:
                st.write(fig2)
            with col3:
                st.write(fig3)
            
            st.dataframe(base)
            st.subheader("Exportar relatório de análise")
            formato = st.radio("O que pretender recolher?",("RAMS","Estado do doente","Terapêutica"))
            exportar(formato)

            st.download_button(label="Exportar",data=ficheiro_relatorio)

        else:
            return text_function(texto)
if __name__ == "__main__":
    main()

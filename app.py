
## Packages Used

import streamlit as st
import pandas as pd
import plotly.express as pe
import spacy
import openpyxl
from spacy import displacy
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import xlsxwriter

## Function for rendering plain text 

def text_function(texto):
    nlp = spacy.load("output/model-last/")
    doc = nlp(texto)
    colors = {"Estado" : "#5F9EA0", "Terapêutica" : "#00FF00","RAM" : "#FFA07A","MCDT" : "#FF00FF", "Dose" : "#696969", "Posologia" : "#E6E6FA"}
    options = {"colors" : colors}
    html = displacy.render(doc,style = "ent", jupyter = False,options = options)
    st.markdown(html, unsafe_allow_html = True)

## Performing NLP on excel and generating report DataFrame

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

## Converting report DataFrame to .xlsx

def to_excel(w):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    w.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

## App main Corpus

def main():
    st.set_page_config(page_title="Projecto AscléPHios", layout="wide")
    if 'formato' not in st.session_state:
        st.session_state['formato'] = 'RAMS'
    elif st.session_state["formato"] == "RAMS":
        st.session_state["formato"] = "RAMS"
    elif st.session_state["formato"] == "Terapêutica":
        st.session_state["formato"] = "Terapêutica"
    else:
        st.session_state["formato"] = "Estado"
    
    st.title('NLP em consulta farmacêutica')
    st.caption("Esta é uma ferramenta que permite a identificação de parâmetros e outcomes importantes em contexto de consulta farmacêutica, utilizando um modelo de Natural Language Processing (NLP)")
    
    st.header("Utilizando um ficheiro")
    ficheiro = st.file_uploader("Faça Upload do ficheiro contendo as notas clínicas. O ficheiro deve ter 2 colunas: ID (Número de identificação anonimizado) e Notas (Coluna contendo as notas recolhidas)", type=["xls","xlsx"])
    if ficheiro is not None:
        file_data =  ficheiro.read()
        df=pd.read_excel(ficheiro)
        df["ID"] = df["ID"].astype(int)
        df["Nota"] = df["Nota"].astype(str)

        
    st.header("Utilizando texto livre")
    texto = st.text_input("Insira aqui a nota")

    
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
        
        st.subheader("Exportar relatório de análise")
        formato = st.selectbox("O que quer recolher?",("RAMS","Estado","Terapêutica"),key = "formato")
        if formato == "RAMS":
            ficheiro_download = RAMS
        elif formato == "Estado":
            ficheiro_download = Estado
        else:
            ficheiro_download = Tx
        ficheiro_relatorio = to_excel(ficheiro_download)
        st.download_button(label="Exportar",data=ficheiro_relatorio, file_name="relatorio.xlsx")

    else:
        return text_function(texto)

if __name__ == "__main__":
    main()

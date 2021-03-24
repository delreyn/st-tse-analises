ufs = ["ac","al","am","ap","ba","ce","df","es","go","ma","mg","ms","mt","pa","pb","pe","pi","pr","rj","rn",
     "ro","rr","rs","sc","se","sp","to","zz"]
ufs = [uf.upper() for uf in ufs]
uf = "PB"
import numpy as np
import pandas as pd
import streamlit as st
#import matplotlib.pyplot as plt
import geojson as gs


import plotly.express as px

# dados2018 = pd.read_csv("https://raw.githubusercontent.com/gilvandrocesardemedeiros/DCA_UFRN_Data-Science/main/consulta_cand_2018/consulta_cand_2018_{}.csv".format(uf),
#                         sep = ";", encoding = "latin-1")
# partidosAC = dados2018.SG_PARTIDO.value_counts()
# subSet_eleitos_PartidoAC = dados2018.loc[dados2018["CD_SIT_TOT_TURNO"].isin([1,2,3]) ,["SG_PARTIDO","CD_SIT_TOT_TURNO"]]
# subSet_candidatosAC_social = dados2018.loc[dados2018["CD_SIT_TOT_TURNO"].isin([1,2,3]) ,["SG_UF","SG_PARTIDO","DS_COR_RACA","DS_CARGO","DS_OCUPACAO","DS_GENERO",
#                                                                                             "DS_GRAU_INSTRUCAO"]]
st.title('Analise das Eleições 2020')

h1 = st.header("Abaixo mostra as analises, use o menu ao lado para filtrar")

# eleitosAC = subSet_eleitos_PartidoAC.SG_PARTIDO.value_counts()                                                                                       
# fig = plt.barh(eleitosAC.index,eleitosAC.values)
# plt.ylabel("Partidos")
# plt.xlabel("Quantidade de eleitos")
# plt.title("Candidatos eleitos por partido UF AC")
# st.pyplot(plt)

ETINIAS = ['BRANCA','INDÍGENA','PARDA','PRETA','SEM INFORMAÇÃO']

ESCOLARIDADES = ['ANALFABETO', 'ENSINO FUNDAMENTAL COMPLETO',
       'ENSINO FUNDAMENTAL INCOMPLETO', 'ENSINO MÉDIO COMPLETO',
       'ENSINO MÉDIO INCOMPLETO', 'LÊ E ESCREVE', 'SUPERIOR COMPLETO',
       'SUPERIOR INCOMPLETO']

df = pd.read_csv('Para_plotar.csv')

st.sidebar.markdown('__Olá__')

#rb = st.selectbox("Escolha um grupo etinico",ETINIAS)

@st.cache
def carregarMapa():
    with open("uf.json", encoding='iso-8859-1') as data_file:                           
        geojsonUF = gs.load(data_file)
    return geojsonUF

@st.cache
def obterEscolaridades():
    return pd.read_csv('dados_instrucao.csv')

@st.cache
def obterDadosEtnia():
    return pd.read_csv('Para_plotar.csv')

@st.cache
def obterMapaEtinia(rb):
    fig = px.choropleth(obterDadosEtnia(), geojson=geojsonUF,
                        locations="SG_UF", featureidkey="properties.UF_05",
                        projection="mercator",color=rb
                       )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0.5,"t":0,"l":0,"b":0})
    return fig

@st.cache
def obterMapaEscolaridade(escolaridade):
    fig = px.choropleth(obterEscolaridades(), geojson=geojsonUF,
                        locations="SG_UF", featureidkey="properties.UF_05",
                        projection="mercator",color=escolaridade
                       )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0.5,"t":0,"l":0,"b":0})
    return fig



########################### RENDENDERIZA PAGINA ##############################

geojsonUF = carregarMapa()


rb = st.sidebar.selectbox("Selecione Grupo Etínico", ETINIAS)

escolaridade = st.sidebar.selectbox("Selecione Escolaridade", ESCOLARIDADES)

st.plotly_chart(obterMapaEtinia(rb))
st.plotly_chart(obterMapaEscolaridade(escolaridade))




st.write(df)

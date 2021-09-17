import streamlit as st
from joblib import load
import pandas as pd
from utils import Transformador

#Cor de fundo do listbox
st.markdown('<style>div[role="listbox"] ul{background-color: #eee1f79e};</style>', unsafe_allow_html=True)

def aprovado():
    
    col4, col5, col6 = st.beta_columns([1,4,1])
    col5.success('Crédito aprovado')
    col5.write('<h1 style="text-align: center;color: HotPink">AEEEEEEEEEEEEE!!!!</h1><br>', unsafe_allow_html = True)
    col5.write('<h3 style="text-align: center;"><span style="color: HotPink">Parabéns!</span> você tem crédito aprovado com a gente! Que legal né?</h3><br>', unsafe_allow_html = True)
    col5.image("img/eu-sou-rica.gif")
    col5.balloons()

def negado():
    st.error('Crédito negado')
    col4, col5, col6 = st.beta_columns([1,4,1])
    col5.write('<h1 style="text-align: center;">Poxa que pena </h1><br>', unsafe_allow_html = True)
    col5.image("img/cry.gif")
    

def validar_dados(dict_respostas):
	# Validando os dados de anos empregado, já que a pessoa não poder estar emprega e desemprega ao mesmo tempo. #ClienteDeSchrödinger
	if dict_respostas['Anos_empregado'] != 0 and dict_respostas['Anos_desempregado'] != 0:
		st.warning('Informações de anos empregado/desempregado incompativeis')
		return False
	return True

def avaliar_mau(dict_respostas):
	modelo = load('objetos/modelo.joblib')
	features = load('objetos/features.joblib')

	if dict_respostas['Anos_desempregado'] > 0:
		dict_respostas['Anos_empregado'] = dict_respostas['Anos_desempregado'] * -1 
	
	respostas = []
	for coluna in features:
		respostas.append(dict_respostas[coluna])

	df_novo_cliente = pd.DataFrame(data=[respostas], columns=features)

	mau = modelo.predict(df_novo_cliente)[0]

	return mau

	



st.image('img/TowerBankLog.png')
st.write('<h1 style="text-align: center;">Avaliação de Crédito</h1><br>', unsafe_allow_html = True)

my_expander_1 = st.beta_expander('Me conte mais sobre seu trabalho!')

my_expander_2 = st.beta_expander("Me Fale mais sobre você!")

my_expander_3 = st.beta_expander("Sua família não pode ficar de fora, né?")

dict_respostas = {}
lista_campos = load('objetos/lista_campos.joblib')

with my_expander_1:

	col1_form, col2_form = st.beta_columns(2)

	dict_respostas['Categoria_de_renda'] = col1_form.selectbox('Qual a sua categoria de renda ?', lista_campos['Categoria_de_renda'])

	dict_respostas['Ocupacao'] = col1_form.selectbox('Qual a sua Ocupação ?', lista_campos['Ocupacao'])

	dict_respostas['Tem_telefone_trabalho'] = 1 if col1_form.radio('Você possui um telefone do trabalho ?', ['Sim', 'Não']) == 'Sim' else 0

	dict_respostas['Rendimento_Anual'] = col2_form.slider('Qual o seu salário mensal ?', help='Olha que legal! Você pode mover a barra usando as setas do teclado', min_value=0, max_value=35000, step=500) * 12

	dict_respostas['Anos_empregado'] = col2_form.slider('Quantos anos você está empregado ?', help='Caso você não esteja trabalhando, deixe no zero.\nVocê pode mover a barra usando as setas do teclado', min_value=0, max_value=50, step=1)

	dict_respostas['Anos_desempregado'] = col2_form.slider('Quantos anos você está desempregado ?', help='Caso você não esteja desempregado, deixe no zero.\nVocê pode mover a barra usando as setas do teclado', min_value=0, max_value=50, step=1)

with my_expander_2:

    col3_form, col4_form = st.beta_columns(2)

    dict_respostas['Grau_Escolaridade'] = col3_form.selectbox('Qual o seu grau de escolaridade ?', lista_campos['Grau_Escolaridade'])

    dict_respostas['Estado_Civil'] = col3_form.selectbox('Qual o seu estado civil ?', lista_campos['Estado_Civil'])

    dict_respostas['Tem_Carro'] = 1 if col3_form.radio('Você possui um ou mais carros  ?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Tem_telefone_fixo'] = 1 if col4_form.radio('Possui um ou mais telefones fixos ?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Tem_email'] = 1 if col4_form.radio('Você possui algum email ?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Idade'] = col4_form.slider('Qual a sua idade ?', help='Prometo que não falarei pra ninguem viu?\nLembrando que você pode mover a barra usando as setas do teclado', min_value=0, max_value=100, step=1)

with my_expander_3:

    col4_form, col5_form = st.beta_columns(2)

    dict_respostas['Moradia'] = col4_form.selectbox('Qual o tipo de moradia ?', lista_campos['Moradia'])

    dict_respostas['Tem_Casa_Propria'] = 1 if col4_form.radio('Tem Casa Propria ?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Tamanho_Familia'] = col5_form.slider('Qual o tamanho da familia ?', help='Olha que legal! Você pode mover a barra usando as setas do teclado', min_value=1, max_value=20, step=1)

    dict_respostas['Qtd_Filhos'] = col5_form.slider('Quantos filhos ?', help='Olha que legal! Você pode mover a barra usando as setas do teclado', min_value=0, max_value=20, step=1)

col1, col2, col3 = st.beta_columns([1.3,1,1])
col4, col5, col6 = st.beta_columns([1,4,1])

if col2.button('Avaliar crédito') and validar_dados(dict_respostas):
	if avaliar_mau(dict_respostas):
		negado()
	else:
		aprovado()

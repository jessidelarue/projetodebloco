#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
from PIL import Image

def function():
    
    st.set_page_config(layout='wide')
    
    st.title('Dashboard do Projeto - Black Friday Sales')
    st.write('''O objetivo do projeto é entender o comportamento (valor) de compra do cliente em relação a vários produtos de diversas categorias, durante a Black Friday.
    O problema principal refere-se às características, tanto dos clientes quanto dos produtos, que influenciam no valor das compras dos clientes durante este período.
    Com isso, pretende-se mensurar o valor da compra de um cliente com base em um determinado conjunto de características.''')
    
    st.subheader('Dataset original')
    data = pd.read_csv('black_friday_sales.csv')
    df = pd.DataFrame(data)
    st.write(df)

    st.subheader('Entendendo as variáveis:')
    st.markdown('''
    - **User_ID:** ID do cliente
    - **Product_ID:** ID do produto
    - **Gender:** sexo do cliente (Feminino/Masculino)
    - **Age:** faixa etária do cliente
    - **Occupation:** ocupação do cliente
    - **City_Category:** categoria da cidade do cliente (A, B, C)
    - **Stay_In_Current_City_Years:** tempo, em anos, de permanência do cliente na cidade atual
    - **Marital_Status:** estado civil do cliente (0 - solteiro, 1 - casado)
    - **Product_Category_1:** categoria principal do produto
    - **Product_Category_2:** categoria secundária do produto
    - **Product_Category_3:** categoria terciária do produto
    - **Purchase:** valor da compra (variável alvo)''')

    st.title('Análise Exploratória dos dados')
    st.write('Iniciamos o projeto tratando os dados ausentes:')
    
    col1, col2 = st.columns(2)
    
    with col1:
        img = Image.open('ausentes.png')
        st.image(img, caption='Visualizando os dados ausentes')
    
    with col2:
        img = Image.open('ausentes_2.png')
        st.image(img, caption='Verificando se os dados ausentes foram tratados')

    st.write('Em seguida, foi analisada a variável alvo:')

    st.subheader('Gráfico de Distribuição da variável alvo - Purchase')
    img = Image.open('distribuicao.png')
    st.image(img, caption='Distribuição de Purchase')
    st.write('A média maior que a mediana indica uma assimetria à direita na curva representativa dos dados.')

    st.subheader('Boxplot da variável alvo - Purchase')
    img = Image.open('boxplot_alvo.png')
    st.image(img, caption='Boxplot de Purchase')

    img = Image.open('purchase_desc.png')
    st.image(img, caption='Descrição de Purchase')

    st.write('Os gráficos refletem que os dados seguem uma distribuição quase normal. Também podem ser observados alguns outliers em valores acima de, aproximadamente, 20.000, como representado no boxplot, justificando a assimetria da curva representativa dos dados.')
    st.write('O desvio padrão relativamente alto em relação à média sugere que os valores são dispersos, e a presença de outliers pode ser uma razão para essa dispersão. Os quartis também ajudam a entender como os valores estão distribuídos ao longo do intervalo de dados:')
    st.markdown('''
    - 25% das compras tem um valor igual ou inferior a $ 5.823,00;
    - 50% das compras tem um valor igual ou inferior a $ 8.047,00;
    - 75% das compras tem um valor igual ou inferior a $ 12.054,00''')
    st.write('A diferença entre o terceiro e o primeiro quartil (IQR) é de aproximadamente 6,231, um IQR relativamente grande também sugere uma dispersão considerável nos dados. A grande diferença entre o terceiro quartil (75%) e o valor máximo (max) reforça a existência de outliers no lado superior da distribuição, indicando observações com valores muito acima da média.')
    
    st.subheader('Analisando outliers das variáveis numéricas')
    img = Image.open('outliers.png')
    st.image(img, caption='Outliers')
    st.write('''Verificamos a existência de outliers nas colunas Product_Category_1 e Purchase, mas como a porcentagem de outliers 
    é baixa, então, como temos uma quantidade razoável de dados, optamos por deletar esses registros para que os mesmos não influenciem no estudo.''')
    
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    col5, col6 = st.columns(2)
    col7, col8 = st.columns(2)
    
    with col1:
        st.subheader('Gender x Purchase')
        img = Image.open('gender_purchase.png')
        st.image(img, caption='Gender x Purchase')
        st.write('Em média, homens gastam mais que mulheres na Black Friday.')

    with col2:
        st.subheader('Age x Purchase')
        img = Image.open('age_purchase.png')
        st.image(img, caption='Age x Purchase')
        st.write('Os maiores consumidores são homens na faixa etária de 26 a 35 anos. Os menores de idade são quem menos consomem na Black Friday.')

    with col3:
        st.subheader('Occupation x Purchase')
        img = Image.open('occ_purchase.png')
        st.image(img, caption='Occupation x Purchase')
        st.write('O total gasto em compras varia bastante em relação à profissão do cliente.')

    with col4:
        st.subheader('City_Category x Purchase')
        img = Image.open('city_purchase.png')
        st.image(img, caption='City_Category x Purchase')
        st.write('Clientes de cidades da categoria B são os que mais consomem no período da Black Friday. Isso pode ser influenciado por diversos fatores, como: tamanho da população, nível de renda, demografia, acesso a lojas, necessidades e preferências do consumidor, entre outros.')

    with col5:
        st.subheader('Stay_In_Current_City_Years x Purchase')
        img = Image.open('years_purchase.png')
        st.image(img, caption='Years in city x Purchase')
        st.write('Pessoas que vivem há mais de um ano na cidade compram e gastam menos durante a Black Friday. O maior consumo é de pessoas entre 1 e 2 anos na cidade.')

    with col6:
        st.subheader('Marital_Status x Purchase')
        img = Image.open('ms_purchase.png')
        st.image(img, caption='Marital Status x Purchase')
        st.write('Solteiros consomem mais na black friday do que os casados.')

    with col7:
        st.subheader('Product_Category_1 x Purchase')
        img = Image.open('categories_purchase_1.png')
        st.image(img, caption='Category_1 x Purchase')
        st.write('Os produtos com mais vendas são os produtos que tem a categoria 5 como categoria principal.')

    with col8:
        st.subheader('Product_Category_1 x Purchase')
        img = Image.open('categories_purchase_2.png')
        st.image(img, caption='Category_1 x Purchase')
        st.write('Já os produtos da Categoria 10 promovem compras com o maior valor médio total.')

    st.title('Pré-processamento dos dados')
    st.write('''Na fase de pré-processamento, foram removidas do dataframe as colunas User_ID e Product_ID, por serem variáveis apenas com fins de identificação do cliente e do produto.
    Também foi realizada a codificação das variáveis Gender, Age, City_Category e Stay_In_Current_City_Years, pois são variáveis que possuem dados no formato object e devem ser transformados em valores numéricos antes de serem usadas em um modelo de regressão linear.
    Já na coluna Stay_In_Current_City_Years, apenas substituímos a string "4+" pelo valor inteiro 4 e converteremos todos os dados da coluna para o formato int.
    Também removemos as colunas Product_Category_2 e Product_Category_3.''')
    st.write('O resultado final foi o dataframe abaixo:')
    new_data = pd.read_csv('/work/encoded_black_friday.csv')
    new_df = pd.DataFrame(new_data)
    st.write(new_df)

    st.subheader('Correlação entre as Variáveis')
    img = Image.open('heatmap.png')
    st.image(img, caption='Correlação entre as Variáveis')
    st.write('''O heatmap reflete que as variáveis possuem uma relação linear fraca. De forma geral, elas variam independentemente uma da outra. 
    Isso pode ocorrer devido ao fato de as variáveis independentes serem categóricas, mesmo sendo numéricas.
    Também pode haver uma relação não linear, ou a relação entre as variáveis pode ser complexa e não pode ser capturada por uma simples medida de correlação linear.
    A ausência de correlação forte entre as features aumenta a dificuldade de serem feitas previsões fortes.''')
    
    st.title('Regressão Linear - Resultados')
    st.write('Após a aplicação do modelo de Regressão Linear, estes foram alguns dos resultados:')
   
    col1, col2 = st.columns(2)
    
    with col1:
        img = Image.open('regressao.png')
        st.image(img, caption='Valores Reais x Previsões do modelo')
    
    with col2:
        img = Image.open('regplot.png')
        st.image(img, caption='Resultados do modelo')


    st.title('Regressão Linear - Métricas de Avaliação')
    st.write('Após a aplicação do modelo de Regressão Linear, foram calculadas as seguintes métricas de avaliação:')
    metrics_data = pd.read_csv('metrics.csv')
    metrics_df = pd.DataFrame(metrics_data)
    st.write(metrics_df)
    
    st.write('''Considerando essas métricas, um modelo ideal teria valores de MSE, RMSE e MAE próximos de zero, o que indicaria que as previsões do modelo são muito próximas dos valores reais.
    Porém, os resultados obtidos e as métricas calculadas sugerem que o modelo de regressão linear possui um desempenho razoável, porém com um erro considerável nas previsões em relação aos valores reais.
    Assim, chegamos à conclusão de que a regressão modelar pode não ser o melhor modelo a ser aplicado ao conjuntos de dados em questão para prever o valor da compra.
    É importante aplicar outros modelos mais complexos que consigam prever valores mais próximos dos reais e que atinjam métricas mais satisfatórias.''')

if __name__ == "__main__":
    function()


# <a style='text-decoration:none;line-height:16px;display:flex;color:#5B5B62;padding:10px;justify-content:end;' href='https://deepnote.com?utm_source=created-in-deepnote-cell&projectId=43b9c1cf-c283-413b-9f4d-02fa2982479a' target="_blank">
# <img alt='Created in deepnote.com' style='display:inline;max-height:16px;margin:0px;margin-right:7.5px;' src='data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iODBweCIgaGVpZ2h0PSI4MHB4IiB2aWV3Qm94PSIwIDAgODAgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDU0LjEgKDc2NDkwKSAtIGh0dHBzOi8vc2tldGNoYXBwLmNvbSAtLT4KICAgIDx0aXRsZT5Hcm91cCAzPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGcgaWQ9IkxhbmRpbmciIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJBcnRib2FyZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyMzUuMDAwMDAwLCAtNzkuMDAwMDAwKSI+CiAgICAgICAgICAgIDxnIGlkPSJHcm91cC0zIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMjM1LjAwMDAwMCwgNzkuMDAwMDAwKSI+CiAgICAgICAgICAgICAgICA8cG9seWdvbiBpZD0iUGF0aC0yMCIgZmlsbD0iIzAyNjVCNCIgcG9pbnRzPSIyLjM3NjIzNzYyIDgwIDM4LjA0NzY2NjcgODAgNTcuODIxNzgyMiA3My44MDU3NTkyIDU3LjgyMTc4MjIgMzIuNzU5MjczOSAzOS4xNDAyMjc4IDMxLjY4MzE2ODMiPjwvcG9seWdvbj4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0zNS4wMDc3MTgsODAgQzQyLjkwNjIwMDcsNzYuNDU0OTM1OCA0Ny41NjQ5MTY3LDcxLjU0MjI2NzEgNDguOTgzODY2LDY1LjI2MTk5MzkgQzUxLjExMjI4OTksNTUuODQxNTg0MiA0MS42NzcxNzk1LDQ5LjIxMjIyODQgMjUuNjIzOTg0Niw0OS4yMTIyMjg0IEMyNS40ODQ5Mjg5LDQ5LjEyNjg0NDggMjkuODI2MTI5Niw0My4yODM4MjQ4IDM4LjY0NzU4NjksMzEuNjgzMTY4MyBMNzIuODcxMjg3MSwzMi41NTQ0MjUgTDY1LjI4MDk3Myw2Ny42NzYzNDIxIEw1MS4xMTIyODk5LDc3LjM3NjE0NCBMMzUuMDA3NzE4LDgwIFoiIGlkPSJQYXRoLTIyIiBmaWxsPSIjMDAyODY4Ij48L3BhdGg+CiAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMCwzNy43MzA0NDA1IEwyNy4xMTQ1MzcsMC4yNTcxMTE0MzYgQzYyLjM3MTUxMjMsLTEuOTkwNzE3MDEgODAsMTAuNTAwMzkyNyA4MCwzNy43MzA0NDA1IEM4MCw2NC45NjA0ODgyIDY0Ljc3NjUwMzgsNzkuMDUwMzQxNCAzNC4zMjk1MTEzLDgwIEM0Ny4wNTUzNDg5LDc3LjU2NzA4MDggNTMuNDE4MjY3Nyw3MC4zMTM2MTAzIDUzLjQxODI2NzcsNTguMjM5NTg4NSBDNTMuNDE4MjY3Nyw0MC4xMjg1NTU3IDM2LjMwMzk1NDQsMzcuNzMwNDQwNSAyNS4yMjc0MTcsMzcuNzMwNDQwNSBDMTcuODQzMDU4NiwzNy43MzA0NDA1IDkuNDMzOTE5NjYsMzcuNzMwNDQwNSAwLDM3LjczMDQ0MDUgWiIgaWQ9IlBhdGgtMTkiIGZpbGw9IiMzNzkzRUYiPjwvcGF0aD4KICAgICAgICAgICAgPC9nPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+' > </img>
# Created in <span style='font-weight:600;margin-left:4px;'>Deepnote</span></a>

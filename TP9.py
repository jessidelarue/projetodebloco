#!/usr/bin/env python
# coding: utf-8

# # Importando os dados

# In[1]:


import pandas as pd

df = pd.read_csv('/work/black_friday_sales.csv')
df.head()


# ## Entendendo as variáveis
# 
# - **User_ID:** ID do cliente
# - **Product_ID:** ID do produto
# - **Gender:** sexo do cliente (Feminino/Masculino)
# - **Age:** faixa etária do cliente
# - **Occupation:** ocupação do cliente
# - **City_Category:** categoria da cidade do cliente (A, B, C)
# - **Stay_In_Current_City_Years:** tempo, em anos, de permanência do cliente na cidade atual
# - **Marital_Status:** estado civil do cliente (0 - solteiro, 1 - casado)
# - **Product_Category_1:** categoria principal do produto
# - **Product_Category_2:** categoria secundária do produto
# - **Product_Category_3:** categoria terciária do produto
# - **Purchase:** valor da compra (variável alvo)

# # Explorando os dados

# In[2]:


df.info()


# In[3]:


df.shape


# **Conclusão:** Verificamos que o dataset é formado por 550.068 registros e 12 colunas e contém dados nos tipos int, float e object. As variáveis *Product_Category_2* e *Product_Category_3* contém bastantes dados ausentes.

# ## Verificando se há registros duplicados

# In[4]:


df.duplicated().sum()


# **Conclusão:** não há valores duplicados no dataset.

# ## Tratando os valores ausentes
# 
# Verificamos que as colunas *Product_Category_2* e *Product_Category_3* tem muitos dados faltantes. Isso acontece porque a maioria dos produtos não pertencem a uma segunda ou terceira categoria. É preciso tratar esses dados ausentes.

# In[5]:


# Visualizando os valores únicos de cada categoria
unique_categories = [sorted(df['Product_Category_1'].unique()),
                     sorted(df['Product_Category_2'].unique()),
                     sorted(df['Product_Category_3'].unique())]

for i, category in enumerate(unique_categories):
    print(f'Valores únicos da Categoria {i+1}:')
    print(category)


# In[6]:


# Verificando se os campos com valores ausentes foram preenchidos
import matplotlib.pyplot as plt
import seaborn as sns

sns.heatmap(df.isnull(), cbar=False)
plt.title('Verificando valores ausentes')

plt.savefig('/work/ausentes.png', bbox_inches='tight')
plt.show()


# Como verificamos acima, não existe uma categoria "0", então, para tratar esses casos ausentes, preencheremos os valores "nan" com o valor "0", para representar a ausência de categoria.

# In[7]:


df['Product_Category_2'].fillna(0, inplace=True)
df['Product_Category_3'].fillna(0, inplace=True)


# In[8]:


# Verificando se os campos com valores ausentes foram preenchidos
import matplotlib.pyplot as plt
import seaborn as sns

sns.heatmap(df.isnull(), cbar=False)
plt.title('Verificando preenchimento de ausentes')

plt.savefig('/work/ausentes_2.png', bbox_inches='tight')
plt.show()


# ## Analisando a distribuição da variável alvo - Purchase

# In[9]:


import numpy as np

sns.histplot(data=df, x='Purchase')
plt.xlabel('Purchase')

# Incluindo as informações de média e mediana no gráfico
plt.axvline(np.mean(df['Purchase']), color='green')
plt.axvline(np.median(df['Purchase']), color='red')

plt.savefig('/work/distribuicao.png', bbox_inches='tight')
plt.show()


# **Conclusão:** A média maior que a mediana indica uma assimetria à direita na curva representativa dos dados.

# In[10]:


df['Purchase'].plot(kind = 'density')


# In[11]:


sns.boxplot(x = df['Purchase'])

plt.savefig('/work/boxplot_alvo.png', bbox_inches='tight')


# In[12]:


purchase_desc = df['Purchase'].describe()
purchase_desc


# In[13]:


plt.bar(purchase_desc.index, purchase_desc.values)
plt.title('Estatísticas Descritivas de Purchase')
plt.ylabel('Valores')
plt.xlabel('Estatísticas')
plt.xticks(rotation=45)  # Rotacionando os rótulos do eixo x se necessário

# Salvar como imagem
plt.savefig('/work/purchase_desc.png', bbox_inches='tight')
plt.show()


# **Conclusões:**
# 
# Os gráficos refletem que os dados seguem uma distribuição quase normal. Também podem ser observados alguns outliers em valores acima de, aproximadamente, 20.000, como representado no boxplot, justificando a assimetria da curva representativa dos dados.
# 
# O desvio padrão relativamente alto em relação à média sugere que os valores são dispersos, e a presença de outliers pode ser uma razão para essa dispersão. Os quartis também ajudam a entender como os valores estão distribuídos ao longo do intervalo de dados:
# 
# - 25% das compras tem um valor igual ou inferior a $ 5.823,00;
# - 50% das compras tem um valor igual ou inferior a $ 8.047,00;
# - 75% das compras tem um valor igual ou inferior a $ 12.054,00
# 
# A diferença entre o terceiro e o primeiro quartil (IQR) é de aproximadamente 6,231, um IQR relativamente grande também sugere uma dispersão considerável nos dados. A grande diferença entre o terceiro quartil (75%) e o valor máximo (max) reforça a existência de outliers no lado superior da distribuição, indicando observações com valores muito acima da média.

# ## Analisando outliers através de boxplots

# In[14]:


# Plotando o boxplot das variáveis numéricas
df.plot(kind = "box", figsize = (10, 4), subplots = True)
plt.tight_layout()
plt.savefig('/work/outliers.png', bbox_inches='tight')


# **Conclusão:** verificamos a existência de outliers nas colunas *Product_Category_1* e *Purchase*. Agora, verificaremos se a quantidade de outliers é significante para que possamos analisar a melhor forma de tratá-los. Os outliers na primeira coluna referem-se a valores superiores a, aproximadamente, 17.5. Já na coluna target, referem-se a valores superiores a, aproximadamente, 20.000.

# In[15]:


# Verificando outliers na coluna Product_Category_1
# Calculando a porcentagem de dados acima de 17,5
category_1_outliers_percent = df[df['Product_Category_1'] > 17.5].shape[0]/df.shape[0] * 100
print(f'Outliers de Product_Category_1: {category_1_outliers_percent:.2f}%')

# Verificando outliers na coluna Purchase
# Calculando a porcentagem de dados acima de 20000
purchase_outliers_percent = df[df['Purchase'] > 20000].shape[0]/df.shape[0] * 100
print(f'Outliers de Purchase: {purchase_outliers_percent:.2f}%')


# **Conclusão:** a porcentagem de outliers é baixa, então, como temos uma quantidade razoável de dados, optamos por deletar esses registros para que os mesmos não influenciem no estudo.

# In[16]:


# Deletando os registros com outliers
df = df.drop(df[(df['Product_Category_1']>17.5) | (df['Purchase']>20000)].index)


# In[17]:


# Visualizando os boxplots após a exclusão dos outliers
columns = ['Product_Category_1', 'Purchase']
df[columns].plot(kind = "box", subplots = True)
plt.tight_layout()


# ## Analisando a relação entre cada variável e a variável alvo
# 
# ### Gender x Purchase

# In[18]:


# Calculando a média de "Purchase" por gênero
gender_df = df.groupby('Gender')['Purchase'].mean().reset_index()

# Plotando o gráfico
ax = sns.barplot(x='Gender', y='Purchase', data=gender_df)
plt.title('Valor médio da compra por gênero')

plt.savefig('/work/gender_purchase.png', bbox_inches='tight')
plt.show()


# **Conclusão:** em média, homens gastam mais que mulheres na Black Friday

# ### Age x Purchase

# In[19]:


sns.countplot(x=df['Age'], hue=df['Gender'])
plt.title('Contagem de compras por faixa etária e gênero')

plt.savefig('/work/age_purchase.png', bbox_inches='tight')
plt.show()


# **Conclusão:** Os maiores consumidores são homens na faixa etária de 26 a 35 anos. Os menores de idade são quem menos consomem na Black Friday.

# ### Occupation x Purchase

# In[20]:


# Calculando o somatório de "Purchase" por profissão
occupation_df = df.groupby('Occupation')['Purchase'].sum().reset_index()

# Plotando o gráfico
ax = sns.barplot(x='Occupation', y='Purchase', data=occupation_df)
plt.title('Total gasto em compras por profissão do cliente')

plt.savefig('/work/occ_purchase.png', bbox_inches='tight')
plt.show()


# **Conclusão:** o total gasto em compras varia bastante em relação à profissão do cliente.

# ### City_Category x Purchase

# In[21]:


purchase_per_city = df.groupby('City_Category')['Purchase'].sum().reset_index()
sns.barplot(x='City_Category', y='Purchase', data=purchase_per_city)
plt.title('Total gasto em cada cidade')
plt.xticks(rotation=45)

plt.savefig('/work/city_purchase.png', bbox_inches='tight')
plt.show()


# **Conclusão:** clientes de cidades da categoria B são os que mais consomem no período da Black Friday. Isso pode ser influenciado por diversos fatores, como: tamanho da população, nível de renda, demografia, acesso a lojas, necessidades e preferências do consumidor, entre outros.

# ### Stay_In_Current_City_Years x Purchase

# In[22]:


# Calculando a soma das compras de acordo com o tempo na cidade
current_city = df.groupby('Stay_In_Current_City_Years')['Purchase'].sum()

sns.scatterplot(data=current_city)
plt.title('Valor total das compras pelo tempo na cidade')
plt.grid()

plt.savefig('/work/years_purchase.png', bbox_inches='tight')


# **Conclusão:** pessoas que vivem há mais de um ano na cidade compram e gastam menos durante a Black Friday. O maior consumo é de pessoas entre 1 e 2 anos na cidade.

# ### Marital_Status x Purchase

# In[23]:


# Fazendo a contagem de cada valor em "Marital_Status"
marital_status = df['Marital_Status'].value_counts()

plt.pie(marital_status, labels=['Not married', 'Married'], autopct='%1.1f%%')

plt.savefig('/work/ms_purchase.png', bbox_inches='tight')
plt.show()


# **Conclusão:** Solteiros consomem mais na black friday do que os casados 

# ### Product_Category_1 x Purchase

# In[24]:


sns.countplot(x=df['Product_Category_1'], data=df)
plt.title('Total de observações de cada categoria principal')

plt.savefig('/work/categories_purchase_1.png', bbox_inches='tight')
plt.show()


# In[25]:


purchase_per_category = df.groupby('Product_Category_1')['Purchase'].mean().reset_index()

sns.barplot(x='Product_Category_1', y='Purchase', data=purchase_per_category)
plt.title('Total gasto em cada categoria')
plt.xticks(rotation=45)

plt.savefig('/work/categories_purchase_2.png', bbox_inches='tight')
plt.show()


# **Conclusão:** os produtos com mais vendas são os produtos que tem a categoria 5 como categoria principal, porém, produtos da Categoria 10 promovem compras com o maior valor médio total.

# # Preparando os dados

# ## Excluindo colunas desnecessárias
# 
# Como as variáveis *User_ID* e *Product_ID* são variáveis apenas de identificação do cliente e do produto, respectivamente, optamos por não utilizá-las em nosso modelo, então as excluiremos do nosso conjunto de dados.

# In[26]:


clean_df = df.drop('User_ID', axis=1)
clean_df = clean_df.drop('Product_ID', axis=1)


# ## Codificando variáveis
# 
# As colunas *Gender*, *Age*, *City_Category* e *Stay_In_Current_City_Years* possuem dados no formato object e devem ser transformadas em valores numéricos antes de serem usadas em um modelo de regressão linear, ou seja, é necessária uma codificação para que o modelo possa interpretar essas categorias. Usaremos o método map() para substituir cada valor categórico por um valor correspondente nas três primeiras colunas.

# In[27]:


# Criando uma cópia do dataframe para não sobrescrever o dataframe limpo
encoded_df = clean_df.copy()

# Tratando a coluna 'Gender'
mapping_gender = {
                    'F': 0,
                    'M': 1
                 }
encoded_df['Gender'] = encoded_df['Gender'].map(mapping_gender)

# Tratando a coluna 'Age'
mapping_age = {
                    '0-17': 1,
                    '18-25': 2,
                    '26-35': 3,
                    '36-45': 4,
                    '46-50': 5,
                    '51-55': 6,
                    '55+': 7
                 }                 
encoded_df['Age'] = encoded_df['Age'].map(mapping_age)

# Tratando a coluna 'City_Category'
mapping_city_category = {
                            'A': 1,
                            'B': 2,
                            'C': 3
                        }
encoded_df['City_Category'] = encoded_df['City_Category'].map(mapping_city_category) 


# Na coluna *Stay_In_Current_City_Years*, apenas substituiremos a string "4+" pelo valor inteiro 4 e converteremos todos os dados da coluna para o formato int. 

# In[28]:


encoded_df['Stay_In_Current_City_Years'] = encoded_df['Stay_In_Current_City_Years'].replace('4+', 4).astype(int)


# In[29]:


# Visualizando o dataframe com as variáveis convertidas
encoded_df.head()


# In[30]:


encoded_df = encoded_df.drop('Product_Category_2', axis=1)
encoded_df = encoded_df.drop('Product_Category_3', axis=1)
encoded_df


# # Analisando a correlação entre os dados

# In[31]:


sns.heatmap(encoded_df.corr(), cmap = 'coolwarm', vmin=-1, vmax=1, annot=True)
plt.savefig('/work/heatmap.png', bbox_inches='tight')


# **Conclusão:** o heatmap reflete que não há uma relação linear muito forte entre as variáveis; de forma geral, elas variam independentemente uma da outra. Isso pode ocorrer devido ao fato de as variáveis independentes serem categóricas, mesmo sendo numéricas. Também pode haver uma relação não linear, ou a relação entre as variáveis pode ser complexa e não pode ser capturada por uma simples medida de correlação linear. Assim, analisaremos de forma individual a relação entre cada variável e a variável alvo Purchase. A ausência de correlação forte entre as features aumenta a dificuldade de serem feitas previsões fortes.

# ## Verificando a necessidade de normalizar os dados
# 
# Feita a codificação dos dados categóricos, precisamos analisar a necessidade de normalizá-los. Para isso, compararemos as estatísticas descritivas de cada variável antes e após a codificação.

# In[32]:


# Estatísticas descritivas antes da codificação
before_encoding = clean_df[['Gender', 'Age', 'City_Category', 'Stay_In_Current_City_Years']].describe(include='all')
print(before_encoding)


# **Conclusões:**
# 
# - **Gender:** possui duas categorias únicas ("M" e "F"), sendo "M" a categoria mais frequente;
# - **Age:** possui sete categorias únicas, sendo "26-35" a categoria mais frequente;
# - **City_Category:** possui três categorias únicas, sendo "B" a categoria mais frequente;
# - **Stay_In_Current_City_Years:** possui cinco categorias únicas, sendo "1" a categoria mais frequente.

# In[33]:


# Estatísticas descritivas depois da codificação
after_encoding = encoded_df[['Gender', 'Age', 'City_Category', 'Stay_In_Current_City_Years']].describe()
print(after_encoding)


# **Conclusões:**
# 
# - **Gender:** a média é aproximadamente 0.752, sugerindo que a categoria 1 ("M") é mais comum após a codificação. Os quartis indicam a distribuição dos dados, onde a maioria dos valores  é 1 ("M").
# - **Age:** a média de 3.489377 indica que os valores estão concentrados em torno de 3 (26-35). Os quartis indicam a distribuição dos dados, onde a maioria dos valores está entre 3 e 4 (18-25 e 26-35);
# - **City_Category:** a média de 2.038961 indica que os valores estão concentrados em torno de 2 (B). Os quartis indicam a distribuição dos dados, onde a maioria dos valores está entre 1 e 3, que são os valores possíveis após a codificação;
# - **Stay_In_Current_City_Years**: A média de 1.858892 indica que os valores estão concentrados em torno de 2 (3). Os quartis indicam a distribuição dos dados, onde a maioria dos valores está entre 1 e 3.
# 
# Não houve alterações nas estatísticas descritivas após a codificação. Além disso, as variáveis, com exceção da variável alvo, se encontram na mesma escala. Dessa forma, não é necessário fazer a normalização/escalonamento dos dados.

# In[34]:


encoded_df.to_csv('encoded_black_friday.csv', index=False)


# ## Separando os dados em grupos de treinamento e teste

# In[35]:


x = encoded_df.drop('Purchase', axis=1)
y = encoded_df['Purchase']


# In[36]:


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=42)


# # Aplicando o modelo de Regressão Linear

# In[37]:


from sklearn.linear_model import LinearRegression

# Criando uma instância do modelo
model = LinearRegression()

# Aplicando o modelo nos dados de treino
reg = model.fit(x_train, y_train)

# Fazendo as predições utilizando os dados de teste
y_pred = reg.predict(x_test)


# In[38]:


y_pred = np.round(y_pred,2)
result_df = pd.DataFrame({'Valor Real': y_test, 'Valor Previsto': y_pred})
result_df


# In[39]:


result_df = pd.DataFrame({'Valor Real': y_test[:25], 'Valor Previsto': y_pred[:25]})

result_df.plot(kind='bar', figsize=(8, 6))
plt.title('Valores Reais vs. Valores Previstos')
plt.xlabel('Amostras')
plt.ylabel('Valores')
plt.xticks(rotation=45) 
plt.legend()

plt.savefig('/work/regressao.png', bbox_inches='tight')

plt.show()


# In[40]:


sns.regplot(x = y_test, y = y_pred)
plt.savefig('/work/regplot.png', bbox_inches='tight')


# # Avaliando o modelo

# In[41]:


from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)

print(f'MSE: {mse:.2f}')
print(f'RMSE: {rmse:.2f}')
print(f'MAE: {mae:.2f}')


# In[42]:


metrics_df = pd.DataFrame({'Métricas': ['MSE', 'RMSE', 'MAE'],
                           'Valores': [mse, rmse, mae]})

metrics_df.to_csv('metrics.csv', index=False)


# Observamos um MSE alto, o que indica que o modelo está cometendo grandes erros quadráticos em suas previsões, o que não é desejável. O RMSE fornece uma medida do desvio padrão dos erros entre as previsões e os valores reais. O valor encontrado sugere que, em média, os erros têm uma amplitude considerável em relação aos valores reais, o que é bastante alto. O MAE é a média das diferenças absolutas entre as previsões e os valores reais. O valor encontrado para esta métrica indica que, em média, as previsões do modelo estão a aproximadamente 3288.45 unidades de distância dos valores reais.
# 
# Assim, as métricas de avaliação indicam que o modelo de regressão linear em questão tem um desempenho limitado na previsão dos dados. O modelo pode não estar capturando adequadamente os padrões nos dados ou pode ser necessário considerar outros modelos mais complexos ou features adicionais para melhorar a precisão das previsões.



# <a style='text-decoration:none;line-height:16px;display:flex;color:#5B5B62;padding:10px;justify-content:end;' href='https://deepnote.com?utm_source=created-in-deepnote-cell&projectId=43b9c1cf-c283-413b-9f4d-02fa2982479a' target="_blank">
# <img alt='Created in deepnote.com' style='display:inline;max-height:16px;margin:0px;margin-right:7.5px;' src='data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPHN2ZyB3aWR0aD0iODBweCIgaGVpZ2h0PSI4MHB4IiB2aWV3Qm94PSIwIDAgODAgODAiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB4bWxuczp4bGluaz0iaHR0cDovL3d3dy53My5vcmcvMTk5OS94bGluayI+CiAgICA8IS0tIEdlbmVyYXRvcjogU2tldGNoIDU0LjEgKDc2NDkwKSAtIGh0dHBzOi8vc2tldGNoYXBwLmNvbSAtLT4KICAgIDx0aXRsZT5Hcm91cCAzPC90aXRsZT4KICAgIDxkZXNjPkNyZWF0ZWQgd2l0aCBTa2V0Y2guPC9kZXNjPgogICAgPGcgaWQ9IkxhbmRpbmciIHN0cm9rZT0ibm9uZSIgc3Ryb2tlLXdpZHRoPSIxIiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPgogICAgICAgIDxnIGlkPSJBcnRib2FyZCIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTEyMzUuMDAwMDAwLCAtNzkuMDAwMDAwKSI+CiAgICAgICAgICAgIDxnIGlkPSJHcm91cC0zIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgxMjM1LjAwMDAwMCwgNzkuMDAwMDAwKSI+CiAgICAgICAgICAgICAgICA8cG9seWdvbiBpZD0iUGF0aC0yMCIgZmlsbD0iIzAyNjVCNCIgcG9pbnRzPSIyLjM3NjIzNzYyIDgwIDM4LjA0NzY2NjcgODAgNTcuODIxNzgyMiA3My44MDU3NTkyIDU3LjgyMTc4MjIgMzIuNzU5MjczOSAzOS4xNDAyMjc4IDMxLjY4MzE2ODMiPjwvcG9seWdvbj4KICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik0zNS4wMDc3MTgsODAgQzQyLjkwNjIwMDcsNzYuNDU0OTM1OCA0Ny41NjQ5MTY3LDcxLjU0MjI2NzEgNDguOTgzODY2LDY1LjI2MTk5MzkgQzUxLjExMjI4OTksNTUuODQxNTg0MiA0MS42NzcxNzk1LDQ5LjIxMjIyODQgMjUuNjIzOTg0Niw0OS4yMTIyMjg0IEMyNS40ODQ5Mjg5LDQ5LjEyNjg0NDggMjkuODI2MTI5Niw0My4yODM4MjQ4IDM4LjY0NzU4NjksMzEuNjgzMTY4MyBMNzIuODcxMjg3MSwzMi41NTQ0MjUgTDY1LjI4MDk3Myw2Ny42NzYzNDIxIEw1MS4xMTIyODk5LDc3LjM3NjE0NCBMMzUuMDA3NzE4LDgwIFoiIGlkPSJQYXRoLTIyIiBmaWxsPSIjMDAyODY4Ij48L3BhdGg+CiAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMCwzNy43MzA0NDA1IEwyNy4xMTQ1MzcsMC4yNTcxMTE0MzYgQzYyLjM3MTUxMjMsLTEuOTkwNzE3MDEgODAsMTAuNTAwMzkyNyA4MCwzNy43MzA0NDA1IEM4MCw2NC45NjA0ODgyIDY0Ljc3NjUwMzgsNzkuMDUwMzQxNCAzNC4zMjk1MTEzLDgwIEM0Ny4wNTUzNDg5LDc3LjU2NzA4MDggNTMuNDE4MjY3Nyw3MC4zMTM2MTAzIDUzLjQxODI2NzcsNTguMjM5NTg4NSBDNTMuNDE4MjY3Nyw0MC4xMjg1NTU3IDM2LjMwMzk1NDQsMzcuNzMwNDQwNSAyNS4yMjc0MTcsMzcuNzMwNDQwNSBDMTcuODQzMDU4NiwzNy43MzA0NDA1IDkuNDMzOTE5NjYsMzcuNzMwNDQwNSAwLDM3LjczMDQ0MDUgWiIgaWQ9IlBhdGgtMTkiIGZpbGw9IiMzNzkzRUYiPjwvcGF0aD4KICAgICAgICAgICAgPC9nPgogICAgICAgIDwvZz4KICAgIDwvZz4KPC9zdmc+' > </img>
# Created in <span style='font-weight:600;margin-left:4px;'>Deepnote</span></a>

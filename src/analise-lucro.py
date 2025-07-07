import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Aquisição de dados
df = pd.read_excel('report-consolidado.xlsx')

# 700 linhas, 13 colunas
df.shape  

df.head(100)
df.info()

# Padronização dos nomes das colunas
df.columns
colunas = [
    'segmento', 'pais', 'produto', 'qtd_unidades_vendidas',
    'preco_unitario', 'valor_total', 'desconto', 'valor_total_c/_desconto',
    'custo_total', 'lucro', 'data', 'mes', 'ano'
]
df.columns = colunas
df.columns

# Conversão de tipos: inteiros e decimais
df = df.astype({
    'qtd_unidades_vendidas': np.int64,
    'preco_unitario': np.float64
})

# Conversão de datas
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')

# Verificação de duplicatas e valores nulos
df.duplicated().sum()
df.isnull().sum()

# Ordenação por país, produto e data
df.sort_values(['pais', 'produto', 'data'], inplace=True)

# Estatísticas descritivas
df.describe().round(2)
df.describe(include=object)

# Lucro negativo (problemas)
df.sort_values(['lucro'])
df.sort_values(['lucro'], ascending=False)

# Análise de margem de lucro por segmento
colunas_lucro = ['valor_total_c/_desconto', 'custo_total', 'lucro']
df_segmento = df.groupby('segmento')[colunas_lucro].sum().round(2)
df_segmento['margem_lucro'] = round((df_segmento['lucro'] / df_segmento['valor_total_c/_desconto']) * 100, 2)
df_segmento

# Gráfico: faturamento por segmento
plt.figure(figsize=(10, 5))
df_segmento['valor_total_c/_desconto'].plot(kind='bar', color='pink')
plt.title('Faturamento por segmento')
plt.ylabel('Faturamento')
plt.xlabel('Segmentos')
plt.xticks(rotation=0)

# Análise por país
df_pais = df.groupby('pais')[colunas_lucro].sum().round(2)
df_pais['margem_lucro'] = round((df_pais['lucro'] / df_pais['valor_total_c/_desconto']) * 100, 2)
df_pais

# Análise por produto
df_produto = df.groupby('produto')[colunas_lucro].sum().round(2)
df_produto['margem_lucro'] = round((df_produto['lucro'] / df_produto['valor_total_c/_desconto']) * 100, 2)
df_produto

# Agrupamento geral
df_geral = df.groupby(['pais', 'segmento', 'produto'])[colunas_lucro].sum().round(2)
df_geral = df.groupby(['produto', 'segmento'])[colunas_lucro].sum().round(2)  # prejuízos

# Agregações com múltiplas funções
df.groupby('segmento').agg({
    'valor_total_c/_desconto': ['count', 'sum', 'mean', 'min', 'max'],
    'custo_total': 'mean',
    'lucro': ['min', 'max']
}).round(2)

# Filtragem: lucros negativos
df_prejuizo = df.query('lucro < 0')
df_prejuizo

# Prejuízo por país
df_prejuizo.groupby('pais')['lucro'].sum().round(2)

# Prejuízo por segmento
df_prejuizo.groupby('segmento')['lucro'].sum().round(2)

# Gráfico: produtos com prejuízo
df_grafico = df_prejuizo.groupby('produto')['lucro'].sum().round(2)
df_grafico.plot(kind='bar', color='pink')
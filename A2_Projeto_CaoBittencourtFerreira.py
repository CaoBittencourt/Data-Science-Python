# region OBJETIVO
# Estatísticas descritivas para comparar as despesas de domicílios de solteiros e domicílios com apenas dois adultos nas POFs 2002 e 2008 (com e sem variáveis de controle).
# endregion

# region BIBLIOTECAS
import pandas as pd 
import numpy as np
import os as os
import random
from pandas.core.frame import DataFrame

# endregion

# region IMPORTAÇÃO DOS DADOS
# Diretório de trabalho
os.chdir('C:/Users/Sony/Documents/GitHub/Data-Science-Python')

# Desabilitar max rows e max cols do Pandas para visualizar os dfs completamente
# pd.set_option('display.max_columns', None)
pd.set_option('max_row', None)

# POF 2002 
df_pof_2002 = pd.read_csv('pof_2002.csv', encoding='utf8')

# POF 2008 
df_pof_2008 = pd.read_csv('pof_2008.csv', encoding='utf8')

# endregion 

# region MANIPULAÇÃO DOS DADOS
# A. Nomes uniformes
# A.1. Sem pontos nos nomes 
df_pof_2002.columns = df_pof_2002.columns.str.replace(pat='.', repl='_')
df_pof_2008.columns = df_pof_2008.columns.str.replace(pat='.', repl='_')

# A.2. Sem espaços nos nomes 
df_pof_2002.columns = df_pof_2002.columns.str.replace(pat=' ', repl='_')
df_pof_2008.columns = df_pof_2008.columns.str.replace(pat=' ', repl='_')

# A.3. Sem 'control_' nos nomes
df_pof_2002.columns = df_pof_2002.columns.str.replace(pat='control_', repl='')
df_pof_2008.columns = df_pof_2008.columns.str.replace(pat='control_', repl='')

# A.4. Editar prefixos e sufixos (nomes de variáveis mais curtos)
df_pof_2002.columns = df_pof_2002.columns.str.replace('despesas_mensais_','d_m_')
df_pof_2008.columns = df_pof_2008.columns.str.replace('despesas_mensais_','d_m_')

df_pof_2002.columns = df_pof_2002.columns.str.replace('per_capita','p_c')
df_pof_2008.columns = df_pof_2008.columns.str.replace('per_capita','p_c')

df_pof_2002.columns = df_pof_2002.columns.str.replace('share_d_m_','prc_')
df_pof_2008.columns = df_pof_2008.columns.str.replace('share_d_m_','prc_')

# A.5. Nomes idênticos das variáveis de interesse
# Colunas em comum
df_pof_2002[df_pof_2002.columns.intersection(df_pof_2008.columns)].dtypes

# Colunas diferentes
df_pof_2002[df_pof_2002.columns.difference(df_pof_2008.columns)].dtypes
df_pof_2008[df_pof_2008.columns.difference(df_pof_2002.columns)].dtypes

# A.6. Dicionários para renomear as variáveis
pof_2002_dict = {#Dicionário para variáveis da POF 2002
    # Classe etária
    '(14,110]_anos':'adultos'
    # Domicílio
    , 'domc_cond_ocup':'domc_propriedade'
    , 'n_morador':'qtd_morador'
    , 'n_banh':'qtd_banheiros'
    , 'n_comodos':'qtd_comodos'
    , 'n_dorm':'qtd_dormitorios'
    # Chefe da família
    , 'chefe_anos_est':'chefe_anos_estudo'
    , 'chefe_orc_rend':'chefe_emprego'
    }

pof_2008_dict = {#Dicionário para variáveis da POF 2008
    # Classe etária
    '(14,104]_anos':'adultos'
    # Domicílio
    , 'domc_cod_cond_ocup':'domc_propriedade'
    , 'qtd_morador_domc':'qtd_morador'
    , 'qtd_comodos_domc':'qtd_comodos'
    , 'qtd_comd_serv_dormit':'qtd_dormitorios'
    # Chefe da família
    , 'chefe_anos_de_estudo':'chefe_anos_estudo'
    , 'chefe_cod_cor_raca':'chefe_cor'
    , 'chefe_cod_sexo':'chefe_sexo'
    , 'chefe_cod_sit_receita':'chefe_emprego'
    , 'chefe_idade_anos':'chefe_idade'
    # Renda
    , 'renda_total':'renda'
    , 'renda_total_p_c':'renda_p_c'   
    }

# A.7. Dfs renomeados
df_pof_2002 = df_pof_2002.rename(columns=pof_2002_dict)
df_pof_2008 = df_pof_2008.rename(columns=pof_2008_dict)

# B. Índice
df_pof_2002 = df_pof_2002.set_index('id_dom')
df_pof_2008 = df_pof_2008.set_index('id_dom')

# C. Variáveis de interesse
# C.1. Seleção de variáveis
list_despesas = [col for col in df_pof_2002 if col.startswith('d_m_')]
list_share = [col for col in df_pof_2002 if col.startswith('prc_')]
list_qtd_caract = [col for col in df_pof_2002 if col.startswith('qtd_') and 'Tem' in col] + ['qtd_Empregado']
list_qtd_dom = ['qtd_banheiros', 'qtd_dormitorios', 'qtd_comodos']
list_qtd_pessoas = ['qtd_morador', 'qtd_chefe', 'qtd_conjuge', 'qtd_filhos', 'qtd_outros_parentes', 'qtd_empregados', 'qtd_agregados', 'qtd_pensionistas', 'qtd_parentes_empregados']
list_qtd = list_qtd_caract + list_qtd_dom + list_qtd_pessoas
list_chefe = [col for col in df_pof_2002 if col.startswith('chefe_')]
list_vars = ['regiao', 'UF_sigla', 'classe_social', 'renda_p_c', 'urbano', 'adultos', 'domc_propriedade']

list_keep = list_vars.copy()
list_keep.extend(list_chefe)
list_keep.extend(list_qtd)
list_keep.extend(list_share)
list_keep.extend(list_despesas)

df_pof_2002 = df_pof_2002[list_keep]
df_pof_2008 = df_pof_2008[list_keep]

# C.2. Recode em variável 'urbano' (rural = 0, urbano = 1)
df_pof_2002['urbano'] = np.where(df_pof_2002['urbano'] == 1, 'Urbano', 'Rural')
df_pof_2008['urbano'] = np.where(df_pof_2008['urbano'] == 1, 'Urbano', 'Rural')

# C.3. Recode em variável 'adultos' (A = 1, AA = 2)
df_pof_2002['adultos'] = pd.Series(['A']*len(df_pof_2002)).str.repeat(repeats=df_pof_2002['adultos'])
df_pof_2008['adultos'] = pd.Series(['A']*len(df_pof_2008)).str.repeat(repeats=df_pof_2008['adultos'])

# D. Escopo: famílias do tipo A (um único adulto) vs AA (apenas dois adultos)
# D.1. Excluir pensionistas, empregados domésticos, parentes de empregados domésticos etc.
list_remove_ppl = ['qtd_empregados', 'qtd_agregados', 'qtd_pensionistas', 'qtd_parentes_empregados']

df_pof_2002 = df_pof_2002[(df_pof_2002[list_remove_ppl] == 0).all(axis=1)]
df_pof_2008 = df_pof_2008[(df_pof_2008[list_remove_ppl] == 0).all(axis=1)]

# D.2. Manter apenas as famílias dos tipos A e AA
df_pof_2002 = df_pof_2002[df_pof_2002['adultos'].isin(['A','AA'])]
df_pof_2008 = df_pof_2008[df_pof_2008['adultos'].isin(['A','AA'])]

# E. Tipos das variáveis
# df_pof_2002.dtypes
# df_pof_2008.dtypes

types_dict = {#Dicionário de tipos de variáveis
    'adultos':'category'
    , 'regiao':'category'
    , 'UF_sigla':'category'
    , 'classe_social':'category'
    , 'urbano':'category'
    , 'domc_propriedade':'category'
    , 'chefe_sexo':'category'
    , 'chefe_cor':'category'
    , 'chefe_emprego':'category'
    } 

df_pof_2002 = df_pof_2002.astype(types_dict)
df_pof_2008 = df_pof_2008.astype(types_dict)

# df_pof_2002.dtypes
# df_pof_2008.dtypes

# F. Breve descrição exploratória dos dados
df_pof_2002[[col for col in list_chefe if 'idade' not in col and 'estudo' not in col]].describe()
df_pof_2008[[col for col in list_chefe if 'idade' not in col and 'estudo' not in col]].describe()

df_pof_2002[list_chefe].describe()
df_pof_2008[list_chefe].describe()

df_pof_2002[list_qtd_pessoas].describe()
df_pof_2008[list_qtd_pessoas].describe()

df_pof_2002[list_qtd_caract].describe()
df_pof_2008[list_qtd_caract].describe()

df_pof_2002[list_qtd_dom].describe()
df_pof_2008[list_qtd_dom].describe()

df_pof_2002[list_despesas].describe()
df_pof_2008[list_despesas].describe()

df_pof_2002[list_share].describe()
df_pof_2008[list_share].describe()

# G. NA'S 
# G.1. Verificação de NA's nas variáveis de interesse
df_pof_2002[list_chefe].isna().sum() #Substituir NAs pela mediana do grupo (UF, classe social, rural vs urbano)
df_pof_2008[list_chefe].isna().sum() #Substituir NAs pela mediana do grupo (UF, classe social, rural vs urbano)

df_pof_2002[list_qtd_pessoas].isna().sum() #Ok
df_pof_2008[list_qtd_pessoas].isna().sum() #Ok

df_pof_2002[list_qtd_caract].isna().sum() #Ok
df_pof_2008[list_qtd_caract].isna().sum() #Ok

df_pof_2002[list_qtd_dom].isna().sum() #Ok
df_pof_2008[list_qtd_dom].isna().sum() #Ok

df_pof_2002[list_despesas].isna().sum().sum() #Ok
df_pof_2008[list_despesas].isna().sum().sum() #Ok

df_pof_2002[list_share].isna().sum().sum() #Ok
df_pof_2008[list_share].isna().sum().sum() #Ok

# G.2. Mediana agrupada das variáveis com NA
list_chefe_groups = ['UF_sigla', 'classe_social', 'urbano']

df_pof_2002['chefe_anos_estudo'] = (
    df_pof_2002
    .groupby(list_chefe_groups)['chefe_anos_estudo']
    .transform(
        lambda x: x.fillna(
            x.median()
            )
        )
)

df_pof_2008['chefe_anos_estudo'] = (
    df_pof_2008
    .groupby(list_chefe_groups)['chefe_anos_estudo']
    .transform(
        lambda x: x.fillna(
            x.median()
            )
        )
)

df_pof_2002[list_chefe].isna().sum() #Ok
df_pof_2008[list_chefe].isna().sum() #Ok

# endregion 

# region DESCRIÇÃO DOS DADOS
# A. Escopo
# A.1. Variáveis de interesse para comparação
list_despesas = [
    'totais'
    , 'alimentacao'
    , 'moradia'
    , 'vestuario'
    , 'transporte'
    # , 'higiene'
    # , 'saude'
    # , 'educacao'
    , 'lazer'
    # , 'viagens'
    # , 'bebidas_alcoolicas'
    # , 'fumo'
]

list_despesas_remove = [
    'infantil'
    , 'proxy'
    , 'menos_bebida'
    , 'homem_mulher'
    , 'lazer_adulto'
]

# A.2. Regular Expression para partial matching
regex_vars_interesse = 'renda_p_c|' + "|".join(list_despesas)
regex_vars_remove = "|".join(list_despesas_remove)

# A.3. Remover variáveis não utilizadas (alimentação menos bebidas alcoólicas)
df_pof_2002_temp = df_pof_2002.loc[:,~df_pof_2002.columns.str.contains(regex_vars_remove)]
df_pof_2008_temp = df_pof_2008.loc[:,~df_pof_2008.columns.str.contains(regex_vars_remove)]

# A.4. Apenas variáveis per capita
df_pof_2002_temp = df_pof_2002_temp.loc[:,df_pof_2002_temp.columns.str.contains('p_c')]
df_pof_2008_temp = df_pof_2008_temp.loc[:,df_pof_2008_temp.columns.str.contains('p_c')]

# A.5. Colunas para comparações
cols_pof_2002 = df_pof_2002_temp.loc[:,df_pof_2002_temp.columns.str.contains(regex_vars_interesse)].columns
cols_pof_2008 = df_pof_2008_temp.loc[:,df_pof_2008_temp.columns.str.contains(regex_vars_interesse)].columns

# B. Estatísticas descritivas sem controles (apenas comparando A vs AA)
# B.1. Dicionários de estatísticas descritivas
comp_pof_2002_sem_control = {#Dicionário de estatísticas descritivas
    x:
    df_pof_2002
    .groupby('adultos')[x]
    .describe()
    .pivot_table(values=['mean','25%','50%','75%'], columns='adultos')
    
    for x in cols_pof_2002
    # Equivalente a lapply(list,summary) no R
    }

comp_pof_2008_sem_control = {#Dicionário de estatísticas descritivas
    x:
    df_pof_2008
    .groupby('adultos')[x]
    .describe()
    .pivot_table(values=['mean','25%','50%','75%'], columns='adultos')
    
    for x in cols_pof_2008
    # Equivalente a lapply(list,summary) no R
    }

# B.2. Função de comparação de variáveis entre A vs AA (sem controles)
def pof_comp_casal(
    comp_pof: dict
    ,var: str
    ):
    
    # Cópia dos df incluso no dicionário de estatísticas descritivas por variável 
    df_pof = comp_pof[var].copy()

    #Comparação entre casais e solteiros
    df_pof[['var_prc_casal']] = df_pof['AA']/df_pof['A'] 
    #Benefício percentual dos casais sobre os solteiros em 1 mês (per capita)
    df_pof[['benef_prc_p_c_1m']] = 1 - df_pof[['var_prc_casal']] 
    #Benefício percentual dos casais sobre os solteiros em 1 mês (juntos)
    df_pof[['benef_prc_casal_1m']] = 2*df_pof['benef_prc_p_c_1m'] 
    #Benefício percentual em 1 ano (per capita)
    df_pof[['benef_acum_p_c_12m']] = 12*df_pof['benef_prc_p_c_1m'] 
    #Benefício percentual em 1 ano (juntos)
    df_pof[['benef_acum_casal_12m']] = 2*12*df_pof['benef_prc_p_c_1m'] 
    
    return(df_pof)

# B.3. Função de comparação de variáveis entre POFs (sem controles)
def pof_comp_ano(
    var: str
    ,comp_pof_ano1: dict
    ,comp_pof_ano2: dict
    ,ano1: int
    ,ano2: int
    ):
    
    # Cópias dos dfs inclusos no dicionário de estatísticas descritivas por variável 
    df_pof1 = comp_pof_ano1[var].copy()
    df_pof2 = comp_pof_ano2[var].copy()
    
    # Comparação entre os dois anos
    df_pof_comp = (df_pof2/df_pof1)
    
    # Taxa de crescimento da variável no período para os solteiros
    df_pof_comp[['tx_cresc_' + var + '_A']] = df_pof_comp['A']**(1/(ano2 - ano1)) - 1
    # Taxa de crescimento da variável no período para os casais
    df_pof_comp[['tx_cresc_' + var + '_AA']] = df_pof_comp['AA']**(1/(ano2 - ano1)) - 1
    # Diferença da taxa de crescimento da variável no período entre casais e solteiros
    df_pof_comp[['delta_tx_cresc_casal']] = df_pof_comp['tx_cresc_' + var + '_AA'] - df_pof_comp['tx_cresc_' + var + '_A'] 

    return(df_pof_comp)

# B.4. Exemplo: despesas totais
desp_totais = 'd_m_totais_p_c'

# POF 2008 vs POF 2002
pof_comp_ano(
    var=desp_totais
    ,comp_pof_ano1=comp_pof_2002_sem_control
    ,comp_pof_ano2=comp_pof_2008_sem_control
    ,ano1=2002
    ,ano2=2008
    )

# POF 2002: A vs AA
pof_comp_casal(
    var=desp_totais
    ,comp_pof=comp_pof_2002_sem_control
    )

# POF 2008: A vs AA
pof_comp_casal(
    var=desp_totais
    ,comp_pof=comp_pof_2008_sem_control
    )

# C. Estatísticas descritivas com controles
# C.1. Variáveis de controles baseadas nas características do domicílio e do chefe da família
list_controls = [
    var for var in list_vars + list_chefe
    if var != 'adultos'
    and var != 'renda_p_c'
    and 'idade' not in var
    and 'estudo' not in var
]

# C.2. Dicionários de estatísticas descritivas
comp_pof_2002_com_control = {
    x: {
        control:
        df_pof_2002
        .groupby(['adultos',control])[x]
        .describe()
        .reset_index()
        .pivot_table(
            index=control
            , values=['mean','25%','50%','75%']
            , columns='adultos')
        
        for control in list_controls 
        }
    
    for x in cols_pof_2002
}

comp_pof_2008_com_control = {
    x: {
        control:
        df_pof_2008
        .groupby(['adultos',control])[x]
        .describe()
        .reset_index()
        .pivot_table(
            index=control
            , values=['mean','25%','50%','75%']
            , columns='adultos')
        
        for control in list_controls 
        }
    
    for x in cols_pof_2008
}

# C.3. Função de comparação de variáveis entre A vs AA (com controles)
def pof_comp_casal_control(
    comp_pof: dict
    ,var: str
    ,control: str
):
    dfAA = (
        comp_pof[var][control]
        .loc[:,pd.IndexSlice[:,'AA']]
        .copy()
        )

    dfA = (
        comp_pof[var][control]
        .loc[:,pd.IndexSlice[:,'A']]
        .copy()
        )

    df_var_prc_casal = dfAA.div(dfA.values, axis=1).copy()
    df_benef_prc_p_c_1m = 1 - df_var_prc_casal
    df_benef_prc_casal_1m = 2*df_benef_prc_p_c_1m
    df_benef_acum_p_c_12m = 12*df_benef_prc_p_c_1m
    df_benef_acum_casal_12m = 2*12*df_benef_prc_p_c_1m

    df_var_prc_casal.columns = df_var_prc_casal.columns.droplevel(1)
    df_benef_prc_p_c_1m.columns = df_benef_prc_p_c_1m.columns.droplevel(1)
    df_benef_prc_casal_1m.columns = df_benef_prc_casal_1m.columns.droplevel(1)
    df_benef_acum_p_c_12m.columns = df_benef_acum_p_c_12m.columns.droplevel(1)
    df_benef_acum_casal_12m.columns = df_benef_acum_casal_12m.columns.droplevel(1)

    dict_return = {
        'var_prc_casal':df_var_prc_casal
        ,'benef_prc_p_c_1m':df_benef_prc_p_c_1m
        ,'benef_prc_casal_1m':df_benef_prc_casal_1m
        ,'benef_acum_p_c_12m':df_benef_acum_p_c_12m
        ,'benef_acum_casal_12m':df_benef_acum_casal_12m
    }
    
    df_return = pd.concat(dict_return, axis=0)

    return(df_return)

# C.4. Função de comparação entre POFs (com controles)
def pof_comp_ano_control(
    var: str
    ,control: str
    ,comp_pof_ano1: dict
    ,comp_pof_ano2: dict
    ,ano1: int
    ,ano2: int
):
    dfAA1 = (
        comp_pof_ano1[var][control]
        .loc[:,pd.IndexSlice[:,'AA']]
        .copy()
        )

    dfA1 = (
        comp_pof_ano1[var][control]
        .loc[:,pd.IndexSlice[:,'A']]
        .copy()
        )
    
    dfAA2 = (
        comp_pof_ano2[var][control]
        .loc[:,pd.IndexSlice[:,'AA']]
        .copy()
        )

    dfA2 = (
        comp_pof_ano2[var][control]
        .loc[:,pd.IndexSlice[:,'A']]
        .copy()
        )

    df_var_ano2_ano1_AA = dfAA2.div(dfAA1.values, axis=1).copy()**(1/(ano2 - ano1)) - 1
    df_var_ano2_ano1_A = dfA2.div(dfA1.values, axis=1).copy()**(1/(ano2 - ano1)) - 1
    df_var_ano2_ano1_delta = df_var_ano2_ano1_AA - df_var_ano2_ano1_A.values

    df_var_ano2_ano1_AA = df_var_ano2_ano1_AA.rename(columns={'AA':'tx_cresc_' + var}, level=1)
    df_var_ano2_ano1_A = df_var_ano2_ano1_A.rename(columns={'A':'tx_cresc_' + var}, level=1)
    df_var_ano2_ano1_delta = df_var_ano2_ano1_delta.rename(columns={'AA':'tx_cresc_' + var}, level=1)

    dict_return = {
        'AA':df_var_ano2_ano1_AA
        ,'A':df_var_ano2_ano1_A
        ,'delta':df_var_ano2_ano1_delta
    }

    df_return = pd.concat(dict_return, axis=0)
    df_return.columns = df_return.columns.swaplevel(0, 1)
    df_return = df_return.sort_index(axis=1, level=0)

    return(df_return)

# C.5. Exemplo: comparação aleatória (uma variável qualquer e um controle qualquer) 
var_exemplo = random.choice(cols_pof_2008)
control_exemplo = random.choice(list_controls)

# POF 2008 vs POF 2002
pof_comp_ano_control(
    var=var_exemplo
    ,control=control_exemplo
    ,comp_pof_ano1=comp_pof_2002_com_control
    ,comp_pof_ano2=comp_pof_2008_com_control
    ,ano1=2002
    ,ano2=2008
)

# POF 2002: A vs AA
pof_comp_casal_control(
    comp_pof=comp_pof_2002_com_control
    ,var=var_exemplo
    ,control=control_exemplo
)

# POF 2008: A vs AA
pof_comp_casal_control(
    comp_pof=comp_pof_2008_com_control
    ,var=var_exemplo
    ,control=control_exemplo
)

# endregion 

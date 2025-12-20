import itertools
import pandas as pd
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Leitura do dataset

df = pd.read_excel("MunicipioBrasil_20230102.xlsx")

df_regiao1 = df[df["cod_regiao"] == 1].copy()

# Definição das variáveis fuzzy

var1 = ctrl.Antecedent(np.arange(0, 101, 1), 'perc_dom_pobres_var1')
var2 = ctrl.Antecedent(np.arange(0, 1.001, 0.001), 'num_idhm')
var3 = ctrl.Antecedent(np.arange(0, 101, 1), 'per_dom_vuln_var3')
var4 = ctrl.Antecedent(np.arange(0, 101, 1), 'perc_pobres_0a11_var1')

saida = ctrl.Consequent(np.arange(0, 101, 1), 'indicador_auxilio')

# Funções de pertinência – Entradas

var1['baixissimo'] = fuzz.trimf(var1.universe, [0, 10, 20])
var1['baixo'] = fuzz.trimf(var1.universe, [15, 30, 40])
var1['mediano'] = fuzz.trimf(var1.universe, [35, 50, 60])
var1['alto'] = fuzz.trimf(var1.universe, [55, 65, 70])
var1['altissimo'] = fuzz.trimf(var1.universe, [65, 85, 100])

var2['baixo'] = fuzz.trimf(var2.universe, [0.0, 0.30, 0.55])
var2['medio'] = fuzz.trimf(var2.universe, [0.45, 0.65, 0.85])
var2['alto'] = fuzz.trimf(var2.universe, [0.75, 0.90, 1.0])

var3['baixissimo'] = fuzz.trimf(var3.universe, [0, 2, 5])
var3['baixo'] = fuzz.trimf(var3.universe, [4, 8, 10])
var3['mediano'] = fuzz.trimf(var3.universe, [9, 20, 30])
var3['alto'] = fuzz.trimf(var3.universe, [28, 50, 70])
var3['altissimo'] = fuzz.trimf(var3.universe, [65, 85, 100])

var4['baixissimo'] = fuzz.trimf(var4.universe, [0, 1, 2])
var4['baixo'] = fuzz.trimf(var4.universe, [1.5, 6, 10])
var4['mediano'] = fuzz.trimf(var4.universe, [9, 15, 20])
var4['alto'] = fuzz.trimf(var4.universe, [18, 28, 35])
var4['altissimo'] = fuzz.trimf(var4.universe, [30, 65, 100])

# Funções de pertinência – Saída

saida['baixissimo'] = fuzz.trimf(saida.universe, [0, 2, 5])
saida['baixo'] = fuzz.trimf(saida.universe, [4, 8, 10])
saida['mediano'] = fuzz.trimf(saida.universe, [9, 20, 30])
saida['alto'] = fuzz.trimf(saida.universe, [28, 50, 70])
saida['altissimo'] = fuzz.trimf(saida.universe, [65, 85, 100])

# Geração das 375 regras fuzzy

termos_var1 = ['baixissimo', 'baixo', 'mediano', 'alto', 'altissimo']
termos_var2 = ['baixo', 'medio', 'alto']
termos_var3 = ['baixissimo', 'baixo', 'mediano', 'alto', 'altissimo']
termos_var4 = ['baixissimo', 'baixo', 'mediano', 'alto', 'altissimo']

regras = []

for t1, t2, t3, t4 in itertools.product(
        termos_var1, termos_var2, termos_var3, termos_var4):

    severidade = termos_var1.index(
        t1) + (2-termos_var2.index(t2)) + termos_var3.index(t3) + termos_var4.index(t4)

    if severidade <= 4:
        saida_term = 'baixo'
    elif severidade <= 7:
        saida_term = 'mediano'
    elif severidade <= 10:
        saida_term = 'alto'
    else:
        saida_term = 'altissimo'

    regra = ctrl.Rule(
        var1[t1] & var2[t2] & var3[t3] & var4[t4],
        saida[saida_term]
    )

    regras.append(regra)

# Sistema fuzzy

sistema_ctrl = ctrl.ControlSystem(regras)
sistema = ctrl.ControlSystemSimulation(sistema_ctrl)

# Termo linguístico da saída


def termo_linguistico(valor):
    if valor <= 5:
        return "Baixíssimo"
    elif valor <= 10:
        return "Baixo"
    elif valor <= 30:
        return "Mediano"
    elif valor <= 70:
        return "Alto"
    else:
        return "Altíssimo"

# Processamento dos municípios


resultados = []

for _, row in df_regiao1.iterrows():
    sistema.input['perc_dom_pobres_var1'] = row['perc_dom_pobres_var1']
    sistema.input['num_idhm'] = row['num_idhm']
    sistema.input['per_dom_vuln_var3'] = row['per_dom_vuln_var3']
    sistema.input['perc_pobres_0a11_var1'] = row['perc_pobres_0a11_var1']

    sistema.compute()

    valor = sistema.output['indicador_auxilio']
    termo = termo_linguistico(valor)

    resultados.append([
        row['nom_mun'],
        round(valor, 2),
        termo
    ])

# Tabela final

tabela_final = pd.DataFrame(
    resultados,
    columns=[
        'MUNICIPIO',
        'INDICADOR DE NECESSIDADE',
        'TERMO LINGUISTICO'
    ]
)

tabela_final.to_excel("resultado_fuzzy.xlsx", index=False)

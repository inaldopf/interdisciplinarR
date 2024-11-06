# Libs
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import pickle
import pandas as pd
import numpy as np

load_dotenv()

mongo_uri = os.environ.get("URI_MONGO")

try:
    client = MongoClient(mongo_uri)
    print("Connected to MongoDB.")

    db = client["Khiata"]
    print("Database 'Khiata' accessed successfully.")

    # Função para obter o último registro e pré-processá-lo
    def obter_e_processar_ultimo_registro():
        forms = db["forms"]

        ultimo_registro = forms.find().sort("_id", -1).limit(1)
        ultimo_registro = list(ultimo_registro)

        if not ultimo_registro:
            raise ValueError("Nenhum registro encontrado no banco de dados.")

        ultimo_registro = ultimo_registro[0]  # Extrai o dicionário do registro
        id_registro = ultimo_registro.pop("_id", None)
        atributos = pd.DataFrame([ultimo_registro])
        atributos = atributos.drop("q8", axis=1)

        # Definir um mapeamento entre os nomes das colunas no banco e os esperados pelo pré-processador
        mapeamento_colunas = {
            "q1": "Faixa_Etaria",
            "q2": "Consumiu_Prod_Artesanal",
            "q3": "Freq_Compra_Prod_Artesanal",
            "q4": "Utilizou_App_Prod_Artesanal",
            "q5": "Qual seu nível de interesse em relação a produtos feitos à mão? ",
            "q6": "Tipo_Produto_Mais_Interessado",
            "q7": "Faixa_Preco_Interessado",
        }

        # Renomear as colunas para os nomes esperados
        atributos.rename(columns=mapeamento_colunas, inplace=True)

        # Pré-processamento
        with open(r"API\model\preprocessador.pkl", "rb") as f:
            preprocessador = pickle.load(f)

        # Garantir que todas as colunas esperadas estão presentes, preenchendo com np.nan
        colunas_esperadas = preprocessador.get_feature_names_out()

        atributos = atributos.reindex(columns=colunas_esperadas, fill_value=np.nan)

        # Aplicando o pré-processamento
        df_transformado = preprocessador.fit_transform(atributos)

        return df_transformado, id_registro

    # Função para prever se a pessoa é um potencial cliente
    def prever_cliente(df_transformado):
        # Carregar o modelo treinado (supondo que o modelo já esteja serializado)
        with open(r"API\model\classificador.pkl", "rb") as f:
            modelo_carregado = pickle.load(f)

        # Prever usando o modelo carregado
        predicao = modelo_carregado.predict(df_transformado)[0]
        predicao = int(predicao) if isinstance(predicao, np.int64) else predicao

        return predicao

    # Função para atualizar o registro com o resultado da previsão
    def atualizar_registro_com_previsao(id_registro, previsao):
        forms = db["forms"]
        forms.update_one({"_id": id_registro}, {"$set": {"avaliation": previsao}})

    # Obter e processar o último registro, fazer a previsão e atualizar o registro

    def call_all():
        df_transformado, id_ultimo_registro = obter_e_processar_ultimo_registro()
        previsao = prever_cliente(df_transformado)
        atualizar_registro_com_previsao(id_ultimo_registro, previsao)

        return "Previsão realizada e registro atualizado com sucesso."

except Exception as e:
    print("Failed to connect to MongoDB:", e)

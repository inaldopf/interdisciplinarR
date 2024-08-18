from pymongo import MongoClient

# Conectando ao servidor MongoDB
client = MongoClient("localhost", 27017)

db = client.bancoTeste


# documento = {"ids": 1}
# colecao.insert_one(documento)

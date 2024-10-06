from pymongo import MongoClient

# Conectando ao servidor MongoDB

db = MongoClient('mongodb+srv://Inaldo:Acess2012@khiata.64kjc.mongodb.net/?retryWrites=true&w=majority&appName=Khiata').get_database("Khiata")


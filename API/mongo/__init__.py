from pymongo import MongoClient

# Conectando ao servidor MongoDB


# Create a new client and connect to the server



client = MongoClient('mongodb+srv://Inaldo:Acess2012@khiata.64kjc.mongodb.net/?retryWrites=true&w=majority&appName=Khiata')

db = client['Khiata']

from pymongo import MongoClient

uri = "mongodb+srv://Inaldo:Acess2012@khiata.64kjc.mongodb.net/?retryWrites=true&w=majority&appName=Khiata"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client['Khiata']

order = db["order"]
order = order.find()

for i in order:
    print(i)
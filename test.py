from pymongo import MongoClient
from API.Predis.main import setCart
from API.mongo.main import redisCart, getOrderByCpf

uri = "mongodb+srv://Inaldo:acess2012@khiata.64kjc.mongodb.net/?retryWrites=true&w=majority&appName=Khiata"

# Create a new client and connect to the server
client = MongoClient(uri)

db = client["Khiata"]

print(getOrderByCpf("98765432100"))

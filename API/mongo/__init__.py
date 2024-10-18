from pymongo import MongoClient
import os

BD = os.getenv("BD")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")

client = MongoClient(
    f"mongodb+srv://{USER}:{PASSWORD}@khiata.64kjc.mongodb.net/?retryWrites=true&w=majority&appName=Khiata"
)

db = client[f"{BD}"]

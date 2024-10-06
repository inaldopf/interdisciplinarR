from .__init__ import db


colecao = db.get_collection("order")

# print(dict(colecao.find_one()))


def getColection():
    return dict(colecao.find_one())

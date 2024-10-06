from .__init__ import db


colecao = db.order

# print(dict(colecao.find_one()))


def getColection():
    return dict(colecao.find_one())

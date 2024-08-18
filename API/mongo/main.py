from .__init__ import db


colecao = db.colecaoTeste

# print(dict(colecao.find_one()))


def getCol():
    return dict(colecao.find_one())

from sqlalchemy import Column, String, Integer, DateTime

from datetime import datetime

from typing import Union

from model import Base


class Filme(Base):
    __tablename__ = 'filme'

    id = Column("pk_filme", Integer, primary_key=True)
    nome = Column(String(60), index=True)
    ano = Column(Integer)
    resumo = Column(String(350))
    imageUrl = Column(String(255))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome: str, ano: int, resumo: str, imageUrl: str, data_insercao: Union[DateTime, None] = None):
        self.nome = nome
        self.ano = ano
        self.resumo = resumo
        self.imageUrl = imageUrl

        if data_insercao:
            self.data_insercao = data_insercao
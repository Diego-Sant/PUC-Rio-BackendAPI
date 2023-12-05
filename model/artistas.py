from sqlalchemy import Column, String, Integer, DateTime

from datetime import datetime
from typing import Union

from model import Base

class Artistas(Base):
    __tablename__ = 'artistas'

    id = Column("pk_artistas", Integer, primary_key=True)
    nome = Column(String(100), index=True)
    idade = Column(Integer)
    imageUrl = Column(String(255))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome: str, idade: int, imageUrl: str, data_insercao: Union[DateTime, None] = None):
        self.nome = nome
        self.idade = idade
        self.imageUrl = imageUrl

        if data_insercao:
            self.data_insercao = data_insercao
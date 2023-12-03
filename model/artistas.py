from sqlalchemy import Column, String, Integer, DateTime

from datetime import datetime
from typing import Union, Optional

from model import Base

class Artistas(Base):
    __tablename__ = 'artistas'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    idade = Column(Integer)
    imageUrl = Column(Optional(String(255)))
    data_insercao = Column(DateTime, default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    def __init__(self, nome: str, idade: int = None, imageUrl: str = None, data_insercao: Union[DateTime, None] = None):
        self.nome = nome
        self.idade = idade
        self.imageUrl = imageUrl

        if data_insercao:
            self.data_insercao = data_insercao
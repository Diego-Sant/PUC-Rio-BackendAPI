from sqlalchemy import Column, String, Integer, DateTime

from datetime import datetime

from typing import Union, Optional

from model import Base


class Filme(Base):
    __tablename__ = 'filme'

    id = Column(Integer, primary_key=True)
    nome = Column(String(60), unique=True)
    ano = Column(Integer)
    resumo = Column(String(1000))
    imageUrl = Column(Optional(String(255)))
    data_insercao = Column(DateTime, default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    def __init__(self, nome: str, ano: int = None, resumo: str = None, imageUrl: str = None, data_insercao: Union[DateTime, None] = None):
        self.nome = nome
        self.ano = ano
        self.resumo = resumo
        self.imageUrl = imageUrl

        if data_insercao:
            self.data_insercao = data_insercao
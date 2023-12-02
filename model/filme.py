from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

from typing import Union, List

from model import Base, ArtistaFilme


class Filme(Base):
    __tablename__ = 'filme'

    id = Column("pk_filme", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    artistas = relationship('ArtistaFilme', back_populates='filme')
    resumo = Column(String(4000))
    imageUrl = Column(String(255))
    data_insercao = Column(DateTime, default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    def __init__(self, nome: str, artistas: Union[List['ArtistaFilme'], None] = None, resumo: str = None, imageUrl: str = None, data_insercao: Union[DateTime, None] = None):
        self.nome = nome
        self.artistas = artistas if artistas is not None else []
        self.resumo = resumo
        self.imageUrl = imageUrl

        if data_insercao:
            self.data_insercao = data_insercao
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime
from typing import Union, List

from model import Base

class Artistas(Base):
    __tablename__ = 'artistas'

    id = Column(Integer, primary_key=True)
    nome = Column(String(140))
    filmes = relationship('ArtistaFilme', back_populates='artista')
    data_insercao = Column(DateTime, default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    def __init__(self, nome: str, filmes: Union[List['ArtistaFilme'], None] = None, data_insercao: Union[DateTime, None] = None):
        self.nome = nome
        self.filmes = filmes if filmes else []

        if data_insercao:
            self.data_insercao = data_insercao

class ArtistaFilme(Base):
    __tablename__ = 'artista_filme'

    id = Column(Integer, primary_key=True)
    artista_id = Column(Integer, ForeignKey('artistas.id'))
    filme_id = Column(Integer, ForeignKey('filme.pk_filme'))
    artista = relationship('Artistas', back_populates='filmes')
    filme = relationship('Filme', back_populates='artistas')
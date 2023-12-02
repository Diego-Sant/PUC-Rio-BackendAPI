from pydantic import BaseModel
from typing import Optional, List
from model.filme import Filme

from schemas import ArtistasSchema

class FilmeSchema(BaseModel):
    nome: str
    artistas: List[ArtistasSchema]
    resumo: str

    class Config:
        orm_mode = True

class FilmeBuscaSchema(BaseModel):
    nome: str

class ListagemFilmesSchema(BaseModel):
    filmes: List[FilmeSchema]

def apresenta_filmes(filmes: List[Filme]):
    result = []
    for filme in filmes:
        result.append({
            "nome": filme.nome,
            "artistas": filme.artistas,
            "resumo": filme.resumo,
        })

    return {"filmes": result}

class FilmeViewSchema(BaseModel):
    id: int = 1
    nome: str = "Homem-Aranha: Sem Volta para Casa"
    resumo: str = "Com a identidade do Homem-Aranha revelada, para restabelecer seu segredo, Peter Parker pede ajuda ao Doutor Estranho. O feitiço do mago, porém, corre mal e acaba trazendo vilões do Homem-Aranha de outros universos."
    total_artistas: int = 1
    artistas:List[ArtistasSchema]

class FilmeDeleteSchema(BaseModel):
    mesage: str
    nome: str

def apresenta_filme(filme: Filme):
    return {
        "id": filme.id,
        "nome": filme.nome,
        "resumo": filme.resumo,
        "total_artistas": len(filme.artistas),
        "artistas": [{"texto": c.texto} for c in filme.artistas]
    }
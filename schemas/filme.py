from pydantic import BaseModel
from typing import Optional, List
from model.filme import Filme

class FilmeSchema(BaseModel):
    nome: str = "Oppenheimer"
    ano: int = 2023
    resumo: str = "A história do físico americano J. Robert Oppenheimer, seu papel no Projeto Manhattan e no desenvolvimento da bomba atômica durante a Segunda Guerra Mundial, e o quanto isso mudaria a história do mundo para sempre."
    imageUrl: str = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2/jvaI1gezzvhkKid00goKxz9fAso.jpg"

    class Config:
        orm_mode = True

class FilmeBuscaSchema(BaseModel):
    nome: str = "Oppenheimer"

class ListagemFilmesSchema(BaseModel):
    filmes: List[FilmeSchema]

def apresenta_filmes(filmes: List[Filme]):
    # Retorna uma representação do filme seguindo o schema definido em FilmeViewSchema.
    
    result = []
    for filme in filmes:
        result.append({
            "nome": filme.nome,
            "ano": filme.ano,
            "resumo": filme.resumo,
            "imageUrl": filme.imageUrl
        })

    return {"filmes": result}

class FilmeViewSchema(BaseModel):
    id: int = 1
    nome: str = "Homem-Aranha: Sem Volta para Casa"
    resumo: str = "Com a identidade do Homem-Aranha revelada, para restabelecer seu segredo, Peter Parker pede ajuda ao Doutor Estranho. O feitiço do mago, porém, corre mal e acaba trazendo vilões do Homem-Aranha de outros universos."
    imageUrl: str = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2/fVzXp3NwovUlLe7fvoRynCmBPNc.jpg"
    ano: int = 2012

class FilmeDeleteSchema(BaseModel):
    message: str
    nome: str

def apresenta_filme(filme: Filme):
    return {
        "id": filme.id,
        "nome": filme.nome,
        "ano": filme.ano,
        "resumo": filme.resumo,
        "imageUrl": filme.imageUrl
    }
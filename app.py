from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from flask_cors import CORS

from urllib.parse import unquote

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from model import Session, Artistas, Filme
from logger import logger
from schemas import *

info = Info(title="API PUC-Rio", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc.")
filme_tag = Tag(name="Filme", description="Adição, visualização, edição e remoção de filmes.")
artista_tag = Tag(name="Artistas", description="Adição, visualização, remoção e edição de artistas.")

@app.get('/', tags=[home_tag])
def home():
    # Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    return redirect('/openapi')

@app.post('/filme', tags=[filme_tag], responses={"200": FilmeViewSchema, "409": ErrorSchema, "400": ErrorSchema})

def add_filme(form: FilmeSchema):
    filme = Filme(
        ano=form.ano,
        imageUrl=form.imageUrl,
        nome=form.nome,
        resumo=form.resumo)
    
    logger.debug(f"Adicionando nome do filme: '{filme.nome}'")
    try:
        session = Session()

        # adicionando filme
        session.add(filme)

        # efetivando o camando de adição de novo item na tabela
        session.commit()

        logger.debug(f"Nome do filme adicionado com sucesso: '{filme.nome}'")
        return apresenta_filme(filme), 200
    
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Já existe um filme no banco de dados com esse nome."
        logger.warning(f"Erro ao adicionar filme '{filme.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Aconteceu um erro inesperado. Tente novamente mais tarde!"
        logger.warning(f"Erro ao adicionar filme '{filme.nome}', {error_msg}")
        return {"message": error_msg}, 400

@app.get('/filmes', tags=[filme_tag], responses={"200": ListagemFilmesSchema, "404": ErrorSchema})

def get_filmes():
    logger.debug(f"Procurando todos os filmes...")
    session = Session()

    # fazendo a busca
    filmes = session.query(Filme).all()

    if not filmes:
        return {"Não há nenhum filme com esse nome no nosso banco de dados!": []}, 200
    else:
        logger.debug(f"%d filmes encontrados no nosso banco de dados!" % len(filmes))
    
    # retorna a representação de filmes
    print(filmes)
    return apresenta_filmes(filmes), 200

@app.get('/filme', tags=[filme_tag], responses={"200": FilmeViewSchema, "404": ErrorSchema})

def get_filme(query: FilmeBuscaSchema):
    filme_nome = query.nome

    logger.debug(f"Procurando todos os filmes... #{filme_nome}")
    session = Session()

    # fazendo a busca
    filme = session.query(Filme).filter(func.lower(Filme.nome) == func.lower(filme_nome)).first()

    if not filme:
        error_msg = "Não há nenhum filme com esse nome no nosso banco de dados!"  
        logger.warning(f"Erro ao buscar o filme desejado.'{filme_nome}', {error_msg}")
        return {"message": error_msg}, 404

    else:
        logger.debug(f"Filmes com a seguinte pesquisa encontrados: '{filme.nome}'")

        return apresenta_filme(filme), 200

@app.delete('/filme', tags=[filme_tag], responses={"200": FilmeDeleteSchema, "404": ErrorSchema})

def delete_filme(query: FilmeBuscaSchema):

    # Deleta um filme a partir do nome de filme informado
    filme_nome = unquote((query.nome))

    print(filme_nome)

    logger.debug(f"Deletando dados sobre o filme {filme_nome}")
    session = Session()

    # fazendo a remoção
    count = session.query(Filme).filter(Filme.nome == filme_nome).delete()

    session.commit()
    
    if count:
        logger.debug(f"O filme {filme_nome} foi deletado com sucesso!")
        return {"message": "Filme removido", "nome": filme_nome}
    else:
        error_msg = "Não há nenhum filme com esse nome no nosso banco de dados!"
        logger.warning(f"Erro ao deletar o filme '{filme_nome}', {error_msg}")
        return {"message": error_msg}, 404

@app.put('/filme', tags=[filme_tag], responses={"200": FilmeViewSchema, "404": ErrorSchema})
def edit_filme(query: FilmeBuscaSchema, form: FilmeSchema):
    filme_nome = unquote(query.nome)

    logger.debug(f"Editando dados sobre o filme {filme_nome}")
    session = Session()

    # fazendo a busca
    filme = session.query(Filme).filter(func.lower(Filme.nome) == func.lower(filme_nome)).first()

    if not filme:
        error_msg = "Não há nenhum filme com esse nome no nosso banco de dados!"  
        logger.warning(f"Erro ao editar o filme desejado.'{filme_nome}', {error_msg}")
        return {"message": error_msg}, 404

    # Atualizando os dados do filme
    filme.nome = form.nome
    filme.ano = form.ano
    filme.resumo = form.resumo
    filme.imageUrl = form.imageUrl

    # efetivando o comando de edição
    session.commit()

    logger.debug(f"Os dados do filme {filme_nome} foram editados com sucesso!")
    return apresenta_filme(filme), 200

@app.post('/artista', tags=[artista_tag], responses={"200": ArtistaViewSchema, "409": ErrorSchema, "400": ErrorSchema})

def add_artista(form: ArtistasSchema):

    artista = Artistas(
        nome=form.nome,
        idade=form.idade,
        imageUrl=form.imageUrl)

    logger.debug(f"Adicionando nome do artista: '{artista.nome}'")
    try:
        # criando conexão com a base
        session = Session()

        # adicionando artista
        session.add(artista)

        # efetivando o camando de adição de novo item na tabela
        session.commit()

        logger.debug(f"Nome do artista adicionado com sucesso: '{artista.nome}'")
        return apresenta_artista(artista), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Já existe um artista no banco de dados com esse nome."
        logger.warning(f"Erro ao adicionar o artista '{artista.nome}', {error_msg}")
        return {"message": error_msg}, 409


    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Aconteceu um erro inesperado. Tente novamente mais tarde!"
        logger.warning(f"Erro ao adicionar o artista '{artista.nome}', {error_msg}")
        return {"message": error_msg}, 400
    
@app.get('/artistas', tags=[artista_tag], responses={"200": ListagemArtistaSchema, "404": ErrorSchema})

def get_artistas():
    logger.debug(f"Procurando todos os artistas...")
    session = Session()

    # fazendo a busca
    artistas = session.query(Artistas).all()

    if not artistas:
        return {"Não há nenhum artista com esse nome no nosso banco de dados!": []}, 200
    else:
        logger.debug(f"%d artistas encontrados no nosso banco de dados!" % len(artistas))
        print(artistas)
        return apresenta_artistas(artistas), 200

@app.delete('/artista', tags=[artista_tag], responses={"200": ArtistaDeleteSchema, "404": ErrorSchema})

def delete_artista(query: ArtistaBuscaSchema):
    artista_nome = unquote((query.nome))
    print(artista_nome)

    logger.debug(f"Deletando dados sobre o artista {artista_nome}")
    session = Session()

    # fazendo a remoção
    count = session.query(Artistas).filter(Artistas.nome == artista_nome).delete()
    session.commit()

    if count:
        logger.debug(f"O artista {artista_nome} foi deletado com sucesso!")
        return {"message": "Artista removido", "nome": artista_nome}
    else:
        error_msg = "Não há nenhum artista com esse nome no nosso banco de dados!"
        logger.warning(f"Erro ao deletar o artista '{artista_nome}', {error_msg}")
        return {"message": error_msg}, 404
    
@app.put('/artista', tags=[artista_tag], responses={"200": ArtistaViewSchema, "404": ErrorSchema})
def edit_artista(query: ArtistaBuscaSchema, form: ArtistasSchema):
    artista_nome = unquote(query.nome)

    logger.debug(f"Editando dados sobre o artista {artista_nome}")
    session = Session()

    # fazendo a busca
    artista = session.query(Artistas).filter(func.lower(Artistas.nome) == func.lower(artista_nome)).first()

    if not artista:
        error_msg = "Não há nenhum artista com esse nome no nosso banco de dados!"  
        logger.warning(f"Erro ao editar o artista desejado.'{artista_nome}', {error_msg}")
        return {"message": error_msg}, 404

    # Atualizando os dados do artista
    artista.nome = form.nome
    artista.idade = form.idade
    artista.imageUrl = form.imageUrl

    # efetivando o comando de edição
    session.commit()

    logger.debug(f"Os dados do artista {artista_nome} foram editados com sucesso!")
    return apresenta_artista(artista), 200
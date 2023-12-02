from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from schemas import *
from flask_cors import CORS

info = Info(title="API PUC-Rio", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


@app.get('/')
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')

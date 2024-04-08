from flask import Blueprint, Response, request
from models.table import User, db
import json

user_blueprint = Blueprint('user', __name__)

# fazer um gerador de response
def gera_response(status, nome_conteudo, conteudo, mensagem=False): 
    body = {}
    body[nome_conteudo] = conteudo
    if mensagem: 
        body[mensagem] = mensagem
    return Response(json.dumps(body), status=status, mimetype='application/json')

# crud
# selecionar todos
@user_blueprint.route("/usuarios", methods=['GET'])
def selecionar_users(): 
    users = User.query.all()
    users_json = [c.to_json() for c in users]
    return gera_response(200, "usuarios", users_json)


# selecionar um
# cadastrar 
# atualizar 
# deletar
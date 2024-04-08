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
@user_blueprint.route("/usuarios/<id>", methods=['GET'])
def selecionar_user(id): 
    user = User.query.filter(id).first()
    user_json = user.to_json()
    return Response(200, "usuario", user_json)

# cadastrar 
@user_blueprint.route("/usuarios/<id>", methods=['POST'])
def cadastrar(id): 
    # verificar se user ja existe
    verificar = User.query.get(id)
    if verificar is None: 
        return gera_response(404, "", {}, mensagem='Usuário não encontrado')
    
    # adicionar user
    receber_user = request.json
    cadastrar = User(nome=receber_user['nome'], senha=receber_user['senha'], email=receber_user['email'])
    db.session.add(cadastrar)
    db.session.commit()
    return gera_response(204, "", {}, mensagem='cadastro realizado com sucesso!')

# atualizar
@user_blueprint.route("/usuarios/<id>", methods=['PUT'])
def update(id): 
    # verificar se existe
    verificar = User.query.get(id)
    if verificar is None: 
        return gera_response(404, '', {}, mensagem='Usuário não cadastrado')
    
    # ver qual campo será alterado
    receber_resp = request.json
    if 'nome' in receber_resp: 
        User.nome = receber_resp['nome']
    if 'senha' in receber_resp: 
        User.senha = receber_resp['senha']
    if 'email' in receber_resp: 
        User.email = receber_resp['email']
    db.session.commit()

    return gera_response(204, '', {}, mensagem='Usuário atualizado.')

# deletar
@user_blueprint.route("/usuarios/<id>", methods=['DELETE'])
def deletar(id): 
    user = User.query.get(id) 
    if user is None: 
        return gera_response(404, '', {}, mensagem='Usuário não encontrado!')
    
    db.session.delete(user)
    db.session.commit()
    return gera_response(200, '', {}, mensagem='usuário deletado!')
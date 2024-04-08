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
    if request.method == 'GET': 
        users = User.query.all()
        users_json = [c.to_json() for c in users]
        return gera_response(200, "usuarios", users_json)
    else:
        return 'erro! metodo invalido'
# selecionar um
@user_blueprint.route("/usuarios/<id>", methods=['GET'])
def selecionar_user(id): 
    user = User.query.filter_by(id=id).first()
    user_json = user.to_json()
    return Response(200, "usuario", user_json)

# cadastrar 
@user_blueprint.route("/usuarios/", methods=['POST'])
def cadastrar(): 
    if request.method == 'POST': 
        # adicionar user
        receber_user = request.json
        cadastrar = User(nome=receber_user['nome'], senha=receber_user['senha'], email=receber_user['email'])
        db.session.add(cadastrar)
        db.session.commit()
        return gera_response(204, "", {}, mensagem='cadastro realizado com sucesso!')
    else: 
        return 'erro! metodo invalido'

# atualizar
@user_blueprint.route("/usuarios/<id>", methods=['PUT'])
def update(id): 
    if request.method == 'PUT': 
        # verificar se existe
        verificar = User.query.get(id)
        if verificar: 
            # ver qual campo será alterado
            receber_resp = request.json
            if receber_resp:
                if 'nome' in receber_resp: 
                    verificar.nome = receber_resp['nome']
                if 'senha' in receber_resp: 
                    verificar.senha = receber_resp['senha']
                if 'email' in receber_resp: 
                    verificar.email = receber_resp['email']
                db.session.commit()
                return gera_response(204, '', {}, mensagem='Usuário atualizado.')
            else: 
                return gera_response(400, '', {}, mensagem='Corpo da requisição vazio')
        else: 
            return gera_response(404, '', {}, mensagem='Usuario não encontrado!')
    else:
        return 'erro! metodo invalido'

# deletar
@user_blueprint.route("/usuarios/<id>", methods=['DELETE'])
def deletar(id): 
    user = User.query.get(id) 
    if user is None: 
        return gera_response(404, '', {}, mensagem='Usuário não encontrado!')
    
    db.session.delete(user)
    db.session.commit()
    return gera_response(200, '', {}, mensagem='usuário deletado!')
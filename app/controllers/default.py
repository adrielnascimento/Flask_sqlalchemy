from flask import Blueprint, Response, request, jsonify
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

def erro(): 
    return jsonify({'error': 'Houve um erro na requisição, por favor use o método correto.'}), 400

# crud
# selecionar todos
@user_blueprint.route("/usuarios", methods=['GET'])
def selecionar_users(): 
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int) 
        users = User.query.paginate(page=page, per_page=per_page)
        users_json = [user.to_json() for user in users.items]
        return gera_response(200, "usuarios", users_json, mensagem='Consulta bem-sucedida',
                             total_items=users.total, total_pages=users.pages,
                             current_page=users.page, per_page=per_page)
    else:
        return erro()
    
# selecionar um
@user_blueprint.route("/usuarios/<id>", methods=['GET'])
def selecionar_user(id): 
    user = User.query.filter_by(id=id).first()
    if user is None: 
        return gera_response(404, '', {}, mensagem='Usuário não existe')
    
    user_json = user.to_json()
    return Response(200, "usuario", user_json)

# cadastrar 
@user_blueprint.route("/usuarios", methods=['POST'])
def cadastrar(): 
    if request.method == 'POST': 
        require = ['nome', 'senha', 'email']
        if not all(field in request.json for field in require): 
            return gera_response(400, '', {}, mensagem='todos os campos são obrigatorios')
        
        # adicionar user
        receber_user = request.json
        cadastrar = User(nome=receber_user['nome'], senha=receber_user['senha'], email=receber_user['email'])
        db.session.add(cadastrar)
        db.session.commit()
        return gera_response(204, "", {}, mensagem='cadastro realizado com sucesso!')
    else: 
        return erro()

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
        return erro()

# deletar
@user_blueprint.route("/usuarios/<id>", methods=['DELETE'])
def deletar(id):
    if request.method == 'DELETE':  
        user = User.query.get(id) 
        if user is None: 
            return gera_response(404, '', {}, mensagem='Usuário não encontrado!')
        
        db.session.delete(user)
        db.session.commit()
        return gera_response(200, '', {}, mensagem='usuário deletado!')
    else:
        return erro()
from flask import Flask
from models.table import db
from controllers.default import user_blueprint

app = Flask(__name__)

#configuração do banco
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'

db.init_app(app)
app.register_blueprint(user_blueprint)

if __name__ == "__main__": 
    with app.test_request_context():
        db.create_all()
    app.run(debug=True)
from flask import Flask
app = Flask(__name__)

#configuração do banco
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'


if __name__ == "__main__": 
    app.run(debug=True)
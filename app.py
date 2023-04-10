from  flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
  return "Olá, mundo! Esse é meu site. (João)"

@app.route("/sobre")
def sobre():
  return "João Leite é jornalsita de dados em formação pelo Insper(SP)."

@app.route("/contato")
def contato():
  return "Aqui vai o conteúdo da página sobre"

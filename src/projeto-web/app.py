#app.py
from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB

app = Flask(__name__)

db = TinyDB("posts.json")

@app.route("/")
def index():
    return render_template("index.html")

# @app.route("/sobre", methods=["GET", "POST"])
# def sobre(nome=None):
#     if request.method == "POST":
#         nome = request.form.get("nome")
#         db.insert({"nome": nome})
#     posts = db.all()
#     return render_template("sobre.html", nome=nome, posts=posts)

@app.route("/novo", methods=["GET", "POST"])
def novo(rota = None):
    if request.method == "POST":
        rota = request.form.get("rota")
        db.insert({"X": rota})
        db.insert({"Y": rota})
        db.insert({"Z": rota})
        db.insert({"W": rota})
    posts = db.all()
    return render_template("novo.html", rota=rota, posts=posts)

@app.route("/pegar_caminho", methods=["GET"])
def pegar_caminho():
    return render_template("pegar_caminho.html", pegar_caminho=pegar_caminho)

@app.route("/atualizar", methods=["GET"])
def index():
    return render_template("atualizar.html")

@app.route("/deletar", methods=["DELETE"])
def index():
    return render_template("deletar.html")

@app.route("/listas_caminhos", methods=["GET"])
def index():
    return render_template("Listas_caminhos.html")

@app.route("/pegar_caminhos", methods=["GET"])
def index():
    return render_template("pegar_caminhos.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
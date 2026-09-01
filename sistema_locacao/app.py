from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import conectar

app = Flask(__name__)

app.secret_key = "chave-secreta-sistema-locacao"


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        # Funcionário de teste
        if email == "admin@admin.com" and senha == "1234":

            session["funcionario_id"] = 1
            session["funcionario_nome"] = "Administrador"

            return redirect(url_for("index"))

        flash("E-mail ou senha incorretos.")

    return render_template("login.html")


@app.route("/")
def index():

    if "funcionario_id" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))

@app.route("/equipamentos")
def equipamentos():
    return render_template("equipamentos.html")


@app.route("/estoque")
def estoque():
    return render_template("estoque.html")


@app.route("/funcionario")
def funcionario():
    return render_template("funcionario.html")


@app.route("/registro")
def registro():
    return render_template("registro.html")


if __name__ == "__main__":
    app.run(debug=True)
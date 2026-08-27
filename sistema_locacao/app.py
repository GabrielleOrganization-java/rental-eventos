from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import conectar


app = Flask(__name__)

app.secret_key = "chave-secreta-sistema-locacao"


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["senha"]

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT id, nome, senha
            FROM funcionario
            WHERE email = %s
        """, (email,))

        funcionario = cursor.fetchone()

        cursor.close()
        conexao.close()

        if funcionario is not None:

            funcionario_id = funcionario[0]
            nome = funcionario[1]
            senha_banco = funcionario[2]

            if senha == senha_banco:

                session["funcionario_id"] = funcionario_id
                session["funcionario_nome"] = nome

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


if __name__ == "__main__":
    app.run(debug=True)
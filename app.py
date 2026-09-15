from flask import Flask, request, jsonify
from flask_cors import CORS
from database import conectar
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps


app = Flask(__name__)
CORS(app)

SECRET = "chave-secreta-rental"


# ============================================================
# JWT - VERIFICAR TOKEN
# ============================================================

def token_required(f):
    @wraps(f)
    def verificar(*args, **kwargs):

        auth = request.headers.get("Authorization")

        if not auth or not auth.startswith("Bearer "):
            return jsonify({
                "erro": "Token não informado"
            }), 401

        token = auth.split(" ", 1)[1]

        try:
            jwt.decode(
                token,
                SECRET,
                algorithms=["HS256"]
            )

        except jwt.InvalidTokenError:
            return jsonify({
                "erro": "Token inválido ou expirado"
            }), 401

        return f(*args, **kwargs)

    return verificar


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["POST"])
def login():

    dados = request.json

    email = dados["email"]
    senha = dados["senha"]

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, email
        FROM funcionario
        WHERE email = %s AND senha = %s
    """, (email, senha))

    funcionario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if funcionario:

        token = jwt.encode(
            {
                "id": funcionario[0],
                "nome": funcionario[1],
                "exp": datetime.now(timezone.utc) + timedelta(hours=2)
            },
            SECRET,
            algorithm="HS256"
        )

        return jsonify({
            "mensagem": "Login realizado",
            "token": token,
            "id": funcionario[0],
            "nome": funcionario[1],
            "email": funcionario[2]
        })

    return jsonify({
        "mensagem": "Email ou senha incorretos"
    }), 401


# ============================================================
# FUNCIONÁRIOS
# ============================================================

@app.route("/funcionarios", methods=["GET"])
@token_required
def listar_funcionarios():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, cpf, email
        FROM funcionario
        ORDER BY id
    """)

    funcionarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    lista = []

    for funcionario in funcionarios:

        lista.append({
            "id": funcionario[0],
            "nome": funcionario[1],
            "cpf": funcionario[2],
            "email": funcionario[3]
        })

    return jsonify(lista)


@app.route("/funcionarios", methods=["POST"])
@token_required
def cadastrar_funcionario():

    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO funcionario
        (nome, cpf, email, senha)
        VALUES (%s, %s, %s, %s)
    """, (
        dados["nome"],
        dados["cpf"],
        dados["email"],
        dados["senha"]
    ))

    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({
        "mensagem": "Funcionário cadastrado"
    })


@app.route("/funcionarios", methods=["DELETE"])
@token_required
def deletar_funcionario():

    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM registro
        WHERE funcionario_id = %s
    """, (dados["id"],))

    cursor.execute("""
        DELETE FROM funcionario
        WHERE id = %s
    """, (dados["id"],))

    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({
        "mensagem": "Funcionário deletado"
    })


# ============================================================
# EQUIPAMENTOS
# ============================================================

@app.route("/equipamentos", methods=["GET"])
@token_required
def listar_equipamentos():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, marca, modelo, categoria, potencia,
               material, peso, dimensoes, cor
        FROM equipamento
        ORDER BY id
    """)

    equipamentos = cursor.fetchall()

    cursor.close()
    conexao.close()

    lista = []

    for equipamento in equipamentos:

        lista.append({
            "id": equipamento[0],
            "marca": equipamento[1],
            "modelo": equipamento[2],
            "categoria": equipamento[3],
            "potencia": equipamento[4],
            "material": equipamento[5],
            "peso": equipamento[6],
            "dimensoes": equipamento[7],
            "cor": equipamento[8]
        })

    return jsonify(lista)


@app.route("/equipamentos", methods=["POST"])
@token_required
def cadastrar_equipamento():

    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO equipamento
        (marca, modelo, categoria, potencia,
         material, peso, dimensoes, cor)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        dados["marca"],
        dados["modelo"],
        dados["categoria"],
        dados["potencia"],
        dados["material"],
        dados["peso"],
        dados["dimensoes"],
        dados["cor"]
    ))

    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({
        "mensagem": "Equipamento cadastrado"
    })


@app.route("/equipamentos", methods=["DELETE"])
@token_required
def deletar_equipamento():

    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM estoque
        WHERE equipamento_id = %s
    """, (dados["id"],))

    cursor.execute("""
        DELETE FROM equipamento
        WHERE id = %s
    """, (dados["id"],))

    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({
        "mensagem": "Equipamento deletado"
    })


# ============================================================
# ESTOQUE
# ============================================================

@app.route("/estoque", methods=["GET"])
@token_required
def listar_estoque():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, quant_disponivel,
               quant_minima, equipamento_id
        FROM estoque
        ORDER BY id
    """)

    estoques = cursor.fetchall()

    cursor.close()
    conexao.close()

    lista = []

    for estoque in estoques:

        lista.append({
            "id": estoque[0],
            "quant_disponivel": estoque[1],
            "quant_minima": estoque[2],
            "equipamento_id": estoque[3]
        })

    return jsonify(lista)


@app.route("/estoque", methods=["POST"])
@token_required
def cadastrar_estoque():

    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO estoque
        (quant_disponivel, quant_minima, equipamento_id)
        VALUES (%s, %s, %s)
    """, (
        dados["quant_disponivel"],
        dados["quant_minima"],
        dados["equipamento_id"]
    ))

    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({
        "mensagem": "Estoque cadastrado"
    })


@app.route("/estoque", methods=["DELETE"])
@token_required
def deletar_estoque():

    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM registro
        WHERE estoque_id = %s
    """, (dados["id"],))

    cursor.execute("""
        DELETE FROM estoque
        WHERE id = %s
    """, (dados["id"],))

    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({
        "mensagem": "Estoque deletado"
    })


# ============================================================
# REGISTROS
# ============================================================

@app.route("/registros", methods=["GET"])
@token_required
def listar_registros():

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, entrada, saida,
               funcionario_id, estoque_id
        FROM registro
        ORDER BY id
    """)

    registros = cursor.fetchall()

    cursor.close()
    conexao.close()

    lista = []

    for registro in registros:

        lista.append({
            "id": registro[0],
            "entrada": registro[1],
            "saida": registro[2],
            "funcionario_id": registro[3],
            "estoque_id": registro[4]
        })

    return jsonify(lista)


@app.route("/registros", methods=["POST"])
@token_required
def cadastrar_registro():

    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO registro
        (entrada, saida, funcionario_id, estoque_id)
        VALUES (%s, %s, %s, %s)
    """, (
        dados["entrada"],
        dados["saida"],
        dados["funcionario_id"],
        dados["estoque_id"]
    ))

    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({
        "mensagem": "Registro cadastrado"
    })


@app.route("/registros", methods=["DELETE"])
@token_required
def deletar_registro():

    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM registro
        WHERE id = %s
    """, (dados["id"],))

    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({
        "mensagem": "Registro deletado"
    })


# ============================================================
# INICIAR SERVIDOR
# ============================================================

if __name__ == "__main__":
    app.run(debug=True)
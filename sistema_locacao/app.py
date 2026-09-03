from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from database import conectar

app = Flask(__name__)

# Configuração do JWT
app.config["JWT_SECRET_KEY"] = "chave-secreta-sistema-locacao"
jwt = JWTManager(app)

# =========================
# LOGIN
# =========================

@app.route("/login", methods=["POST"])
def login():

    dados = request.get_json()

    if not dados:
        return jsonify({
            "erro": "Envie os dados em JSON."
        }), 400

    email = dados.get("email")
    senha = dados.get("senha")

    # Funcionário de teste
    if email == "admin@admin.com" and senha == "1234":

        token = create_access_token(
            identity="1"
        )

        return jsonify({
            "mensagem": "Login realizado com sucesso!",
            "funcionario_id": 1,
            "nome": "Administrador",
            "access_token": token
        }), 200

    return jsonify({
        "erro": "E-mail ou senha incorretos."
    }), 401


# =========================
# ROTA INICIAL
# =========================

@app.route("/", methods=["GET"])
def index():

    return jsonify({
        "sistema": "Sistema de Locação",
        "status": "API funcionando",
        "mensagem": "Servidor Flask funcionando corretamente."
    }), 200


# =========================
# EQUIPAMENTO
# =========================

@app.route("/equipamento", methods=["GET"])
@jwt_required()
def equipamento():

    try:
        funcionario_id = get_jwt_identity()

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("SELECT * FROM equipamento")

        resultados = cursor.fetchall()

        # Pega os nomes das colunas
        colunas = [descricao[0] for descricao in cursor.description]

        equipamento = []

        for resultado in resultados:
            equipamento = dict(zip(colunas, resultado))
            equipamento.append(equipamento)

        cursor.close()
        conexao.close()

        return jsonify({
            "funcionario_id": funcionario_id,
            "quantidade": len(equipamento),
            "equipamento": equipamento
        }), 200

    except Exception as erro:

        return jsonify({
            "erro": "Erro ao consultar equipamento.",
            "detalhes": str(erro)
        }), 500


# =========================
# TESTE DO JWT
# =========================

@app.route("/teste-jwt", methods=["GET"])
@jwt_required()
def teste_jwt():

    funcionario_id = get_jwt_identity()

    return jsonify({
        "mensagem": "JWT válido!",
        "funcionario_id": funcionario_id
    }), 200


# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":
    app.run(debug=True)
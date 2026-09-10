from flask import Flask, request, jsonify
from database import conectar

app = Flask(__name__)


# LOGIN
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
        return jsonify({
            "mensagem": "Login realizado",
            "id": funcionario[0],
            "nome": funcionario[1],
            "email": funcionario[2]
        })

    return jsonify({
        "mensagem": "Email ou senha incorretos"
    }), 401


# FUNCIONÁRIOS

# FUNCIONÁRIOS- listar
@app.route("/funcionarios", methods=["GET"])
def listar_funcionarios():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome, cpf, email, senha
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
            "email": funcionario[3],
            "senha": funcionario[4]
        })

    return jsonify(lista)

# FUNCIONÁRIOS- CADASTRAR
@app.route("/funcionarios", methods=["POST"])
def cadastrar_funcionario():
    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
            INSERT INTO funcionario (nome, cpf, email, senha)
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

# FUNCIONÁRIOS - DELETAR
@app.route("/funcionarios", methods=["DELETE"])
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

# EQUIPAMENTOS

#EQUIPAMENTOS- LISTAR
@app.route("/equipamentos", methods=["GET"])
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

# EQUIPAMENTOS - CADASTRAR
@app.route("/equipamentos", methods=["POST"])
def cadastrar_equipamento():
    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO equipamento
        (marca, modelo, categoria, potencia, material, peso, dimensoes, cor)
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

# EQUIPAMENTOS - DELETAR
@app.route("/equipamentos", methods=["DELETE"])
def deletar_equipamento():
    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        DELETE FROM estoque
        WHERE equipamento_id = %s
    """, (dados ["id"],))

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

#ESTOQUE
# ESTOQUE - LISTAR
@app.route("/estoque", methods=["GET"])
def listar_estoque():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, quant_disponivel, quant_minima, equipamento_id
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


# ESTOQUE - CADASTRAR
@app.route("/estoque", methods=["POST"])
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

#ESTOQUE - DELETAR
@app.route("/estoque", methods=["DELETE"])
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

#REGISTRO
# REGISTRO - LISTAR
@app.route("/registros", methods=["GET"])
def listar_registros():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, entrada, saida, funcionario_id, estoque_id
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
            "entrada": str(registro[1]),
            "saida": str(registro[2]),
            "funcionario_id": registro[3],
            "estoque_id": registro[4]
        })

    return jsonify(lista)


# REGISTRO - CADASTRAR
@app.route("/registros", methods=["POST"])
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

# REGISTRO - DELETE
@app.route("/registros", methods=["DELETE"])
def deletar_registro():
    dados = request.json

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(""" 
        DELETE FROM registro
        where id = %s
    """, (dados["id"],))

    conexao.commit()

    cursor.close()
    conexao.close()
    
    return jsonify({
        "mensagem": "Registro deletado"
    })

if __name__ == "__main__":
    app.run(debug=True)
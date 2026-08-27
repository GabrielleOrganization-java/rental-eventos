import psycopg2


def conectar():
    conexao = psycopg2.connect(
        host="localhost",
        database="rental_db",
        user="postgres",
        password="ALUNO",
        port="5432"
    )

    return conexao

if __name__ == "__main__":
    try:
        conexao = conectar()
        print("Conexão com o banco realizada com sucesso!")
        conexao.close()
    except Exception as erro:
        print("Erro ao conectar com o banco:")
        print(erro)
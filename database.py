import pg8000

def conectar():
    conexao = pg8000.connect(
        host="localhost",
        port=5432,
        database="rental_db",
        user="postgres",
        password="ALUNO"
    )

    return conexao
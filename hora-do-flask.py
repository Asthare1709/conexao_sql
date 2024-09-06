from flask import Flask, request
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

app = Flask(__name__)

# Carrega as variáveis de ambiente do arquivo .cred (se disponível)
load_dotenv('.cred')

# Configurações para conexão com o banco de dados usando variáveis de ambiente
config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME', 'db_escola'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}

# Função para conectar ao banco de dados
def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None


@app.route('/aluno', methods=['POST'])
def post_aluno(nome, cpf, idade):
    conn = connect_db()  # Conecta ao banco de dados
    aluno_id = None  # ID do aluno inserido
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
            sql = "INSERT INTO tbl_alunos (nome, cpf, idade) VALUES (%s, %s, %s)"  # Comando SQL para inserir um aluno
            values = (nome, cpf, idade)  # Dados a serem inseridos

            # Executa o comando SQL com os valores fornecidos
            print(f"Executando SQL: {sql} com valores: {values}")
            cursor.execute(sql, values)
            
            # Confirma a transação no banco de dados
            conn.commit()

            # Obtém o ID do registro recém-inserido
            aluno_id = cursor.lastrowid
            print(f"Aluno inserido com sucesso! ID: {aluno_id}")
            
        except Error as err:
            # Em caso de erro na inserção, imprime a mensagem de erro
            print(f"Erro ao inserir aluno: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()

    return aluno_id


@app.route('/aluno', methods=['GET'])
def get_lista_alunos():
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "SELECT * FROM tbl_alunos"  # Comando SQL para selecionar todos os alunos

        try:
            # Executa o comando SQL
            cursor.execute(sql)
            # Recupera todos os registros da consulta
            alunos = cursor.fetchall()
            # Itera sobre os resultados e imprime os detalhes de cada aluno
            for aluno in alunos:
                print(f"ID: {aluno[0]}, Nome: {aluno[1]}, CPF: {aluno[2]}, Idade: {aluno[3]}")
        except Error as err:
            # Em caso de erro na busca, imprime a mensagem de erro
            print(f"Erro ao buscar alunos: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()


@app.route('/aluno/<int:id>/', methods=['DELETE'])
def delete_aluno(id):
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "DELETE FROM tbl_alunos WHERE id = %s"  # Comando SQL para deletar um aluno pelo ID

        try:
            # Executa o comando SQL com o ID fornecido
            cursor.execute(sql, (id,))
            # Confirma a transação no banco de dados
            conn.commit()
            # Verifica se alguma linha foi afetada (deletada)
            if cursor.rowcount:
                print("Aluno deletado com sucesso!")
            else:
                print("Aluno não encontrado!")
        except Error as err:
            # Em caso de erro na deleção, imprime a mensagem de erro
            print(f"Erro ao deletar aluno: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()


@app.route('/aluno/<int:id>/', methods=['PUT'])
def put_aluno(nome, cpf, idade, id):
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "UPDATE tbl_alunos SET nome = %s, cpf = %s, idade = %s WHERE id = %s"  # Comando SQL para atualizar o aluno
        values = (nome, cpf, idade, id)  # Dados a serem atualizados

        try:
            # Executa o comando SQL com os valores fornecidos
            cursor.execute(sql, values)
            # Confirma a transação no banco de dados
            conn.commit()
            # Verifica se alguma linha foi afetada (atualizada)
            if cursor.rowcount:
                print("Aluno atualizado com sucesso!")
            else:
                print("Aluno não encontrado!")
        except Error as err:
            # Em caso de erro na atualização, imprime a mensagem de erro
            print(f"Erro ao atualizar aluno: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()


@app.route('/aluno/<int:id>', methods=['GET'])
def get_aluno(aluno_id):
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "SELECT * FROM tbl_alunos WHERE id = %s"  # Comando SQL para buscar um aluno pelo ID

        try:
            # Executa o comando SQL com o ID fornecido
            cursor.execute(sql, (aluno_id,))
            # Recupera o resultado da consulta
            aluno = cursor.fetchone()
            # Verifica se o aluno foi encontrado e imprime seus detalhes
            if aluno:
                print(f"ID: {aluno[0]}, Nome: {aluno[1]}, CPF: {aluno[2]}, Idade: {aluno[3]}")
            else:
                print("Aluno não encontrado!")
        except Error as err:
            # Em caso de erro na busca, imprime a mensagem de erro
            print(f"Erro ao buscar aluno: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()


@app.route('/disciplina/', methods=['POST'])
def post_disciplina(nome, aulas):
    conn = connect_db()  # Conecta ao banco de dados
    id_disciplina = None  # ID do aluno inserido
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
            sql = "INSERT INTO tbl_disciplinas (nome, aulas) VALUES (%s, %s)"  # Comando SQL para inserir um aluno
            values = (nome, aulas)  # Dados a serem inseridos

            # Executa o comando SQL com os valores fornecidos
            print(f"Executando SQL: {sql} com valores: {values}")
            cursor.execute(sql, values)
            
            # Confirma a transação no banco de dados
            conn.commit()

            # Obtém o ID do registro recém-inserido
            aluno_id = cursor.lastrowid
            print(f"Disciplina inserida com sucesso! ID: {id_disciplina}")
            
        except Error as err:
            # Em caso de erro na inserção, imprime a mensagem de erro
            print(f"Erro ao inserir aluno: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()

    return aluno_id


@app.route('/disciplina/', methods=['GET'])
def get_lista_disciplina():
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "SELECT * FROM tbl_disciplinas"  # Comando SQL para selecionar todos os alunos

        try:
            # Executa o comando SQL
            cursor.execute(sql)
            # Recupera todos os registros da consulta
            disciplinas = cursor.fetchall()
            # Itera sobre os resultados e imprime os detalhes de cada aluno
            for disciplina in disciplinas:
                print(f"ID: {disciplina[0]}, Nome: {disciplina[1]}, Aulas: {disciplina[2]}")
        except Error as err:
            # Em caso de erro na busca, imprime a mensagem de erro
            print(f"Erro ao buscar disciplinas: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()


@app.route('/disciplina/<int:id>/', methods=['DELETE'])
def delete_disciplina(id):
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "DELETE FROM tbl_disciplinas WHERE id = %s"  # Comando SQL para deletar um aluno pelo ID

        try:
            # Executa o comando SQL com o ID fornecido
            cursor.execute(sql, (id,))
            # Confirma a transação no banco de dados
            conn.commit()
            # Verifica se alguma linha foi afetada (deletada)
            if cursor.rowcount:
                print("Disciplina deletada com sucesso!")
            else:
                print("Disciplina não encontrada!")
        except Error as err:
            # Em caso de erro na deleção, imprime a mensagem de erro
            print(f"Erro ao deletar disciplina: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()


@app.route('/disciplina/int:id/', methods=['PUT'])
def put_disciplina(nome, aulas, id):
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "UPDATE tbl_disciplinas SET nome = %s, aulas = %s WHERE id = %s"  # Comando SQL para atualizar o aluno
        values = (nome, aulas, id)  # Dados a serem atualizados

        try:
            # Executa o comando SQL com os valores fornecidos
            cursor.execute(sql, values)
            # Confirma a transação no banco de dados
            conn.commit()
            # Verifica se alguma linha foi afetada (atualizada)
            if cursor.rowcount:
                print("Disciplina atualizada com sucesso!")
            else:
                print("Disciplina não encontrada!")
        except Error as err:
            # Em caso de erro na atualização, imprime a mensagem de erro
            print(f"Erro ao atualizar disciplina: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()


@app.route('/disciplina/<int:id>', methods=['GET'])
def get_disciplina(id):
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "SELECT * FROM tbl_disciplinas WHERE id = %s"  # Comando SQL para buscar um aluno pelo ID

        try:
            # Executa o comando SQL com o ID fornecido
            cursor.execute(sql, (id))
            # Recupera o resultado da consulta
            disciplina = cursor.fetchone()
            # Verifica se o aluno foi encontrado e imprime seus detalhes
            if disciplina:
                print(f"ID: {disciplina[0]}, Nome: {disciplina[1]}, Aulas: {disciplina[2]}")
            else:
                print("Disciplina não encontrada!")
        except Error as err:
            # Em caso de erro na busca, imprime a mensagem de erro
            print(f"Erro ao buscar disciplina: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()


@app.route('/matricula', methods=['POST'])
def post_matricula(id_aluno, id_disciplina):
    conn = connect_db()  # Conecta ao banco de dados
    id_matricula = None  # ID do aluno inserido
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
            sql = "INSERT INTO tbl_matriculas (id_aluno, id_disciplina) VALUES (%s, %s)"  # Comando SQL para inserir um aluno
            values = (id_aluno, id_disciplina)  # Dados a serem inseridos

            # Executa o comando SQL com os valores fornecidos
            print(f"Executando SQL: {sql} com valores: {values}")
            cursor.execute(sql, values)
            
            # Confirma a transação no banco de dados
            conn.commit()

            # Obtém o ID do registro recém-inserido
            aluno_id = cursor.lastrowid
            print(f"Matrícula inserida com sucesso! ID: {id_matricula}")
            
        except Error as err:
            # Em caso de erro na inserção, imprime a mensagem de erro
            print(f"Erro ao inserir matrícula: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()

    return aluno_id


@app.route('/matricula/<int:id>/', methods=['DELETE'])
def delete_matricula(id):
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "DELETE FROM tbl_matriculas WHERE id = %s"  # Comando SQL para deletar um aluno pelo ID

        try:
            # Executa o comando SQL com o ID fornecido
            cursor.execute(sql, (id))
            # Confirma a transação no banco de dados
            conn.commit()
            # Verifica se alguma linha foi afetada (deletada)
            if cursor.rowcount:
                print("Matrícula deletada com sucesso!")
            else:
                print("Matrícula não encontrada!")
        except Error as err:
            # Em caso de erro na deleção, imprime a mensagem de erro
            print(f"Erro ao deletar matrícula: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()


@app.route('/matricula/<int:id>/', methods=['GET'])
def get_matricula(id):
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "SELECT * FROM tbl_matriculas WHERE id = %s"  # Comando SQL para buscar um aluno pelo ID

        try:
            # Executa o comando SQL com o ID fornecido
            cursor.execute(sql, (id))
            # Recupera o resultado da consulta
            matricula = cursor.fetchone()
            # Verifica se o aluno foi encontrado e imprime seus detalhes
            if matricula:
                print(f"ID: {matricula[0]}, ID_Aluno: {matricula[1]}, ID_Disciplina: {matricula[2]}")
            else:
                print("Matrícula não encontrada!")
        except Error as err:
            # Em caso de erro na busca, imprime a mensagem de erro
            print(f"Erro ao buscar matrícula: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()


if __name__ == '__main__':
    app.run(debug=True)
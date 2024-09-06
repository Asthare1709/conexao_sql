import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

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
    


# Função para inserir um novo aluno
def inserir_aluno(nome, cpf, idade):
    """Insere um novo aluno na tabela tbl_alunos e retorna o ID do aluno inserido."""
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


# Função para buscar um aluno por ID
def buscar_aluno_por_id(aluno_id):
    """Busca um aluno específico na tabela tbl_alunos pelo seu ID."""
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

# Função para buscar todos os alunos
def buscar_todos_alunos():
    """Busca e exibe todos os alunos da tabela tbl_alunos."""
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



# Função para atualizar um aluno
def atualizar_aluno(aluno_id, nome, cpf, idade):
    """Atualiza os dados de um aluno existente na tabela tbl_alunos."""
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "UPDATE tbl_alunos SET nome = %s, cpf = %s, idade = %s WHERE id = %s"  # Comando SQL para atualizar o aluno
        values = (nome, cpf, idade, aluno_id)  # Dados a serem atualizados

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



# Função para deletar um aluno por ID
def deletar_aluno(aluno_id):
    """Deleta um aluno da tabela tbl_alunos pelo seu ID."""
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "DELETE FROM tbl_alunos WHERE id = %s"  # Comando SQL para deletar um aluno pelo ID

        try:
            # Executa o comando SQL com o ID fornecido
            cursor.execute(sql, (aluno_id,))
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

# Inserindo um novo aluno
inserir_aluno("Gustavo Santana", "22222222222", 19)

# Buscando todos os alunos
# buscar_todos_alunos()

# Buscando um aluno por ID
# buscar_aluno_por_id(1)

# Atualizando um aluno
# atualizar_aluno(1, "João da Silva", "12345678111", 21)

# Deletando um aluno
# deletar_aluno(1)
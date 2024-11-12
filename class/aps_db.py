import re
import mysql.connector

class DbManager:
    def __init__(self):
        self.num_para_letra = { "0": "O",
                                "1": "I", 
                                "2": "Z",
                                "3": "B",
                                "4": "A",
                                "5": "S",
                                "6": "G",
                                "7": "J",
                                "8": "D" }

        self.letra_para_num = { "O": "0",
                                "Q": "0",
                                "I": "1",
                                "Z": "2",
                                "B": "3",
                                "A": "4",
                                "S": "5",
                                "G": "6",
                                "J": "7",
                                "D": "8" }

    def tratamento_string(self, s: str):
        # Remove espaço caracteres especiais, com exceção do /
        s = re.sub(r'[^a-zA-Z0-9\/]', '', s)

        # Verifica tamanho mínimo
        if not len(s) == 7:
            return ""

        # Substitui "/" por "I"
        s = s.replace("/", "I")

        s = s.upper()
        primeiros_3 = s[:3]
        ultimos_4 = s[3:7]

        # Verifica se os 3 primeiros caracteres são letras e troca se necessário
        lista_3 = list(primeiros_3)
        for i in range(3):
            if not lista_3[i].isalpha():
                if lista_3[i] in self.num_para_letra:
                    lista_3[i] = self.num_para_letra[lista_3[i]]
                else:
                    lista_3[i] = ""
        primeiros_3 = "".join(lista_3)

        # Verifica se os caracteres na posição 4, 6 e 7 são números
        lista_4 = list(ultimos_4)
        for i in range(4):
            if (not i == 1) and (not ultimos_4[i].isdigit()):
                if lista_4[i] in self.letra_para_num:
                    lista_4[i] = self.letra_para_num[lista_4[i]]
                else:
                    lista_4[i] = ""
        ultimos_4 = "".join(lista_4)

        string_final = primeiros_3 + ultimos_4

        if len(string_final) == 7:
            return string_final
        else:
            return ""
    
    def busca_no_banco(self, placa: str):
        placa_tratada = self.tratamento_string(placa)

        if not placa_tratada:
            return None  # Se a placa não for válida, retorna None

        try:
            # Conexão com o banco de dados
            conexao = mysql.connector.connect(
                host="local_host",         # Endereço do servidor (exemplo: 'localhost')
                user="aps_db_user",        # Usuário do banco de dados
                password="aps_db_password",    # Senha do banco de dados
                database="aps_database"     # Nome do banco de dados
            )

            # Criação do cursor para executar consultas
            cursor = conexao.cursor()

            # Consulta para buscar a placa tratada
            consulta = "SELECT * FROM aps_veiculos WHERE placa LIKE %s"
            parametro = f"%{placa_tratada}%"
            cursor.execute(consulta, (parametro,))

            # Obtenção dos resultados
            resultados = cursor.fetchall()
            
            # Verifica se há resultados
            if resultados:
                return resultados
            else:
                return None  # Retorna None se não houver resultados

        except mysql.connector.Error as erro:
            print(f"Erro ao conectar ao banco de dados: {erro}")
            return None

        finally:
            # Fecha a conexão com o banco de dados
            if conexao.is_connected():
                cursor.close()
                conexao.close()

# Exemplo de uso
db_manager = DbManager()

# Teste com uma placa válida
placa_encontrada = db_manager.busca_no_banco("OIZB456")
if placa_encontrada:
    print("Placa encontrada:", placa_encontrada)
else:
    print("Placa não encontrada.")

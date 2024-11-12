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

        try:
            # Conexão com o banco de dados
            self.conexao = mysql.connector.connect(
                host="localhost",         # Endereço do servidor (exemplo: 'localhost')
                user="aps_db_user",        # Usuário do banco de dados
                password="aps_db_password",    # Senha do banco de dados
                database="aps_database",     # Nome do banco de dados
                charset="utf8mb3"
            )

            # Criação do cursor para executar consultas
            self.cursor = self.conexao.cursor()

        except mysql.connector.Error as erro:
            print(f"Erro ao conectar ao banco de dados: {erro}")
            exit()


    def tratamento_string(self, s: str):
        # Remove espaço caracteres especiais, com exceção do / e |
        s = re.sub(r'[^a-zA-Z0-9\/\|]', '', s)

        # Verifica tamanho mínimo
        if not len(s) == 7:
            return ""

        # Substitui "/" e "|" por "I"
        s = s.replace("/", "I").replace("|","I")

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

        # Consulta para buscar a placa tratada
        consulta = "SELECT * FROM aps_veiculos WHERE placa = %s"
        self.cursor.execute(consulta, (placa_tratada,))

        # Obtenção dos resultados
        resultados = self.cursor.fetchall()
        
        # Verifica se há resultados
        if resultados:
            return resultados
        else:
            return None  # Retorna None se não houver resultados

    def encerra_conexao(self):
        if self.conexao.is_connected():
                self.cursor.close()
                self.conexao.close()
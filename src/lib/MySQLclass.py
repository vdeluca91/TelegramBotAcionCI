## prima installa il modulo mysql-connector-python da terminale eg GITBash
#pip install mysql-connector-python

import mysql.connector
from mysql.connector import Error

class MySQLDatabase:
    def __init__(self, config_file_path='src\\lib\\config.py'):
        self.config_file_path = config_file_path
        self.connection = None

    def read_config(self):
        try:
            # Importa il modulo come un modulo Python
            config = {}
            with open(self.config_file_path, 'r') as file:
                exec(file.read(), config)
            return config
        except FileNotFoundError:
            raise Exception("File di configurazione non trovato.")
        except Exception as e:
            raise Exception(f"Errore nel parsing del file di configurazione: {e}")

    def connect(self):
        try:
            config = self.read_config()
            self.connection = mysql.connector.connect(**config['DB_CONFIG'])
            print("Connessione al database avvenuta con successo.")
        except Error as e:
            print(f"Errore durante la connessione al database: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Connessione al database chiusa.")

    # def execute_query(self, query, values=None):
    #     cursor = self.connection.cursor()
    #     try:
    #         cursor.execute(query, values)
    #         self.connection.commit()
    #         print("Query eseguita con successo.")
    #     except Error as e:
    #         print(f"Errore durante l'esecuzione della query: {e}")
    #     finally:
    #         cursor.close()

    def execute_query(self, query, values=None, multi=False):
        cursor = self.connection.cursor()
        try:
            if multi:
                cursor.executemany(query, values)
            else:
                cursor.execute(query, values)
                
            self.connection.commit()
            print("Query eseguita con successo.")
        except Error as e:
            print(f"Errore durante l'esecuzione della query: {e}")
        finally:
            cursor.close()

    def select_query(self, query, values=None):
        cursor = self.connection.cursor(dictionary=True)
        try:
            cursor.execute(query, values)
            result = cursor.fetchall()
            print("Query eseguita con successo.")
            return result
        except Error as e:
            print(f"Errore durante l'esecuzione della query: {e}")
        finally:
            cursor.close()

# Esempio di utilizzo della classe
# if __name__ == "__main__":
#     db = MySQLDatabase()

#     # Connessione al database
#     db.connect()

#     # Esempio di esecuzione di una query
#     create_table_query = """
#     CREATE TABLE IF NOT EXISTS example_table (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         name VARCHAR(255) NOT NULL
#     )
#     """
#     db.execute_query(create_table_query)

#     # Esempio di inserimento di dati
#     insert_data_query = "INSERT INTO example_table (name) VALUES (%s)"
#     data_to_insert = ("John Doe",)
#     db.execute_query(insert_data_query, data_to_insert)

#     # Esempio di selezione di dati
#     select_data_query = "SELECT * FROM example_table"
#     results = db.select_query(select_data_query)
#     print("Risultati della query di selezione:")
#     for row in results:
#         print(row)

#     # Disconnessione dal database
#     db.disconnect()
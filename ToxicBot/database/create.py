import psycopg2
from configparser import RawConfigParser

config = RawConfigParser()
config.read("secret.ini")

USER = config.get("DATABASE", "USER")
PASSWORD = config.get("DATABASE", "PASSWORD")
HOST = config.get("DATABASE", "HOST")
PORT = config.get("DATABASE", "PORT")
DATABASE = config.get("DATABASE", "DATABASE")


class CreateTables:
    def __init__(self):
        self.connection = None
        self.connect()

    def __del__(self):
        if self.connection:
            self.connection.close()

    def connect(self):
        try:
            connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
            cursor = connection.cursor()
            print(connection.get_dsn_parameters(), "\n")
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You are connected to - ", record, "\n")
            self.connection = connection
            cursor.close()
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def createToxicDBSchema(self):

        if not self.connection:
            raise ValueError("Connection does not exist")

        create_table_query = """
            CREATE TABLE IF NOT EXISTS tblToxicCounts(
                Server_Id TEXT NOT NULL,
                User_Id TEXT NOT NULL,
                Toxic_Count SMALLINT NOT NULL,
                timestamp timestamp default current_timestamp,
                UNIQUE (Server_Id, User_Id)
            );"""

        cursor = self.connection.cursor()
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def createServerConfigSchema(self):
        if not self.connection:
            raise ValueError("Connection does not exist")

        create_table_query = """
            CREATE TABLE IF NOT EXISTS tblServerConfig(
                Server_Id TEXT NOT NULL,
                Toxic_Limit SMALLINT NOT NULL DEFAULT 20,
                Toxic_Time_Threshold SMALLINT NOT NULL DEFAULT 14,
                Server_Owner_Id TEXT NOT NULL,
                timestamp timestamp default current_timestamp,
                UNIQUE (Server_Id)
            );"""

        cursor = self.connection.cursor()
        cursor.execute(create_table_query)
        self.connection.commit()
        cursor.close()

    def createSchema(self):
        self.createToxicDBSchema()
        self.createServerConfigSchema()

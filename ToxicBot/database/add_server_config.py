import psycopg2
import datetime
from configparser import RawConfigParser
from discord.ext.commands import NotOwner

config = RawConfigParser()
config.read('secret.ini')

USER = config.get('DATABASE', 'USER')
PASSWORD = config.get('DATABASE', 'PASSWORD')
HOST = config.get('DATABASE', 'HOST')
PORT = config.get('DATABASE', 'PORT')
DATABASE = config.get('DATABASE', 'DATABASE')


class ServerConfig:
    def __init__(self):
        self.connection = None
        self.connect()

    def __del__(self):
        if self.connection:
            self.connection.close()

    def connect(self):
        try:
            connection = psycopg2.connect(
                user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
            self.connection = connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def getConfig(self, server_id):
        if not self.connection:
            raise ValueError("Connection does not exist")

        sql_select_query = "SELECT * from tblServerConfig WHERE Server_Id = %s LIMIT 1"
        cursor = self.connection.cursor()
        cursor.execute(sql_select_query, (server_id,))
        records = cursor.fetchall()
        cursor.close()
        return records

    def getConfigFromUser(self, user_id, server_id=None):
        if not self.connection:
            raise ValueError("Connection does not exist")
        sql_select_query = "SELECT * from tblServerConfig WHERE Server_Owner_Id = %s"
        cursor = self.connection.cursor()
        cursor.execute(sql_select_query, (user_id,))
        records = cursor.fetchall()
        cursor.close()
        if len(records) == 0:
            raise NotOwner("You are not the admin of any server")
        elif len(records) == 1:
            return records[0]
        else:
            raise AttributeError("Author admin of multiple servers")

    def createServerConfig(self, server_id, server_owner_id, count=20, threshold=14):

        if not self.connection:
            raise ValueError("Connection does not exist")
        records = self.getConfig(server_id)
        if len(records) == 0:
            sql_insert_query = """ INSERT INTO tblServerConfig (Server_Id, Toxic_Limit, Toxic_Time_Threshold, Server_Owner_Id)
                            VALUES (%s,%s,%s,%s) """

            cursor = self.connection.cursor()
            cursor.execute(sql_insert_query, (server_id,
                                              count, threshold, server_owner_id))
        self.connection.commit()
        cursor.close()

    def modifyServerConfig(self, server_owner_id, server_id=None, count=None, threshold=None):
        record = self.getConfigFromUser(server_owner_id)
        if record[3] != server_owner_id:
            raise NotOwner("You are not the admin of this server")
        SERVER_ID = record[0]
        if count is None:
            count = record[1]
        if threshold is None:
            threshold = record[2]
        
        sql_update_query = """ UPDATE tblServerConfig 
            SET Toxic_Limit = %s,
            Toxic_Time_Threshold = %s
            WHERE Server_Id = %s
            """
        cursor = self.connection.cursor()
        cursor.execute(sql_update_query, (count, threshold, SERVER_ID))
        self.connection.commit()
        cursor.close()
        return SERVER_ID  # Returns the server id


if __name__ == "__main__":
    server_config = ServerConfig()
    server_config.modifyServerConfig('123', 1, 2)

import psycopg2
from configparser import RawConfigParser
from discord.ext.commands import NotOwner

config = RawConfigParser()
config.read("secret.ini")

USER = config.get("DATABASE", "USER")
PASSWORD = config.get("DATABASE", "PASSWORD")
HOST = config.get("DATABASE", "HOST")
PORT = config.get("DATABASE", "PORT")
DATABASE = config.get("DATABASE", "DATABASE")


class ServerConfig:
    def __init__(self):
        self.connection = None
        self.connect()

    def __del__(self):  # Closes the connection
        if self.connection:
            self.connection.close()

    def connect(self):
        try:  # Connect to the database instance
            connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
            self.connection = connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    # Get the server configuration for a particular server
    def getConfig(self, server_id):
        if not self.connection:
            raise ValueError("Connection does not exist")

        sql_select_query = "SELECT * from tblServerConfig WHERE Server_Id = %s LIMIT 1"
        cursor = self.connection.cursor()
        cursor.execute(sql_select_query, (server_id,))
        records = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return records

    # Similar to getConfig however queries based on user_id instead of server_id
    def getConfigFromUser(self, user_id, server_id=None):
        if not self.connection:
            raise ValueError("Connection does not exist")
        cursor = self.connection.cursor()
        if server_id is not None:  # If server_id is passed as well then use it
            sql_select_query = "SELECT * from tblServerConfig WHERE Server_Owner_Id = %s AND Server_Id = %s"
            cursor.execute(sql_select_query, (user_id, server_id))
        else:
            sql_select_query = "SELECT * from tblServerConfig WHERE Server_Owner_Id = %s"
            cursor.execute(sql_select_query, (user_id,))
        records = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        if len(records) == 0:  # If no records are returned, then issue an error
            raise NotOwner("You are not the admin of any server")
        elif len(records) == 1:
            return records[0]  # If only 1 record is present, reurn it
        else:
            # If multiple records are present, then raise an Error
            raise AttributeError("Author admin of multiple servers")

    # When a bot joins a server, create a configuration for it
    def createServerConfig(self, server_id, server_owner_id, count=20, threshold=14):

        if not self.connection:
            raise ValueError("Connection does not exist")
        records = self.getConfig(server_id)
        if len(records) == 0:  # If record already exists, no need to create a new one
            sql_insert_query = """ INSERT INTO tblServerConfig (Server_Id, Toxic_Limit, Toxic_Time_Threshold, Server_Owner_Id)
                            VALUES (%s,%s,%s,%s) """

            cursor = self.connection.cursor()
            cursor.execute(sql_insert_query, (server_id, count, threshold, server_owner_id))
        self.connection.commit()
        cursor.close()

    # Method called to modify the server config
    def modifyServerConfig(self, server_owner_id, server_id=None, count=None, threshold=None):
        record = self.getConfigFromUser(server_owner_id, server_id)  # Get the server record
        if record[3] != server_owner_id:  # If user is not an admin of the server, raise an error
            raise NotOwner("You are not the admin of this server")
        SERVER_ID = record[0]
        if count is None:  # If values are not provided, then use the value in the record
            count = record[1]
        if threshold is None:
            threshold = record[2]

        # Update SQL query
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

    # Get all the servers for a particular user
    def getAllServers(self, server_owner_id):
        if not self.connection:
            raise ValueError("Connection does not exist")
        sql_select_query = "SELECT * from tblServerConfig WHERE Server_Owner_Id = %s"
        cursor = self.connection.cursor()
        cursor.execute(sql_select_query, (server_owner_id,))
        records = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return records


if __name__ == "__main__":
    server_config = ServerConfig()
    server_config.modifyServerConfig("123", 1, 2)

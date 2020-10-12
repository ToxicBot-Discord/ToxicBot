import psycopg2
import datetime
from configparser import RawConfigParser

config = RawConfigParser()
config.read("secret.ini")

USER = config.get("DATABASE", "USER")
PASSWORD = config.get("DATABASE", "PASSWORD")
HOST = config.get("DATABASE", "HOST")
PORT = config.get("DATABASE", "PORT")
DATABASE = config.get("DATABASE", "DATABASE")


class AddToxicCount:
    def __init__(self):
        self.connection = None
        self.connect()

    def __del__(self):
        if self.connection:
            self.connection.close()

    def connect(self):
        try:
            connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
            self.connection = connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def deleteRecord(self, server_id, user_id):
        if not self.connection:
            raise ValueError("Connection does not exist")
        sql_delete_query = """DELETE from tblToxicCounts WHERE Server_Id = %s AND User_Id = %s"""
        cursor = self.connection.cursor()
        cursor.execute(sql_delete_query, (server_id, user_id))
        self.connection.commit()
        cursor.close()

    def checkIfExists(self, server_id, user_id) -> bool:
        if not self.connection:
            raise ValueError("Connection does not exist")

        sql_select_query = "SELECT * from tblToxicCounts WHERE Server_Id = %s AND User_Id = %s LIMIT 1"
        cursor = self.connection.cursor()
        cursor.execute(sql_select_query, (server_id, user_id))
        records = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        if len(records) == 0:
            return False
        record = records[0]
        timestamp = record[3]
        # Delete toxic count for a certain user if it
        # has exceeded a certain time threshold
        current_time = datetime.datetime.now()
        difference_in_time = current_time - timestamp
        difference_in_time_in_s = difference_in_time.total_seconds()
        days = divmod(difference_in_time_in_s, 86400)[0]
        sql_select_config_query = "SELECT * from tblServerConfig WHERE Server_Id = %s LIMIT 1"
        cursor = self.connection.cursor()
        cursor.execute(sql_select_config_query, (server_id,))
        self.connection.commit()
        config_records = cursor.fetchall()
        config_days = config_records[0][2]
        if days > config_days:
            self.deleteRecord(server_id, user_id)
            return False
        return True

    def addToxicCount(self, server_id, user_id):

        if not self.connection:
            raise ValueError("Connection does not exist")

        if self.checkIfExists(server_id, user_id):
            sql_update_query = """ UPDATE tblToxicCounts
                SET Toxic_Count = Toxic_Count + 1
                WHERE Server_Id = %s AND User_Id = %s
                """
            cursor = self.connection.cursor()
            cursor.execute(sql_update_query, (server_id, user_id))
        else:
            sql_insert_query = """ INSERT INTO tblToxicCounts (Server_Id, User_Id, Toxic_Count)
                            VALUES (%s,%s,%s) """

            cursor = self.connection.cursor()
            cursor.execute(sql_insert_query, (server_id, user_id, 1))
        self.connection.commit()
        sql_select_config_query = "SELECT tblToxicCounts.Toxic_Count, tblServerConfig.Toxic_Limit \
            FROM tblToxicCounts JOIN tblServerConfig \
            ON \
            tblToxicCounts.Server_Id = %s AND \
            tblServerConfig.Server_Id = %s AND \
            tblToxicCounts.User_Id = %s \
            LIMIT 1"
        cursor.execute(sql_select_config_query, (server_id, server_id, user_id))
        records = cursor.fetchall()
        record = records[0]
        toxic_count = record[0]
        toxic_threshold = record[1]
        if toxic_count > toxic_threshold:
            sql_delete_query = "DELETE from tblToxicCounts WHERE Server_Id = %s AND User_Id = %s"
            cursor = self.connection.cursor()
            cursor.execute(sql_delete_query, (server_id, user_id))
            self.connection.commit()
            raise AttributeError("Ban User")
        self.connection.commit()
        cursor.close()

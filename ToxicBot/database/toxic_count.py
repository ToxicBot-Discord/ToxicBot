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

"""
ToxicCount is responsible for ensuring that any toxic messages is added to the database.
This information is later used to determine whether we need to ban the user.

Any record can be identified uniquely using the server_id and user_id.
"""


class ToxicCount:
    def __init__(self):
        self.connection = None
        self.connect()

    def __del__(self):  # Closes the connection
        if self.connection:
            self.connection.close()

    def connect(self):
        try:
            # Connect to the database instance
            connection = psycopg2.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE)
            self.connection = connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    # Utility function to remove history for an user
    def removeHistory(self, server_id, user_id):
        if not self.connection:  # Check if connection has been established
            raise ValueError("Connection does not exist")
        # Update toxic count to 0
        sql_update_query = """UPDATE tblToxicCounts SET Toxic_Count = 0 WHERE Server_Id = %s AND User_Id = %s"""
        cursor = self.connection.cursor()
        cursor.execute(sql_update_query, (server_id, user_id))
        self.connection.commit()
        cursor.close()

    # Check if any record for the particular user in that server exists
    def checkIfExists(self, server_id, user_id) -> bool:
        if not self.connection:
            raise ValueError("Connection does not exist")

        sql_select_query = "SELECT * from tblToxicCounts WHERE Server_Id = %s AND User_Id = %s LIMIT 1"
        cursor = self.connection.cursor()
        cursor.execute(sql_select_query, (server_id, user_id))
        records = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        if len(records) == 0:  # If no record exists, return False ie. does not exist
            return False
        record = records[0]
        timestamp = record[3]  # Timestamp of last toxic messages
        # Delete toxic count for a certain user if it
        # has exceeded a certain time threshold
        current_time = datetime.datetime.now()
        difference_in_time = current_time - timestamp
        difference_in_time_in_s = difference_in_time.total_seconds()
        days = divmod(difference_in_time_in_s, 86400)[0]  # Number of days elapsed since last toxic comment
        sql_select_config_query = (
            "SELECT * from tblServerConfig WHERE Server_Id = %s LIMIT 1"  # Get the server configuration
        )
        cursor = self.connection.cursor()
        cursor.execute(sql_select_config_query, (server_id,))
        self.connection.commit()
        config_records = cursor.fetchall()
        config_days = config_records[0][2]  # Threshold set by the server admin
        if days > config_days:  # If it exceeds the threshold, delete it
            self.removeHistory(server_id, user_id)
        return True

    # Function called when the bot encounters a toxic message
    def addToxicCount(self, server_id, user_id):

        if not self.connection:
            raise ValueError("Connection does not exist")
        # If there is a pre-existing record for an user then update toxic count value
        if self.checkIfExists(server_id, user_id):
            sql_update_query = """ UPDATE tblToxicCounts
                SET Toxic_Count = Toxic_Count + 1
                WHERE Server_Id = %s AND User_Id = %s
                """
            cursor = self.connection.cursor()
            cursor.execute(sql_update_query, (server_id, user_id))
        else:  # If record does not exist create it
            sql_insert_query = """ INSERT INTO tblToxicCounts (Server_Id, User_Id, Toxic_Count)
                            VALUES (%s,%s,%s) """

            cursor = self.connection.cursor()
            cursor.execute(sql_insert_query, (server_id, user_id, 1))
        self.connection.commit()  # Get the toxic_count for the user and toxic limit for the server
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
        if toxic_count > toxic_threshold:  # If it has exceeded threshold set by admin delete user record
            sql_delete_query = "DELETE from tblToxicCounts WHERE Server_Id = %s AND User_Id = %s"
            cursor = self.connection.cursor()
            cursor.execute(sql_delete_query, (server_id, user_id))
            self.connection.commit()
            raise AttributeError("Ban User")  # Raise an error to request the ban of the user
        self.connection.commit()
        cursor.close()

    # This method gets the top n users having the most toxic comments for that server
    def getTopRecords(self, server_id, top):
        if not self.connection:
            raise ValueError("Connection does not exist")
        cursor = self.connection.cursor()
        # Get the top n records for that server
        sql_select_query = """
        SELECT * from tblToxicCounts WHERE Server_Id = %s ORDER BY Toxic_Count DESC LIMIT %s
        """
        cursor.execute(sql_select_query, (server_id, top))
        self.connection.commit()
        # Return all the top n records
        records = cursor.fetchall()
        return records

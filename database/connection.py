import mysql.connector


def get_connection():

    connection = mysql.connector.connect(
        host="LAPTOP-HNSCCGH6",
        port=3306,
        user="root",
        password="",
        database="ai_krushi_mitra"
    )

    return connection
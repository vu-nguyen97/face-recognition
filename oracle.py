import cx_Oracle
import sys
import os


# lib_dir="/root/instantclient_23_4"
# lib_dir=r"C:\oracle\instantclient_21_13"
# cx_Oracle.init_oracle_client(lib_dir="/root/instantclient_23_4")


connection = cx_Oracle.connect(user="FACE_OWNER", password="ftp2023", dsn="192.168.1.251:1521/orcl")

# Check connection state
if connection.ping():
    print("Connection is OK")
else:
    print("Connection is not OK")

# Close connection
connection.close()

# print(cx_Oracle.version)
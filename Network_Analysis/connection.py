import psycopg2
import pandas as pd

params = {
    'username': '',
    'password': '',
    'host': 'redshift-bi.csrthmbsnci7.ca-central-1.redshift.amazonaws.com',
    'port': ,
    'database': ''
}

# Constructing the connection string
connection_string = "dbname='{database}' user='{username}' host='{host}' password='{password}' port={port}".format(**params)

# Establishing the connection
conn = psycopg2.connect(connection_string)

# SQL query
network_in = '''
SELECT * FROM network_analysis
'''

# Reading SQL query into DataFrame
df_network = pd.read_sql_query(network_in, conn)

# Closing the connection
conn.close()

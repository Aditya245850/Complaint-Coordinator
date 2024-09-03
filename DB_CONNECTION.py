import psycopg2
DB_HOST = ''
DB_NAME = ''
DB_USER = ''
DB_PASS = ''
DB_PORT = ''

def get_db_connection():
    conn = psycopg2.connect(
        host = DB_HOST,
        database = DB_NAME,
        user = DB_USER,
        password = DB_PASS,
        port = DB_PORT,
        sslmode = "require",
        sslrootcert = "path_to_pem_file"
    )
    return conn

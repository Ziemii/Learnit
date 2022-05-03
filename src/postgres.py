import psycopg2

with psycopg2.connect(user="User",password="password",host="localhost",port="5432",database="mydb") as connection:
    cursor = connection.cursor()
    # Print PostgreSQL details
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")
    # Executing a SQL query
    cursor.execute("SELECT * FROM users;")
    # Fetch result
    record = cursor.fetchall()
    print("Users ", record, "\n")



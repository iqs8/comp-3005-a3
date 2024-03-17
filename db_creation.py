import psycopg2
from psycopg2 import sql


# Enter database credentials here
dbname = 'postgres'
user = 'postgres'
password = 'TitanFries15'
host = 'localhost'
port = 5433

try:
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    conn.autocommit = True
    cursor = conn.cursor()

    # Terminate all connections to 'assignment3' database
    cursor.execute(sql.SQL("""
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = %s AND pid <> pg_backend_pid();
    """), ['assignment3'])
    print("All connections to 'assignment3' terminated.")

    # Drop 'assignment3' database if it exists
    cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {};").format(sql.Identifier('assignment3')))
    print("Database 'assignment3' dropped if existed.")

    # Create 'assignment3' database
    cursor.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier('assignment3')))
    print("Database 'assignment3' created.")

    # Close the connection before reconnecting to the new database
    cursor.close()
    conn.close()

    # Establish a new connection to the 'assignment3' database
    conn = psycopg2.connect(dbname='assignment3', user=user, password=password, host=host, port=port)
    conn.autocommit = True  # Set autocommit to True again for the new connection
    cursor = conn.cursor()

    # Create 'students' table
    cursor.execute("""
        CREATE TABLE students (
            student_id SERIAL PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            enrollment_date DATE
        );
    """)
    print("Table 'students' created.")

    # Insert data into 'students' table
    cursor.execute("""
        INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
        ('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
        ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
        ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');
    """)
    print("Data inserted into 'students' table.")

    cursor.close()
    conn.close()
except Exception as error:
    print("ERROR:", error)

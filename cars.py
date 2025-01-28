import psycopg2
import psycopg2.extras

database_name = "anindita"
user_name = "postgres"
password = "postgres"
host_ip = "localhost"
host_port =5432


my_con = psycopg2.connect(
            database = database_name,
            user = user_name,
            password = password,
            host = host_ip,
            port = host_port
)

my_con.autocommit = True
cursor = my_con.cursor()

query = "CREATE DATABASE car_db"
cursor.execute(query)
database_name = "car_db"
user_name = "postgres"
password = "postgres"
host_ip = "localhost"
host_port =5432

my_db_con = psycopg2.connect(
            database = database_name,
            user = user_name,
            password = password,
            host = host_ip,
            port = host_port
)
create_table_query = """
CREATE TABLE IF NOT EXISTS cars (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL,
model INTEGER,
number TEXT,
color TEXT,
company TEXT
);
"""
my_db_con.autocommit = True
cursor = my_db_con.cursor()
cursor.execute(create_table_query)
cars = [
    ("Aqua", 2009, "ABC123", "Red", "Toyota"),
    ("700s", 2015, "XXXX22", "Black", "BMW"),
    ("Vezel", 2018, "XXX111", "White", "Honda"),
    ("200C", 2001, "MMMM11", "Black", "Mercedez"),
    ("Vitz", 2010, "XXXX", "Red", "Toyota"),
]

car_records = ", ".join(["%s"] * len(cars))

insert_query = (
    f"INSERT INTO cars (name, model, number, color, company) VALUES {car_records}"
)
cursor.execute(insert_query, cars)


# delete records.

delete_car_records = "DELETE FROM cars WHERE color = 'Red'"

cursor.execute(delete_car_records)





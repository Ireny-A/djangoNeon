import psycopg2

# подключение к базе данных
conn = psycopg2.connect(
    dbname="neonbase",  # замените на имя вашей базы данных
    user="postgres",  # замените на имя своего пользователя
    password="uytii1010",  # ваш пароль
    host="localhost",
    port="5432"
)

# курсор
cursor = conn.cursor()

# получение списка таблиц
table_query = "SELECT tablename FROM pg_tables WHERE schemaname='public'"
cursor.execute(table_query)
tables = cursor.fetchall()

# вывод списка таблиц
print("Список таблиц:")
for table in tables:
    print(table[0])

# закрытие курсора и соединения с базой данных
cursor.close()
conn.close()

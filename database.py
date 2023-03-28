import psycopg2
import csv


def get_connection():
    conn = psycopg2.connect(database='f26bot', user='f26bot', password='f26bot', host='localhost', port=5432)

    return conn


def create_table_profile():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS profile(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(300),
    last_name VARCHAR(300),
    username VARCHAR(200), 
    telegram_id BIGINT
    )
    """)

    conn.commit()
    conn.close()


def update_profile_contact(user_id, phone):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(f"""
    Update profile SET phone='{phone}'
    where telegram_id = {user_id}
    """)

    conn.commit()
    conn.close()


def update_profile_location(user_id, lat, long):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(f"""
    Update profile SET latitude={lat}, longitude={long}
    where telegram_id = {user_id}
    """)

    conn.commit()
    conn.close()


def get_user_data_with_telegram_id(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from profile
    where telegram_id = {telegram_id}
    """)

    data = cursor.fetchall()
    return data


def alter_table_profile():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        AlTER TABLE profile 
        ADD COLUMN  phone VARCHAR(12);
        """)
    except Exception as e:
        pass

    conn.commit()
    conn.close()


def modify_table_profile_phone():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        AlTER TABLE profile 
        ALTER COLUMN phone TYPE VARCHAR(30);
        """)

    conn.commit()
    conn.close()


def add_table_profile_location():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            AlTER TABLE profile 
            ADD COLUMN  latitude decimal,
            ADD COLUMN  longitude decimal;
            """)
    except Exception as e:
        print(e)
        pass

    conn.commit()
    conn.close()


def create_table_region():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS region(
        id SERIAL PRIMARY KEY,
        title VARCHAR(100)
        )
        """)

    conn.commit()
    conn.close()


def create_table_district():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS district(
        id SERIAL PRIMARY KEY,
        region_id INT,
        title VARCHAR(100)
        )
        """)

    conn.commit()
    conn.close()


def check_user_in_table(telegram_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from profile
    where telegram_id={telegram_id}
    """)
    data = cursor.fetchall()
    if data:
        return True
    return False


def get_region_by_title(title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from region
    where title = %s
    """, (title,))
    data = cursor.fetchall()
    return data


def get_region_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from region
    where id = %s
    """, (id,))
    data = cursor.fetchall()
    return data


def get_district_by_title(title):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from district
    where title = %s
    """, (title,))
    data = cursor.fetchall()
    return data


def get_district_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from district
    where id = %s
    """, (id,))
    data = cursor.fetchall()
    return data


def districts_by_region_id(region_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
    select * from district
    where region_id = {region_id}
    """)
    data = cursor.fetchall()
    return data


def insert_user_to_table(first_name, last_name, username, telegram_id):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    insert into profile (first_name, last_name, username, telegram_id)
    values (%s, %s, %s, %s)
    """, (first_name, last_name, username, telegram_id))
    conn.commit()
    conn.close()


def insert_region_to_table(id, title):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    insert into region (id, title)
    values (%s, %s)
    """, (id, title))
    conn.commit()
    conn.close()


def insert_district_to_table(region_id, title):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    insert into district (region_id, title)
    values (%s, %s,)
    """, (region_id, title))
    conn.commit()
    conn.close()


def insert_district_to_table_with_id(id, region_id, title):
    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    insert into district (id, region_id, title)
    values (%s, %s, %s)
    """, (id, region_id, title))
    conn.commit()
    conn.close()


def select_all_regions():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"""
        select * from region
        """)
    data = cursor.fetchall()
    return data


def restore_regions():
    file = open('data/regions.csv')
    csvreader = csv.reader(file)
    for row in csvreader:
        insert_region_to_table(row[0], row[1])


def restore_districts():
    file = open('data/districts.csv')
    csvreader = csv.reader(file)
    for row in csvreader:
        print(row)
        insert_district_to_table_with_id(row[0], row[3], row[1])


create_table_profile()
create_table_region()
alter_table_profile()
modify_table_profile_phone()
create_table_district()
add_table_profile_location()

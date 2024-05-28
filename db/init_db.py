import os
import psycopg2

conn = psycopg2.connect(
    dbname="rental_rating_db",
    user='postgres',
    password='pgpassword',
    host="localhost",
    port="5432"
)

# Open a cursor to perform database operations
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS property;')
cur.execute('DROP TABLE IF EXISTS review;')

cur.execute('''
    CREATE TABLE property (
        id serial PRIMARY KEY,
        nom_id varchar (150) NOT NULL,
        lat float NOT NULL,
        long float NOT NULL,
        display_name text NOT NULL,
        date_added date DEFAULT CURRENT_TIMESTAMP
    );
''')
cur.execute('''
    CREATE TABLE review (
        id serial PRIMARY KEY,
        property_id integer NOT NULL,
        content text NOT NULL,
        date_added date DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (property_id) REFERENCES property (id)
    );
''')

# Insert data into the table
cur.execute('INSERT INTO property (nom_id, lat, long, display_name)'
            'VALUES (%s, %s, %s, %s)',
            ('way266888072building',
             37.7497453,
             -122.46276942254607,
             '380, Pacheco Street, Forest Hill, San Francisco, California, 94116, United States')
            )


cur.execute('INSERT INTO review (property_id, content)'
            'VALUES (%s, %s)',
            (1,
             'This has been a great rental! Very quite neighborhood and ample street parking for guests.')
            )

conn.commit()

cur.close()
conn.close()

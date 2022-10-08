from mysql.connector import MySQLConnection, Error
from db_config import read_config
from tabulate import tabulate

def connect_to_db():
    """
        Establishes the connection to the database
        PARAMETERS
            None
        RETURNS
            The connection object
    """
    config = read_config()

    try:
        connection = MySQLConnection(**config)

        if not connection.is_connected():
            print('\nconnection failed')
    except Error as e:
        print(e)

    return connection

def fetch_password(cursor, isAdmin=True, row_id=-1):
    """
        Queries the database and returns the password for admin user
        PARAMETERS
            cursor object
        RETURNS
            The admin password
    """

    if isAdmin:
        cursor.execute('SELECT password FROM users WHERE name LIKE "admin"')
    else:
        cursor.execute(f'SELECT password FROM sites WHERE id={row_id}')

    password = cursor.fetchone()

    return password[0]

def insert_site(cursor, site_info):
    """
        Inserts the information provided by the user into the table
        PARAMETERS
            cursor object
        RETURNS
            True if insert succeeds else False
    """
    keys, values = [], []

    for key, value in site_info.items():
        if value:
            keys.append(key)
            values.append(value)

    n = len(values)

    query_string = f'INSERT INTO sites ({", ".join(keys)}) VALUES ({"%s" + ", %s"*(n-1)})'

    cursor.execute(query_string, tuple(values))

    return bool(cursor.lastrowid)

def fetch_site_info(cursor, site_name):
    """
        Queries the database and just prints all the information for a particular website
        PARAMETERS
            cursor object
        RETURNS
            None
    """
    query_string = f'SELECT id, usrname, registered_mail, site_name FROM sites WHERE site_name LIKE "%{site_name}%"'

    cursor.execute(query_string)
    site_rows = cursor.fetchall()
    row_ids = [row[0] for row in site_rows]

    print('\n', tabulate(site_rows, headers=['id', 'usrname', 'registered_mail', 'site_name'], tablefmt='psql'), sep='')

    return row_ids

def gen_query_string(site_info, sep=''):
    where_cond = []

    for key, value in site_info.items():
        if value:
            if key == 'site_name':
                value = f'%{value}%'
            where_cond.append(f"{key} {sep} '{value}'")

    return where_cond

def get_no_of_sites(cursor, site_info):
    """
        The number of rows returned for a delete query
        PARAMETERS
            cursor object
        RETURNS
            The number of records matched for the delete query
    """
    where_cond = gen_query_string(site_info, sep='LIKE')

    n = len(where_cond)
    if not n:
        return -1

    query_string = f'SELECT id, usrname, registered_mail, site_name FROM sites WHERE {" AND ".join(where_cond) if n > 1 else where_cond[0]}'

    cursor.execute(query_string)
    site_rows = cursor.fetchall()
    row_ids = [row[0] for row in site_rows]

    print('\n', tabulate(site_rows, headers=['id', 'usrname', 'registered_mail', 'site_name'], tablefmt='psql'), sep='')

    return cursor.rowcount, row_ids

def delete_site_info(cursor, data, choice=True):
    """
        Deletes the site information provided by the user
        PARAMETERS
            cursor object
        RETURNS
            Status of deleting the row
    """
    if choice:
        where_cond = gen_query_string(data, sep='LIKE')
        n = len(where_cond)

        if not n:
            print('\nAtleast the website name should be provided')
            return 0

        query_string = f'DELETE FROM sites WHERE {" AND ".join(where_cond) if n > 1 else where_cond[0]}'

        cursor.execute(query_string)
    else:
        query_string = f'DELETE FROM sites WHERE id = {data}'

        cursor.execute(query_string)

    return bool(cursor.rowcount)

def modify_site_info(cursor, site_info, row_id):
    """
        Updates a site information based on the user inputs
        PARAMETERS
            cursor object
            site_information provided by user
            row_id to be updated
        RETURNS
            Status of updating the row
    """
    where_cond = gen_query_string(site_info, sep='=')
    n = len(where_cond)

    if not n:
        print('\nAtleast one value should be provided to modify')
        return 0

    query_string = f'UPDATE sites SET {", ".join(where_cond) if n > 1 else where_cond[0]} WHERE id = %s'

    cursor.execute(query_string, (row_id, ))

    return cursor.rowcount
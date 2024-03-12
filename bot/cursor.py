import MySQLdb


def dbConnect(host, user, password, database):
    conn = MySQLdb.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
        
    return conn


async def selectQuery(conn, query: str) -> list:
    cursor = conn.cursor()
    cursor.execute(query)

    result = cursor.fetchall()

    cursor.close()
    
    return result


async def updateQuery(conn, query: str, params: tuple) -> None:
    cursor = conn.cursor()
    cursor.execute(query, params)
    
    conn.commit()
    
    cursor.close()


if __name__ == '__main__':
    conn = dbConnect('127.0.0.1', 'app', '265013ef-cc8f-4bc1-8727-96568ee03437', 'inspirationalquotebook')
    print(selectQuery(conn, 'SELECT * FROM quotes'))
    conn.close()
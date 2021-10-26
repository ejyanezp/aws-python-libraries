import pyodbc


def connect(connection_data):
    server = f"tcp:{connection_data['host']}"
    database = connection_data['dbname']
    username = connection_data['username']
    password = connection_data['password']
    conn_timeout = 10000 if 'connection-timeout' not in connection_data else connection_data['connection-timeout'] * 1000
    query_timeout = 20000 if 'query-timeout' not in connection_data else connection_data['query-timeout'] * 1000
    conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
    conn = pyodbc.connect(conn_str, timeout=conn_timeout)
    conn.timeout = query_timeout
    return conn


def fetch_result(cursor):
    # Fetch first resultset
    raw_resultset = cursor.fetchall()
    resultset_dict = dict()
    resultset_counter = 0
    while raw_resultset:
        record_counter = 0
        records = []
        for row in raw_resultset:
            columns_dict = dict()
            columns_counter = 0
            for elem in row:
                columns_dict[row.cursor_description[columns_counter][0]] = elem
                columns_counter += 1
            records.append(columns_dict)
            record_counter += 1
        resultset_dict[f"resultset{resultset_counter}"] = records
        resultset_counter += 1
        # Fetch next resultset
        if cursor.nextset():
            raw_resultset = cursor.fetchall()
        else:
            raw_resultset = None
    return resultset_dict


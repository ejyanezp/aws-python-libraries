import cx_Oracle


def declare_parameters(request_map) -> str:
    key_list = list(request_map.keys())
    sql_params = ':' + key_list[0]
    for key in key_list[1:]:  # Remove last element through python's array slicing
        sql_params += ', :' + key
    return sql_params


def connect(connection_data):
    server = connection_data['host']
    port = connection_data['port']
    database = connection_data['dbname']
    db_url = f"{server}:{port}/{database}"
    print(f"db_url={db_url}")
    username = connection_data['username']
    password = connection_data['password']
    query_timeout = 20 if 'query-timeout' not in connection_data else connection_data['query-timeout']
    ora_conn = cx_Oracle.connect(user=username, password=password, dsn=db_url, encoding="UTF-8")
    ora_conn.call_timeout = query_timeout * 1000
    return ora_conn


def fetch_collection(my_collection):
    response = []
    for elem in my_collection:
        my_dict = dict()
        for the_attrib in elem.type.attributes:
            my_dict[the_attrib.name] = getattr(elem, the_attrib.name)
        response.append(my_dict)
    return response


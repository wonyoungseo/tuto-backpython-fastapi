from sqlalchemy import create_engine

db_config = {
    'username': 'root',
    'password': '{YOUR_DB_PASSWORD}',
    'host': '{YOUR_DB_HOST}',
    'port': 3306,
    'database': 'miniter'
}

if __name__ == "__main__":

    db_url = "mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}?charset=utf8".format(
        username=db_config['username'],
        password=db_config['password'],
        host=db_config['host'],
        port=db_config['port'],
        database=db_config['database']
    )
    db = create_engine(db_url, encoding = 'utf-8', max_overflow = 0)

    print(db.table_names())
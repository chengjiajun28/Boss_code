import json
import pymysql


class DatabaseProcessor:
    def __init__(self, config):
        self.host = config['host']
        self.port = config['port']
        self.user = config['user']
        self.password = config['password']
        self.db_name = config['database']
        self.connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db_name,
                connect_timeout=10
            )
            # print("Successfully connected to the database!")
        except pymysql.Error as e:
            raise ConnectionError("Failed to connect to the database:", e)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database.")

    def ensure_connection(self):
        if self.connection:
            self.connection.ping(reconnect=True)

    def execute_query(self, query):
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully!")
        except pymysql.Error as e:
            raise RuntimeError("Failed to execute query:", e)

    def fetch_data_as_dict(self, table_name):
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                sql = f'SELECT * FROM {table_name}'
                cursor.execute(sql)
                rows = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
        except pymysql.Error as e:
            raise RuntimeError("Failed to fetch data:", e)

    def prepare_data(self, value):
        if isinstance(value, (list, dict)):
            return json.dumps(value)
        return value

    def insert_dict_into_mysql(self, data, table_name):
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                fields = ', '.join(key.replace(" ", "_").lower() for key in data.keys())
                placeholders = ', '.join(['%s'] * len(data))
                values = [self.prepare_data(value) for value in data.values()]
                sql = f'INSERT INTO {table_name} ({fields}) VALUES ({placeholders})'
                cursor.execute(sql, values)
            self.connection.commit()
        except pymysql.Error as e:
            print(f"Failed to insert data: {e}")

    def update_data(self, table_name, update_dict, condition_column, condition_value):
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                prepared_data = {k: self.prepare_data(v) for k, v in update_dict.items()}
                set_clause = ", ".join([f"{key} = %s" for key in prepared_data.keys()])
                sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition_column} = %s"
                update_values = list(prepared_data.values()) + [condition_value]
                cursor.execute(sql, update_values)
                self.connection.commit()
        except pymysql.Error as e:
            self.connection.rollback()
            print(f"Failed to update data: {e}")

    def query_data(self, table_name, condition_dict=None, condition_rules=None, columns=None):
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                columns_str = ", ".join(columns) if columns else '*'
                condition_values, conditions = [], []
                if condition_dict:
                    for key, value in condition_dict.items():
                        if value is not None:
                            operator = condition_rules.get(key, '=') if condition_rules else '='
                            conditions.append(f"{key} {operator} %s")
                            condition_values.append(value)
                        else:
                            conditions.append(f"{key} IS NULL")
                condition_str = " AND ".join(conditions) if conditions else ''
                sql = f"SELECT {columns_str} FROM {table_name}" + (f" WHERE {condition_str}" if condition_str else '')
                cursor.execute(sql, condition_values)
                rows = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                return [dict(zip(columns, row)) for row in rows]
        except pymysql.Error as e:
            print(f"Failed to query data: {e}")

    def delete_data(self, table_name, condition_dict):
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                conditions = [f"{key} = %s" for key in condition_dict.keys()]
                condition_str = " AND ".join(conditions)
                sql = f"DELETE FROM {table_name} WHERE {condition_str}"
                cursor.execute(sql, tuple(condition_dict.values()))
                self.connection.commit()
        except pymysql.Error as e:
            self.connection.rollback()
            print(f"Failed to delete data: {e}")

    def truncate_table(self, table_name):
        self.ensure_connection()
        try:
            with self.connection.cursor() as cursor:
                sql = f"TRUNCATE TABLE {table_name}"
                cursor.execute(sql)
                self.connection.commit()
                print(f"Successfully truncated table: {table_name}")
        except pymysql.Error as e:
            self.connection.rollback()
            print(f"Failed to truncate table: {e}")

    def close(self):
        self.disconnect()


# Example usage
if __name__ == '__main__':
    config = {
        'host': '192.168.31.35',
        'port': 3306,
        'user': 'root',
        'password': '5mLH(SPlt(oUm+ct',
        'db': 'housedb_spider',
    }

    with DatabaseProcessor(config) as db_processor:
        condition_dict = {'times': 0}
        condition_rules = {'times': '='}
        id_datas = db_processor.query_data(table_name="agent_ids", condition_dict=condition_dict,
                                           condition_rules=condition_rules)
        print(id_datas)

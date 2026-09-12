import sqlite3
import json


class DBWorker:
    def __init__(self, db_name):
        self.__db_name = db_name
        self.__connect()
        self.__init_db()

    def __connect(self):
        self.__conn = sqlite3.connect(self.__db_name)

    def __init_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS raw_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            shop_name TEXT NOT NULL,
            json_data TEXT NOT NULL);
        """
        with self.__conn:
            self.__conn.execute(query)

    def save(self, shop_name: str, category: str, url: str, data: dict[str]) -> int:
        query = "INSERT OR IGNORE INTO raw_data (shop_name, category, url, json_data) VALUES (?, ?, ?, ?);"
        json_str = json.dumps(data, ensure_ascii=False)
        with self.__conn:
            cur = self.__conn.execute(query, (shop_name, category, url, json_str))
            return cur.rowcount   

    def clear(self):
        with self.__conn:
            self.__conn.execute("DELETE FROM raw_data;")
            self.__conn.execute("DELETE FROM sqlite_sequence WHERE name = 'raw_data';") 

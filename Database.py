import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS conversations (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, phone text, chat_id text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM conversations")
        rows = self.cur.fetchall()
        return rows

    def insert(self, name, phone, chat_id):
        self.cur.execute("INSERT INTO conversations VALUES (NULL, ?, ?, ?, ?)", (name, phone, chat_id))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM conversations WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, name, phone, chat_id):
        self.cur.execute("UPDATE conversations SET name = ?, phone = ?, email = ?, address = ? WHERE id = ?", (name, phone, chat_id, id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

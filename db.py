import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='security.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        self.conn.execute('''CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY,
            command TEXT,
            output TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        
        self.conn.execute('''CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY,
            description TEXT,
            severity INTEGER,
            resolved BOOLEAN DEFAULT 0,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')

    def log_command(self, command, output):
        self.conn.execute('INSERT INTO commands (command, output) VALUES (?, ?)',
                         (command, output))
        self.conn.commit()

    def create_alert(self, description, severity=1):
        self.conn.execute('INSERT INTO alerts (description, severity) VALUES (?, ?)',
                         (description, severity))
        self.conn.commit()
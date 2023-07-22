
import sqlite3


class TodoBotController:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db', check_same_thread=False)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todo_lists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
                description TEXT,
                done BOOLEAN DEFAULT FALSE
)

        ''')
        self.conn.commit()
    
    def add_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO users (name) VALUES (?)', (str(user_id),))
        self.conn.commit()

    def add_task(self, user_id, description):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO todo_lists (user_id, description) VALUES (?, ?)', (user_id, description))
        # list_id = cursor.lastrowid
        # cursor.execute('UPDATE todo_lists SET count_of_user_id = count_of_user_id + 1 WHERE user_id = ? AND id = ?', (user_id, list_id))
        self.conn.commit()
       # return list_id

    def mark_task_done(self, user_id, task_id):
        cursor = self.conn.cursor()
        cursor.execute('select id from (select ROW_NUMBER() OVER () AS pk, id from (SELECT id FROM todo_lists WHERE user_id = ?)) where pk = ?', (user_id, task_id,))
        task_id = cursor.fetchone()[0]
        cursor.execute('UPDATE todo_lists SET done = TRUE WHERE user_id = ? AND id = ?', (user_id, task_id,))
        self.conn.commit()

    def delete_task(self, user_id, task_id):
        cursor = self.conn.cursor()
        cursor.execute('select id from (select ROW_NUMBER() OVER () AS pk, id from (SELECT id FROM todo_lists WHERE user_id = ?)) where pk = ?', (user_id, task_id,))
        task_id = cursor.fetchone()[0]
        cursor.execute('DELETE FROM todo_lists WHERE user_id = ? AND id = ?', (user_id, task_id, ))
        self.conn.commit()

    def get_all_tasks(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM todo_lists WHERE user_id = ?', (user_id,))
        return cursor.fetchall()

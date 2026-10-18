import sqlite3


class Task:
    def __init__(self):
        self.id = None  # Важно для точечного редактирования и отмены
        self.subject = ""
        self.data = ""
        self.text = ""

    def set_subject(self, _subject):
        self.subject = _subject

    def set_data(self, _data):
        self.data = _data

    def set_text(self, _text):
        self.text = _text


class DatabaseManager:
    def __init__(self, db_path: str = "tasks.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject TEXT,
                    data TEXT,
                    text TEXT
                )
            """)
            conn.commit()

    def add_task(self, task: Task) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO tasks (subject, data, text) VALUES (?, ?, ?)",
                (task.subject, task.data, task.text)
            )
            conn.commit()
            return cursor.lastrowid

    def get_all_tasks(self) -> list[Task]:
        tasks_list = []
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Обязательно забираем id первой колонкой
            cursor.execute(
                "SELECT id, subject, data, text FROM tasks ORDER BY id DESC")
            rows = cursor.fetchall()

            for row in rows:
                new_task = Task()
                new_task.id = row[0]  # Записываем ID в объект задачи
                new_task.set_subject(row[1])
                new_task.set_data(row[2])
                new_task.set_text(row[3])
                tasks_list.append(new_task)

        return tasks_list

    def update_task(self, task_id: int, new_text: str, new_date: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE tasks SET text = ?, data = ? WHERE id = ?",
                (new_text, new_date, task_id)
            )
            conn.commit()
            return cursor.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        """Полностью удаляет задачу из базы данных по её ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cursor.rowcount > 0

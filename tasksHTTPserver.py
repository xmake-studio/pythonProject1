import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

TASKS_FILE = 'tasks.txt'

class TaskManager:
    """Управляет списком задач: создание, получение, завершение, сохранение и загрузка."""

    def __init__(self, storage_file=TASKS_FILE):
        self.storage_file = storage_file
        self._tasks = []
        self._next_id = 1
        self._load_tasks()

    def _load_tasks(self):
        """Загружает задачи из файла, восстанавливает next_id."""
        if not os.path.exists(self.storage_file):
            return

        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("Tasks file must contain a JSON array")
                self._tasks = data
                if self._tasks:
                    self._next_id = max(task.get('id', 0) for task in self._tasks) + 1
        except (json.JSONDecodeError, ValueError, OSError) as e:
            # При ошибке — начинаем с чистого листа
            self._tasks = []
            self._next_id = 1

    def _save_tasks(self):
        """Сохраняет текущий список задач в файл."""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self._tasks, f, ensure_ascii=False, indent=2)
        except OSError:
            # Можно логировать, но не прерывать работу
            pass

    def create_task(self, title: str, priority: str) -> dict:
        """Создаёт новую задачу и возвращает её."""
        if not isinstance(title, str) or not isinstance(priority, str):
            raise ValueError("title and priority must be strings")
        if priority not in ('low', 'normal', 'high'):
            raise ValueError("priority must be 'low', 'normal', or 'high'")

        task = {
            'id': self._next_id,
            'title': title,
            'priority': priority,
            'isDone': False
        }
        self._tasks.append(task)
        self._next_id += 1
        self._save_tasks()
        return task

    def get_all_tasks(self) -> list:
        """Возвращает копию списка всех задач."""
        return self._tasks.copy()

    def complete_task(self, task_id: int) -> bool:
        """Отмечает задачу как выполненную. Возвращает True, если задача найдена."""
        if not isinstance(task_id, int):
            return False
        for task in self._tasks:
            if task.get('id') == task_id:
                task['isDone'] = True
                self._save_tasks()
                return True
        return False


class TaskHTTPRequestHandler(BaseHTTPRequestHandler):
    """Обрабатывает HTTP-запросы, используя TaskManager."""

    def __init__(self, *args, task_manager: TaskManager, **kwargs):
        self.task_manager = task_manager
        super().__init__(*args, **kwargs)

    def _send_json_response(self, status_code: int, data=None):
        """Универсальный метод отправки JSON-ответа."""
        self.send_response(status_code)
        if data is not None:
            body = json.dumps(data, ensure_ascii=False).encode('utf-8')
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        if data is not None:
            self.wfile.write(body)

    def do_GET(self):
        if self.path == '/tasks':
            tasks = self.task_manager.get_all_tasks()
            self._send_json_response(200, tasks)
        else:
            self._send_json_response(404)

    def do_POST(self):
        if self.path == '/tasks':
            # Чтение тела запроса
            content_length_header = self.headers.get('Content-Length')
            if content_length_header is None:
                self._send_json_response(400, {"error": "Missing Content-Length header"})
                return

            try:
                content_length = int(content_length_header)
                if content_length <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                self._send_json_response(400, {"error": "Invalid Content-Length"})
                return

            try:
                raw_body = self.rfile.read(content_length)
                body = json.loads(raw_body.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError, OSError):
                self._send_json_response(400, {"error": "Invalid JSON"})
                return

            if not isinstance(body, dict):
                self._send_json_response(400, {"error": "Request body must be a JSON object"})
                return

            title = body.get('title')
            priority = body.get('priority')

            if not isinstance(title, str) or not isinstance(priority, str):
                self._send_json_response(400, {"error": "Missing or invalid 'title' or 'priority'"})
                return

            try:
                task = self.task_manager.create_task(title, priority)
                self._send_json_response(201, task)
            except ValueError as e:
                self._send_json_response(400, {"error": str(e)})

        elif self.path.endswith('/complete'):
            # Парсим ID из пути: /tasks/123/complete
            path_parts = self.path.strip('/').split('/')
            if len(path_parts) != 3 or path_parts[0] != 'tasks' or path_parts[2] != 'complete':
                self._send_json_response(404)
                return

            try:
                task_id = int(path_parts[1])
            except ValueError:
                self._send_json_response(404)
                return

            if self.task_manager.complete_task(task_id):
                self._send_json_response(200)
            else:
                self._send_json_response(404)

        else:
            self._send_json_response(404)


def main():
    task_manager = TaskManager()
    
    # Фабрика обработчиков с внедрением зависимости
    def handler_factory(*args, **kwargs):
        return TaskHTTPRequestHandler(*args, task_manager=task_manager, **kwargs)

    server = HTTPServer(('', 8000), handler_factory)
    print("Task server started on http://localhost:8000")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.server_close()


if __name__ == '__main__':
    main()
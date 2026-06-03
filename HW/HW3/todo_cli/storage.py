import json
from pathlib import Path
from typing import Optional

from .models import Todo


class TodoStorage:
    def __init__(self, data_file: Optional[str] = None) -> None:
        self.data_file = Path(data_file) if data_file else Path.home() / ".todo_data.json"
        self._todos: dict[int, Todo] = {}
        self._next_id = 1
        self._load()

    def _load(self) -> None:
        if self.data_file.exists() and self.data_file.stat().st_size > 0:
            data = json.loads(self.data_file.read_text())
            self._next_id = data.get("next_id", 1)
            for todo_data in data.get("todos", []):
                todo = Todo(**todo_data)
                self._todos[todo.id] = todo

    def _save(self) -> None:
        data = {
            "next_id": self._next_id,
            "todos": [t.model_dump() for t in self._todos.values()],
        }
        self.data_file.write_text(json.dumps(data, indent=2))

    def add(self, title: str, priority: int = 1) -> Todo:
        todo = Todo(id=self._next_id, title=title, priority=priority)
        self._todos[todo.id] = todo
        self._next_id += 1
        self._save()
        return todo

    def get(self, todo_id: int) -> Optional[Todo]:
        return self._todos.get(todo_id)

    def list_all(self, show_completed: bool = True, priority: Optional[int] = None) -> list[Todo]:
        todos = list(self._todos.values())
        if not show_completed:
            todos = [t for t in todos if not t.completed]
        if priority is not None:
            todos = [t for t in todos if t.priority == priority]
        return sorted(todos, key=lambda t: (-t.priority, t.created_at))

    def complete(self, todo_id: int) -> Optional[Todo]:
        todo = self._todos.get(todo_id)
        if todo and not todo.completed:
            todo.mark_complete()
            self._save()
            return todo
        return None

    def delete(self, todo_id: int) -> bool:
        if todo_id in self._todos:
            del self._todos[todo_id]
            self._save()
            return True
        return False

    def search(self, query: str) -> list[Todo]:
        query_lower = query.lower()
        return [t for t in self._todos.values() if query_lower in t.title.lower()]

    @property
    def count(self) -> int:
        return len(self._todos)

    @property
    def pending_count(self) -> int:
        return sum(1 for t in self._todos.values() if not t.completed)

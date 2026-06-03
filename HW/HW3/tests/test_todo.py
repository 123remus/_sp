import pytest
from todo_cli.models import Todo
from todo_cli.storage import TodoStorage
import tempfile
import os


@pytest.fixture
def storage():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name
    yield TodoStorage(path)
    os.unlink(path)


class TestTodo:
    def test_create_todo(self):
        todo = Todo(id=1, title="Test task")
        assert todo.id == 1
        assert todo.title == "Test task"
        assert todo.completed is False
        assert todo.priority == 1

    def test_priority_label(self):
        assert Todo(id=1, title="t", priority=1).priority_label == "low"
        assert Todo(id=1, title="t", priority=2).priority_label == "medium"
        assert Todo(id=1, title="t", priority=3).priority_label == "high"

    def test_mark_complete(self):
        todo = Todo(id=1, title="Test task")
        todo.mark_complete()
        assert todo.completed is True
        assert todo.completed_at is not None


class TestStorage:
    def test_add_and_get(self, storage):
        todo = storage.add("Buy milk", priority=2)
        assert todo.id == 1
        fetched = storage.get(1)
        assert fetched is not None
        assert fetched.title == "Buy milk"

    def test_list_all(self, storage):
        storage.add("Task 1", priority=1)
        storage.add("Task 2", priority=2)
        todos = storage.list_all()
        assert len(todos) == 2
        assert todos[0].priority == 2  # higher priority first

    def test_complete(self, storage):
        todo = storage.add("Finish report")
        storage.complete(todo.id)
        assert storage.get(todo.id).completed is True

    def test_delete(self, storage):
        todo = storage.add("Temp task")
        assert storage.delete(todo.id) is True
        assert storage.get(todo.id) is None
        assert storage.delete(999) is False

    def test_search(self, storage):
        storage.add("Buy groceries")
        storage.add("Buy books")
        storage.add("Read news")
        results = storage.search("buy")
        assert len(results) == 2

    def test_list_filter_priority(self, storage):
        storage.add("Low task", priority=1)
        storage.add("High task", priority=3)
        high = storage.list_all(priority=3)
        assert len(high) == 1
        assert high[0].priority == 3

    def test_list_hide_completed(self, storage):
        todo = storage.add("Done task")
        storage.complete(todo.id)
        storage.add("Pending task")
        active = storage.list_all(show_completed=False)
        assert len(active) == 1
        assert active[0].title == "Pending task"

    def test_persistence(self):
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        s1 = TodoStorage(path)
        s1.add("Persistent task")
        s2 = TodoStorage(path)
        assert s2.count == 1
        assert s2.get(1).title == "Persistent task"
        os.unlink(path)

    def test_counts(self, storage):
        storage.add("Task 1")
        todo2 = storage.add("Task 2")
        storage.complete(todo2.id)
        assert storage.count == 2
        assert storage.pending_count == 1

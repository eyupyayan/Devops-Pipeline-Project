from datetime import datetime
from typing import Dict, List, Optional

from .models import Task, TaskCreate


class InMemoryTaskStore:
    def __init__(self) -> None:
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def list_tasks(self) -> List[Task]:
        return list(self._tasks.values())

    def get_task(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    def create_task(self, data: TaskCreate) -> Task:
        task = Task(
            id=self._next_id,
            title=data.title,
            description=data.description,
            done=False,
            created_at=datetime.utcnow(),
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def mark_done(self, task_id: int) -> Optional[Task]:
        task = self._tasks.get(task_id)
        if not task:
            return None
        task.done = True
        self._tasks[task_id] = task
        return task

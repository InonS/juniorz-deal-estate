"""
ClearML experiment tracking.
"""
from clearml import Task

def initialize_clearml_task(project_name: str, task_name: str) -> Task:
    """
    Initialize a ClearML experiment tracking task.

    Args:
        project_name: Project name.
        task_name: Task name.

    Returns:
        ClearML Task object.

    >>> isinstance(initialize_clearml_task("MyProj", "MyTask"), Task)  # doctest: +SKIP
    True
    """
    task = Task.init(project_name=project_name, task_name=task_name)
    return task
from celery import Celery

app = Celery(
    'main',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['tasks', 'other_tasks']
)

app.conf.beat_schedule = {
    'print-every-10-seconds': {
        'task': 'tasks.print_hello',
        'schedule': 10.0,
        'args': (),
    },
    'another-task': {
        'task': 'other_tasks.another_task',
        'schedule': 20.0,
        'args': (),
    }
}

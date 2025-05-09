from celery import Celery

# 创建 Celery 应用
app = Celery('tasks',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

# 定时任务配置 - 现在提供两个参数
app.conf.beat_schedule = {
    'print-every-10-seconds': {
        'task': 'tasks.add',  # 任务名称
        'schedule': 10.0,     # 每10秒执行一次
        'args': (3, 5),       # 提供两个参数
        # 'kwargs': {}     # 明确添加空的关键字参数
    },
}

# 定义任务


@app.task(name='tasks.add', bind=True)
def add(self, x, y):
    print(f"计算 {x} + {y}")
    return x + y


@app.task(name='tasks.print_hello', bind=True)
def print_hello(self):
    print(f"hello world")
    return "hello world"

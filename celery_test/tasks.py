from celery import shared_task


@shared_task(name='tasks.print_hello', bind=True)
def print_hello(self):
    print("Hello, this is a scheduled task!")

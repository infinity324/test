from celery import shared_task


@shared_task(name='other_tasks.another_task')
def another_task():
    print("This is another task!")

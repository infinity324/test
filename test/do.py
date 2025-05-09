from celery_app import print_hello, add

print_hello.delay()  # 延迟执行任务，不等待结果
add.delay(3, 5)  # 延迟执行任务，不等待结果

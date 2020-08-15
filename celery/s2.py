from celery.result import AsyncResult
from s1 import my_goods

def callback(task_id):
    async_task = AsyncResult(id=task_id,app=my_goods)
    if async_task.successful():
        return async_task.get()
    else:
        return "玩儿命抢购ing......"
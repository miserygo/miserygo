from celery import Celery
import time
my_goods = Celery("task",broker="redis://127.0.0.1",backend="redis://127.0.0.1")

@my_goods.task
def goods(id):
    time.sleep(5)
    return f"抢购成功{id}"
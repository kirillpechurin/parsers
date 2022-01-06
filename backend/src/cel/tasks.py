from celery import Celery


app = Celery("tasks", backend='rpc://', broker="amqp://guest:guest@rabbitmq:5672//")

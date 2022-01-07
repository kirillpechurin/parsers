from celery import Celery

app = Celery(
    "src.cel",
    backend='rpc://',
    broker="amqp://guest:guest@rabbitmq:5672//",
    include=[
        'src.cel.tasks.map_parser',
        "src.cel.tasks.send_mail"
    ]
)

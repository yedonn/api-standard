from faststream import FastStream
from app.core.config import settings
from faststream.rabbit.fastapi import  RabbitBroker

broker = RabbitBroker(url=f"amqp://guest:guest@{settings.RABBITMQ_URL}:{settings.RABBITMQ_PORT}/",apply_types=False)
app = FastStream(broker)

@broker.subscriber("test_rabbitmq")
async def user_created(user_id):
    print(user_id["test"])

@broker.subscriber("user")
async def user_created(user_id):
    print(user_id)

@broker.publisher("user")
async def pub_smth():
    await broker.publish(1, "user", rpc=True)
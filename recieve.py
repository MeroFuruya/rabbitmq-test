import pika # type: ignore
from dotenv import load_dotenv
from os import getenv

load_dotenv()

parameters = pika.ConnectionParameters(
  host=getenv("RABBITMQ_HOST"),
  port=getenv("RABBITMQ_PORT"),
  credentials=pika.PlainCredentials(
    username=getenv("RABBITMQ_USER"),
    password=getenv("RABBITMQ_PASSWORD")
  )
)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

def callback(ch, method, properties, body):
  print(f" [x] Received {body}")

channel.basic_consume(
  queue='hello',
  auto_ack=True,
  on_message_callback=callback
)

print(' [*] Waiting for messages. To exit press CTRL+C')
try:
  channel.start_consuming()
except KeyboardInterrupt:
  pass
finally:
  channel.close()
  connection.close()
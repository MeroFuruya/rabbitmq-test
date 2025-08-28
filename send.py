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

channel.queue_declare(queue='hello')

while True:
  message = input("Enter your message: ")
  if message.lower() == 'exit':
    break
  channel.basic_publish(exchange='', routing_key='hello', body=message)
  print(f" [x] Sent '{message}'")

channel.close()
connection.close()
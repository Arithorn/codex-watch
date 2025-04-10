#!/usr/bin/env python
import pika
auth = pika.PlainCredentials("codex", "Google123")
connection = pika.BlockingConnection(
    pika.ConnectionParameters('rabbit.lan', credentials=auth))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()

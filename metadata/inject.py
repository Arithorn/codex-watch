import pika
import sys
import os
import time
import json
import pika.delivery_mode

queue_name = "codex/metadata"


def send(msg):
    rabbit_username = os.environ.get("RABBIT_USER")
    rabbit_password = os.environ.get("RABBIT_PASS")
    rabbit_server = os.environ.get("RABBIT_SERVER")

    # Check for Environment Variables
    if not rabbit_username:
        print("ERROR: RABBIT_USER environment variable not set.")
        exit()
    if not rabbit_password:
        print("ERROR: RABBIT_PASS environment variable not set.")
        exit()
    if not rabbit_server:
        print("ERROR: RABBIT_SERVER environment variable not set.")
        exit()

    # Connect to the rabbitmq server
    auth = pika.PlainCredentials(rabbit_username, rabbit_password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(rabbit_server, credentials=auth))
    metadata_channel = connection.channel()
    metadata_channel.queue_declare(queue=queue_name)
    metadata_channel.basic_publish(
        exchange='', routing_key=queue_name, properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent), body=msg)
    print(f" [x] Sent {msg}")
    connection.close()


if __name__ == '__main__':
    data = {}
    data["type"] = "author"
    data["name"] = "Zogarth"
    data["id"] = 344878
    jsonmsg = json.dumps(data)
    try:
        send(jsonmsg)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

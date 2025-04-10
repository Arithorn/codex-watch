#!/usr/bin/env python
import pika
import sys
import os
import time
import json
from MetaDataProcessor import MetaDataProcessor
from hardcover import HardCover


# def searchAuthor(authorId: int):
#     hardcover = HardCover()
#     print(f"Searching for author : {authorId}")
#     hardcover.getBooksByAuthor(authorId=authorId)
#     return


def processMessage(body):
    processor = MetaDataProcessor()
    processor.process(body)
    time.sleep(2)
    return


def main():
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
    metadata_channel.queue_declare(queue='codex/metadata')

    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
        processor = MetaDataProcessor()
        processor.process(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    metadata_channel.basic_consume(
        queue='codex/metadata', on_message_callback=callback)

    print(' [*] Waiting for tasks!. To exit press CTRL+C')
    metadata_channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

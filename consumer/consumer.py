import os
import sys
import time

import pika
from convert import to_mp3

from apps.converter_service.models import MP3, Videos
from converter.rmq_server import channel


def consumer_callback(channel, method, properties, body):
    # to_mp3 returns an error if to_mp3 fail
    error = to_mp3.start(body, Videos, MP3, channel)

    if error:
        # send a negative acknowledgement to the channel
        # That means this is not going to acknowledge if received and
        # processed the message
        # and the message won`t be removed from the queue to be processed later
        channel.basic_nack(delivery_tag=method.delivery_tag)
    else:
        channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"),
        on_message_callback=consumer_callback
    )

    print("Waiting for messages. To exit press CTRL + C")

    # run the consumer
    channel.start_consuming()


if __name__ == "__main__":
    # run the main function or stop when the user press CTRL + C
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

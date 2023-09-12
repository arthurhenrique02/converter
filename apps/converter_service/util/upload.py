import json

import pika

from apps.converter_service.models import File


def upload(request, channel):
    """
    A function that gets a request with the file and username that have sent
    A channel created to send messages through rabbitMQ

    return: a tuple containing json message and the HTTP status
    """
    try:
        # get file instance
        file = File.objects.create(file=request.data["file"])

        file.save()
    except Exception:
        # return an error message and status
        return ({"message": "internal server error"}, 500)

    message = {
        "video_file_id": str(file.id),
        "mp3_file_id": None,
        "username": request.data["username"]
    }

    try:
        channel.basic_publish(
            # default rabbitmq exchange ("")
            # exchange is the 'man' that alocate the message and
            # send to correctly queue
            exchange="",
            # routing_key is the queue that the exchange have to send
            # the message
            routing_key="video",
            # message is all the information that will be processed
            body=json.dumps(message),
            properties=pika.BasicProperties(
                # make sure that the message still persisted
                # when the pod crashes or restart
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception:
        # delete the file from db
        file.delete()

        # return an error message and status
        return ({"message": "internal server error"}, 500)

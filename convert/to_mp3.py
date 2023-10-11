import json
import os
import tempfile

import moviepy.editor
import pika
from bson.objectid import ObjectId

from apps.converter_service.models import MP3, Videos


def start(message, videos, mp3s, channel):
    # load the message
    message = json.loads(message)

    # empty temp file to write the video on this file
    temp_file = tempfile.NamedTemporaryFile()

    # we need to get the file from the id object
    # not from the string id (as we defined when created message object on
    # upload.py)
    # so we use ObejectId to create this id object and search on db
    video = Videos.objects.get(id=message["video_file_id"])

    # add video content to temp file
    # read the bytes from the video and write through temp_file
    # TODO:
    # CHANGE OPENNING FILE METHOD
    temp_file.write(open(video.file, "rb"))

    # convert the video file to audio file
    # VideoFileClip will get the temp_file path and extract the audio
    audio = moviepy.editor.VideoFileClip(temp_file.name).audio

    temp_file.close()

    # get temp_file path
    temp_file_path = temp_file.gettempdir() + f"/{message['video_file_id']}.mp3"

    # write audio on temp_file_path file
    audio.write_audiofile(temp_file_path)

    with open(temp_file_path, "rb") as audio_f:
        audio_data = audio_f.read()

        audio_file = MP3.objects.create(file=audio_data)

        audio_file.save()

    # remove temp_file
    os.remove(temp_file_path)

    message["mp3_file_id"] = str(audio_file.id)

    # try to publish on a different queue
    try:
        channel.basic_publish(
            # default exchange
            exchange="",
            # queue
            routing_key=os.environ.get("MP3_QUEUE"),
            # message body
            body=json.dumps(message),
            # make sure of persitency
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
    except Exception:
        audio_file.delete()

        # return an error message
        return ({"message": "failed to publish message"}, 500)

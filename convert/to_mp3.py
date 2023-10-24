import json
import os
import tempfile

import moviepy.editor
import pika
from django.core.files.base import ContentFile

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
    with video.file.open('rb') as video_file:
        video_binary = video_file.read()

    # Write the binary content to the temp_file
    temp_file.write(video_binary)

    # convert the video file to audio file
    # VideoFileClip will get the temp_file path and extract the audio
    audio = moviepy.editor.VideoFileClip(temp_file.name).audio

    temp_file.close()

    # get temp_file path
    temp_file_path = tempfile.gettempdir() + f"/{message['video_file_id']}.mp3"

    # write audio on temp_file_path file
    audio.write_audiofile(temp_file_path)

    with open(temp_file_path, "rb") as audio_f:
        # TODO:
        # solve the problem that`s not reading the mp3 file and saving on db
        audio_data = audio_f.read()

        audio_file = MP3.objects.create(
            file=ContentFile(audio_data))

        # change mongo db id (_id) and django id

        print(audio_file.__dict__)
        print(audio_file.file)

        audio_file.save(using="mp3s_db")

    # remove temp_file
    os.remove(temp_file_path)

    print(audio_file.file)

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

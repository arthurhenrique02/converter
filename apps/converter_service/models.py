import os

from django.conf import settings
from djongo import models
from djongo.storage import GridFSStorage

# videos(mp4s) GridFs instance
videos_grid_fs_storage = GridFSStorage(
    collection='videosCollection',
    base_url=''.join(
        [os.environ.get("MONGO_HOST"), ":27017/", 'filesdb/']
    ),
    database="videos_db"
)
# mp3s GridFs instance
mp3s_grid_fs_storage = GridFSStorage(
    collection='mp3sCollection',
    base_url=''.join(
        [os.environ.get("MONGO_HOST"), ":27017/", 'mp3sdb/']
    ),
    database="mp3s_db"
)


# Create your models here.
class Videos(models.Model):

    # change storage format as grid_fs
    # gridFS is an storage format to storage files greater than 16MB and
    # not loss quality
    file = models.FileField(storage=videos_grid_fs_storage)


class MP3(models.Model):

    # change storage format as grid_fs
    # gridFS is an storage format to storage files greater than 16MB and
    # not loss quality
    file = models.FileField(storage=mp3s_grid_fs_storage)

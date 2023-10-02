import os

from django.conf import settings
from djongo import models
from djongo.storage import GridFSStorage

# GridFs instance
grid_fs_storage = GridFSStorage(
    collection='videosCollection',
    base_url=''.join(
        [os.environ.get("MONGO_HOST"), ":27017/", 'filesdb/']
    ),
    database="files_db"
)


# Create your models here.
class Videos(models.Model):

    # change storage format as grid_fs
    # gridFS is an storage format to storage files greater than 16MB and
    # not loss quality
    file = models.FileField(storage=grid_fs_storage)


class MP3(models.Model):

    # change storage format as grid_fs
    # gridFS is an storage format to storage files greater than 16MB and
    # not loss quality
    file = models.FileField(storage=grid_fs_storage)

from django.conf import settings
from django.db import models
from djongo.storage import GridFSStorage

# GridFs instance
grid_fs_storage = GridFSStorage(
    collection='videosCollection',
    base_url=''.join(["mongodb://localhost:27017", 'filesdb/'])
)

# Create your models here.


class File(models.Model):

    # change storage format as grid_fs
    # gridFS is an storage format to storage files greater than 16MB and
    # not loss quality
    file = models.FileField(storage=grid_fs_storage)

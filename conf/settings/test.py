import tempfile
from .base import *  # noqa

for key, value in RQ_QUEUES.items():  # noqa
    value["ASYNC"] = False

_temp_media = tempfile.mkdtemp()
MEDIA_ROOT = _temp_media
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

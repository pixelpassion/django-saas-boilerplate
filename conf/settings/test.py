from .base import *  # noqa

for key, value in RQ_QUEUES.items():  # noqa
    value["ASYNC"] = False

"""A MinioProvider Service Provider."""
from .MinioDriver import MinioDriver
from masonite.providers import Provider
from masonite.filesystem import Storage
from masonite.configuration import config


class MinioProvider(Provider):

    def __init__(self, application):
        self.application = application

    def register(self):
        storage = Storage(self.application).set_configuration(
            config("filesystem.disks")
        )
        storage.add_driver("minio", MinioDriver(self.application))
        self.application.bind("storage", storage)

    def boot(self):
        pass
"""A MinioProvider Service Provider."""
from .MinioDriver import MinioDriver
from masonite.providers import Provider


class MinioProvider(Provider):
    def __init__(self, application):
        self.application = application

    def register(self):
        self.application.make("storage").add_driver(
            "minio", MinioDriver(self.application)
        )

    def boot(self):
        """ not required
        """
        pass
